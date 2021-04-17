""" This module exports the Chord class representing a sequence of notes identifiable as a chord
    and the ChordFactory class for creating chords.
"""

from .music_info import identify_chord_numeral_for_key, identify_secondary_dominant_numeral, get_chord_for_intervals, identify_applied_numeral
from .note import NoteFactory


class ChordFactory:
    """Factory Class responsible for handling the creation of Chords using passed string or JSON/Dict-formatted data."""

    _note_factory = NoteFactory()

    def create_chord(self, chord_info):
        """Creates a chord using the passed chord string information."""

        if isinstance(chord_info, str):
            chord_data = self.parse_chord_string(chord_info)

        elif isinstance(chord_info, dict):
            chord_data = self.parse_chord_dict(chord_info)

        else:
            raise ValueError('Invalid chord information format received.')

        if chord_data['valid']:
            return Chord(chord_data['notes'])
            
        else:
            raise ValueError(chord_data['error'])

    def parse_chord_dict(self, chord_dict):
        """Parses the passed dict detailing this chord's notes into its individual notes."""

        notes = chord_dict['notes']
        chord_data = self.parse_chord_string(notes)

        return chord_data

    def parse_chord_string(self, chord_string):
        """Parses the passed string detailing this chord's notes into its individual notes."""

        notes = chord_string.split(',')

        chord_data = {}

        #Check if enough notes were provided for the chord
        if len(notes) >= 3:
            chord_data['notes'] = []

            try:
                for note_string in notes:
                    note_string = note_string.strip()
                    chord_note = self._note_factory.create_note(note_string)

                    chord_data['notes'].append(chord_note)

            except ValueError:
                chord_data['valid'] = False
                chord_data['error'] = 'One or more notes provided were invalid.'

            else:
                chord_data['valid'] = True

        else:
            chord_data['valid'] = False
            chord_data['error'] = 'Not enough notes provided for the chord.'

        return chord_data



class Chord:
    """Class defining a chord as a series of 3+ notes with a specific pattern of intervals between them."""

    def __init__(self, chord_notes):
        self.position = 0
        self.root_index = 0
        self.quality = ''
        self.has_seventh = False

        #Set the notes to the ones passed
        self.notes = chord_notes

        #Identify the chord's position and inversion
        self.__identify_chord()

    def __get_interval_string_info(self):
        """Crafts this chord's interval string for identifying its name and quality.
        
            This method will iterate through all of the chord's listed intervals and create a string that only incorporates
            the intervals between unique notes in the chord. Ex. C3 E3 G3 C4 will omit G3 -> C4
        """

        interval_string = ""

        #Create a temporary copy of this chord's notes
        unique_note_names = []
        unique_notes = []

        #Sort this chord's notes by value to get the proper interval string
        self.notes.sort(key=lambda note: note.value)

        #Filter the chord's notes, to only get those with unique names
        for note in self.notes:

            if note.name not in unique_note_names:
                unique_notes.append(note)
                unique_note_names.append(note.name)

        #Build the chord's interval string using the unique notes
        for i, curr_note in enumerate(unique_notes[0:-1]):
            next_note = unique_notes[i+1]
            interval_string += str((next_note.value - curr_note.value) % 12)
            
        return (interval_string, unique_notes)

    def find_notes_by_name(self, search_name):
        """Searches for and returns the index/indices of any notes in this chord that match
        the name provided.
        """

        note_indicies = []

        for i, note in enumerate(self.notes):
            if note.name == search_name:
                note_indicies.append(i)
            
        return note_indicies

    def get_accidentals_for_key(self, key):
        """Returns an array of accidentals for this chord's notes"""

        accidentals = []

        for note in self.notes:
            accidentals.append(note.get_accidental_for_key(key))

        return accidentals

    def get_indices_from_interval(self, interval): 
        """Returns the index or indicies of the note(s) with the specified interval from the 
        chord's root note.
        """

        root_note = self.notes[self.root_index]
        matching_notes = []

        for i, note in enumerate(self.notes):
            if root_note.get_interval(note) == interval:
                matching_notes.append(i)

        return matching_notes

    def get_root_name(self):
        """Returns the name of this chord's root note."""

        return self.notes[self.root_index].name

    def get_seventh_index(self):
        """Returns the index of this chord's seventh, if it has one."""

        note_index = -1

        if self.has_seventh:
            root_note = self.notes[self.root_index]
        
            for i, note in enumerate(self.notes):

                if note.name != root_note.name:
                    interval = root_note.get_interval(note)

                    #The seventh note's interval from the root note depends on the chord's quality
                    if interval == 11 and self.quality == 'maj7':
                        note_index = i

                    elif interval == 10 and self.quality in ['7', 'm7', 'ø']:
                        note_index = i

                    elif interval == 9 and self.quality == 'o7':
                        note_index = i

                    if note_index != -1:
                        break

        return note_index

    def get_name(self, slash_notation=False):
        """Returns this chord's name in slash notation or in a normal."""

        if slash_notation and self.position != 0:
            return f'{self.notes[self.root_index].name}{self.quality}/{self.notes[0].name}'

        else:
            return f'{self.notes[self.root_index].name}{self.quality}'

    def get_numeral_for_key(self, key, use_inversion=True):
        """Returns this chord's numeral relative to the given key. The inversion string is included if specified."""

        numeral = ''

        if self.quality != 'unknown':
            numeral = identify_chord_numeral_for_key(key, {"root": self.notes[self.root_index].name, 
            "quality": self.quality, "position": self.position, "has_seventh": self.has_seventh}, use_inversion)

        return numeral

    def get_secondary_dominant_numeral(self, base_chord, use_inversion=True):
        """Returns this chord's numeral as a secondary dominant for the passed chord, if it acts as one."""

        #Get the root of the passed chord from its root index as the 'key'
        base_chord_root = base_chord.get_root_name()

        return identify_applied_numeral(base_chord_root, base_chord.quality, {'root': self.notes[self.root_index].name, 
        'quality': self.quality, 'position': self.position, 'has_seventh': self.has_seventh}, use_inversion)

        # return identify_secondary_dominant_numeral(self.get_name(), self.position, self.has_seventh, base_chord_key, second_chord.quality)

    def __identify_chord(self):
        """Identifies the name and quality of this chord by determining its root index and position."""

        interval_string, unique_notes = self.__get_interval_string_info()

        #Get the dictionary object representing the chord for the chord's interval string
        chord_obj = get_chord_for_intervals(interval_string)

        if chord_obj['quality'] == 'unknown':
            self.root_index = 0
            self.position = 0
            self.quality = ''

        else:

            #If this chord has no duplicate notes, set its properties as normal
            if len(unique_notes) == len(self.notes):
                self.root_index = chord_obj['root_index']

            #Else, find the location of this chord's root note within its list of notes
            else:
                chord_root_note = unique_notes[chord_obj['root_index']].name

                for i, note in enumerate(self.notes):
                    
                    if note.name == chord_root_note:
                        self.root_index = i
                        break

            self.quality = chord_obj['quality']
            self.position = chord_obj['position']

            #Check if this chord has a seventh
            if self.quality in ['7','m7','maj7','ø','o7']:
                self.has_seventh = True

    def __len__(self):
        """Returns the number of notes in this chord"""

        return len(self.notes)

    def __repr__(self):
        """Returns a simple string representation of the chord for its re-creation."""

        chord_string = ""

        #Reconstruct the chord string passed to this class instance
        for _, note in enumerate(self.notes):
            chord_string += note.name + str(note.octave) + ', '
            
        #Remove the trailing comma
        return chord_string[0:-2]

    def __str__(self):
        return self.__repr__()
       
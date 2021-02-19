import musicInfo as music_info

from note import NoteFactory
from exceptions import InvalidChordError, InvalidNoteError


class ChordFactory:
    """Factory Class responsible for handling the creation of Chords using passed string or JSON/Dict-formatted data."""

    _note_factory = NoteFactory()

    def create_chord(self, chord_info):
        """Creates a chord using the passed chord string information."""

        if type(chord_info) == str:
            chord_data = self.parse_chord_string(chord_info)

        elif type(chord_info) == dict:
            chord_data = self.parse_chord_dict(chord_info)

        else:
            raise ValueError('Invalid chord information format received.')

        if chord_data['valid']:
            return Chord(chord_data['notes'])
            
        else:
            raise ValueError(chord_data['error'])

    def parse_chord_dict(self, chord_dict):
        return {}

    def parse_chord_string(self, chord_string):
        """Parses the passed string detailing this chord's notes into its individual notes."""

        chord_data = {}

        notes = chord_string.split(',')

        #Check if enough notes were provided for the chord
        if len(notes) >= 3:
            chord_data['notes'] = []

            try:

                for note_string in notes:
                    note_string = note_string.strip()
                    chord_note = self._note_factory.create_note(note_string)

                    chord_data['notes'].append(chord_note)

            except:
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
        self.name = ''
        self.position = 0
        self.bass_index = 0
        self.quality = ''
        self.has_seventh = False

        #Set the notes to the ones passed
        self.notes = chord_notes

        #Identify the chord's position and inversion
        self.identify_chord()

    def get_interval_string_info(self):
        """Crafts this chord's interval string for identifying its name and quality.
        
            This method will iterate through all of the chord's listed intervals and create a string that only incorporates
            the intervals between unique notes in the chord. Ex. C3 E3 G3 C4 will omit G3 -> C4
        """

        interval_string = ""

        #The unique notes already found present in the chord
        unique_notes = []

        #Sort this chord's notes by value to get the proper interval string
        self.notes.sort(key=lambda note: note.value)
        
        for i, curr_note in enumerate(self.notes[0:-1]):
            next_note = self.notes[i+1]

            if curr_note.name in unique_notes:
                continue

            unique_notes.append(curr_note.name)

            #If the next note is a duplicate, check the name of the one after it (if possible)
            if next_note.name in unique_notes:

                if i + 2 < len(self.notes):
                    next_next_note = self.notes[i+2]
                    new_interval = (next_next_note.value - curr_note.value) % 12
                    interval_string += str(new_interval)
                    
            else:
                interval_string += str((next_note.value - curr_note.value) % 12)
        
        #If the final note is a unique note and wasn't added to the array to return, add it
        if self.notes[-1].name not in unique_notes:
            unique_notes.append(self.notes[-1].name)

        return (interval_string, unique_notes)

    def get_name(self, slash_notation=False):
        """Returns this chord's name in slash notation or a regular format."""

        if slash_notation and self.position != 0:
            return f'{self.notes[self.bass_index].name}{self.quality}/{self.notes[0].name}'

        else:
            return f'{self.notes[self.bass_index].name}{self.quality}'

    def identify_chord(self):
        """Identifies this chord by setting its name and bass_index according to its bass index and chord quality."""

        interval_string, unique_notes = self.get_interval_string_info()

        #Get the dictionary object representing the chord for the chord's interval string
        chord_obj = music_info.get_chord_for_intervals(interval_string)

        if chord_obj['quality'] == 'unknown':
            self.bass_index = 0
            self.position = 0
            self.quality = ''

        else:

            #If this chord has no duplicate notes, set its properties as normal
            if len(unique_notes) == len(self.notes):
                self.bass_index = chord_obj['bass_index']

            #Else, find the location of this chord's bass note within its list of notes
            else:
                chord_bass_note = unique_notes[chord_obj['bass_index']]

                for i, note in enumerate(self.notes):

                    if note.name == chord_bass_note:
                        self.bass_index = i
                        break

            self.quality = chord_obj['quality']
            self.position = chord_obj['position']

            #Check if this chord has a seventh
            if len(unique_notes) == 4:
                self.has_seventh = True

    def get_numeral_for_key(self, key):
        """Returns this chord's numeral relative to the given key"""

        return music_info.identify_chord_numeral_for_key(key, self.notes[self.bass_index].name, self.quality, self.position, self.has_seventh)

    def get_secondary_dominant_numeral(self, second_chord):
        """Returns this chord's numeral as a secondary dominant for the next chord, if it is one. Else, returns a blank string."""

        return music_info.identify_secondary_dominant_numeral(self.get_name(), self.position, self.has_seventh, second_chord.notes[self.bass_index].name, second_chord.quality)

    def __repr__(self):
        """Returns a simple string representation of the chord for re-creation"""

        chord_string = ""

        #Reconstruct the chord string passed to this class instance
        for _, note in enumerate(self.notes):
            chord_string += note.name + str(note.octave) + ', '
            
        #Remove the trailing comma
        return chord_string[0:-2]

    def __str__(self):
        return self.__repr__()
       
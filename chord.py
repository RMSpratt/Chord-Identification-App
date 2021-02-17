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

    def identify_chord(self):
        """Identifies this chord by setting its name and bass_index according to its bass index and chord quality."""

        interval_string, unique_notes = self.get_interval_string_info()

        #Get the dictionary object representing the chord for the chord's interval string
        chord_obj = music_info.INTERVAL_STRINGS[interval_string]

        if chord_obj['quality'] == 'unknown':
            print("Unknown : " + str(interval_string))
            self.name = 'Unknown Chord'

        else:

            chord_bass_note = ''

            if len(unique_notes) == len(self.notes):

                #Set this chord's bass note and get its name
                self.bass_index = chord_obj['bass_index']
                chord_bass_note = self.notes[self.bass_index].name

            else:
        
                chord_bass_note = unique_notes[chord_obj['bass_index']]

                for i, note in enumerate(self.notes):

                    if note.name == chord_bass_note:
                        self.bass_index = i
                        break

            self.name += chord_bass_note + chord_obj['quality']
            self.position = chord_obj['position']

            #Check if this chord has a seventh
            if len(unique_notes) == 4:
                self.has_seventh = True

    def identify_numeral_by_key(self, key):
        """Gets and returns the roman numeral for this chord relative to the passed key.
        
        This function searches through the major and minor triads or sevenths for this chord to determine its function within the passed key.
        If the chord is found within the passed key, its inversion string is also appended and returned.
        """

        chord_numeral = ''

        diatonic_chords = None
        diatonic_numerals = None
        mixture_chords = None
        mixture_numerals = None

        #Check if we're searching for a major key
        if key.upper():
            diatonic_numerals = music_info.MAJOR_KEY_NUMERALS
            mixture_numerals = music_info.MINOR_KEY_NUMERALS

            if not self.has_seventh:
                diatonic_chords = music_info.MAJOR_KEY_TRIADS
                mixture_chords = music_info.MINOR_KEY_TRIADS

            else: 
                diatonic_chords = music_info.MAJOR_KEY_SEVENTHS
                mixture_chords = music_info.MINOR_KEY_SEVENTHS

        #Else, we're searching for a minor key
        else:
            diatonic_numerals = music_info.MINOR_KEY_NUMERALS
            mixture_numerals = music_info.MAJOR_KEY_NUMERALS

            if not self.has_seventh:
                diatonic_chords = music_info.MINOR_KEY_TRIADS
                mixture_chords = music_info.MAJOR_KEY_TRIADS

            else:
                diatonic_chords = music_info.MINOR_KEY_SEVENTHS
                mixture_chords = music_info.MAJOR_KEY_SEVENTHS

        if self.name in diatonic_chords[key]:
            chord_index = diatonic_chords[key].index(self.name)
            chord_numeral = diatonic_numerals[chord_index]

        elif self.name in mixture_chords[key]:
            chord_index = mixture_chords[key].index(self.name)
            chord_numeral = mixture_numerals[chord_index]

        #Modify the chord numeral string based on the inversion of the chord
        if chord_numeral != '':

            if not self.has_seventh and self.position < 3:
                chord_numeral += music_info.INVERSION_TRIAD_STRINGS[self.position]

            else:
                chord_numeral += music_info.INVERSION_SEVENTH_STRINGS[self.position]

        return chord_numeral

    def __repr__(self):
        """Returns a simple string representation of the chord for re-creation"""

        chord_string = ""

        #Reconstruct the chord string passed to this class instance
        for _, note in enumerate(self.notes):
            chord_string += note.name + str(note.octave) + ", "
            
        #Remove the trailing comma
        return chord_string[0:-2]

    def __str__(self):
        return self.__repr__()
       
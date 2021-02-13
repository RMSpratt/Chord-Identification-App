
import musicInfo as music_info

from note import NoteFactory
from exceptions import InvalidChordError, InvalidNoteError

class Chord:
    """Class defining a chord as a set of 3-4 notes with a specific pattern of intervals between them."""

    _note_factory = NoteFactory()

    def __init__(self, chord_string):
        self.notes = []
        self.intervals = []
        self.interval_string = ""
        self.name = ''
        self.position = ''
        self.bass_index = 0

        #Parse the chord string into the set of notes for the chord
        try:    
            self.parse_chord_string(chord_string)

        except InvalidChordError as error:
            print(error.value)
            return

        except InvalidNoteError as error:
            print('An invalid note was provided for the chord: ', error.value)
            return
        
        #Calculate the intervals in semitones between the notes in the chord
        self.calculate_chord_intervals()

        #Identify the chord's position and inversion
        self.identify_chord()

    def calculate_chord_intervals(self):
        """Calculates the intervals in semitones between the notes in the chord."""
  
        self.notes.sort(key=lambda note: note['value'])

        for i in range(0, len(self.notes)-1):
            first_note = self.notes[i]['value']
            second_note = self.notes[i+1]['value']

            interval = (second_note - first_note) % 12

            self.intervals.append(interval)
            self.interval_string += str(interval)

    def get_chord_intervals(self):
        return self.intervals

    def identify_chord(self):
        """Identifies this chord by setting its name and bass_index according to its bass index and chord quality."""

        #Get the dictionary object representing the chord for the chord's interval string
        chord_obj = music_info.INTERVAL_STRINGS[self.interval_string]

        if chord_obj['quality'] == 'unknown':
            self.name = 'Unknown Chord'
            
        else:
    
            #Set this chord's bass note and get its name
            self.bass_index = chord_obj['bass_index']
            bass_note_name = self.notes[self.bass_index]['name']

            #Get the quality of this chord from the value returned
            chord_quality = chord_obj['quality']

            #Set the chord's name using its bass index and quality 
            self.name += bass_note_name + chord_quality

    def identify_numeral_by_key(self, key):
        """Gets and returns the roman numeral for this chord relative to the passed key."""

        return music_info.identify_chord_numeral_for_key(key, self.name, self.bass_index)

    def parse_chord_string(self, chord_string):
        """Parses the passed string detailing this chord's notes into its individual notes."""

        notes = chord_string.split(',')

        #If the user didn't provide enough notes for the chord, it's invalid
        if len(notes) < 3:
            raise InvalidChordError(f"Not enough notes for the chord: {chord_string}")

        for note_string in notes:
            note_string = note_string.strip()

            chord_note = self._note_factory.create_note(note_string)
            self.notes.append(chord_note)

    def print_chord_info(self):
        """Outputs this chord's name and notes used for debugging purposes."""

        chord_notes = ''

        print(f"Name: {self.name}")

        for note in self.notes:
            chord_notes += note['name'] + str(note['octave']) + " "

        print(f"Notes: {chord_notes}".strip())

    def __repr__(self):
        """Returns a simple string representation of the chord for re-creation"""

        chord_string = ""

        #Reconstruct the chord string passed to this class instance
        for _, note in enumerate(self.notes):
            chord_string += note["name"] + str(note["octave"]) + ", "
            
        #Remove the trailing comma
        return chord_string[0:-2]

    def __str__(self):
        return self.__repr__()
       
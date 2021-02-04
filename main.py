import collections
import csv
import enum

from collections import defaultdict
from enum import Enum

#Enum class defining strings for every recognized chord type in this program 
class ChordTypes(Enum):
    major = ""
    minor = "m"
    diminished = "dim"
    augmented = "aug"
    add5 = "add5"
    add5maj7 = "add5/maj7"
    sus2 = "sus2"
    sus4 = "sus4"
    major7 = "maj7"
    dominant7 = "7"
    minor7 = "min7"
    halfdim7 = "ø"
    dim7 = "dim7"



#Custom exception for catching invalid input for a chord
class InvalidChordException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return (repr(self.value))


#Custom exception for catching invalid notes input to a chord
class InvalidNoteException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return (repr(self.value))


class NoteFactory:
    """This class is responsible for parsing note strings into proper note objects for a chord."""

    #The set of possible note names recognized by the program
    _note_names = {
        "B#": 1, "C": 1, "Dbb": 1, "Bx": 2, "C#": 2, "Db": 2, "Cx": 3, "D": 3, "Ebb": 3, "D#": 4, "Eb": 4, "Fbb": 4,
        "Dx": 5, "E": 5, "Fb": 5, "E#": 6, "F": 6, "Gbb": 6, "Ex": 7, "F#": 7, "Gb": 7, "Fx": 8, "G": 8, "Abb": 8, 
        "G#": 9, "Ab": 9, "Gx": 10, "A": 10, "Bbb": 10, "A#": 11, "Bb": 11, "Cbb": 11, "B": 12, "Cb": 12
    }

    #The set of octaves a note can be defined as
    _note_octaves = [0,1,2,3,4,5,6,7]

    def calculate_note_value(self, name, octave):
        """Calculates the numerical value of a note by taking its position within an octave and multiplying by the number of octaves above C0 it is."""

        return self._note_names[name] + octave * 12

    def create_note(self, note_string):
        """This factory method creates and returns a note using the passed note string.

        Notes are created as a dictionary containing three key-value pairs:
        name - The letter name of the note, i.e. C, Db, E, A#  
        octave - The octave of the note, restricted to 0-7
        value - An integer representing the note's position on a keyboard and relative to other notes
        """

        #Parse the note into its name and octave
        note_name, note_octave = self.parse_note(note_string)

        if note_name == 'invalid':
            raise InvalidNoteException(note_string)

        else:

            #Calculate the note's numerical value based on its position on the Keyboard
            note_value = self.calculate_note_value(note_name, note_octave)

            return {
                'name': note_name,
                'octave': note_octave,
                'value': note_value
            }

    def parse_note(self, note_string):
        """Parses a given note string into its letter and octave components."""

        for j, c in enumerate(note_string):

            #Seperate the note at its octave
            if c.isdigit():
                note_name = note_string[0:j]
                note_octave = int(note_string[j])

                #Validate the parsed name and octave for the note
                if note_name in self._note_names.keys() and note_octave in self._note_octaves:
                    return (note_name, note_octave)

                else:
                    return ('invalid', -1)

        #If the note didn't have an octave indicated, it's invalid
        return ('invalid', -1)


class ChordIdentifier:

    #Dictionary holding all of the recognized interval strings comprising a chord
    chord_interval_strings = defaultdict(lambda: {'bass_index': 'unknown', 'quality': 'unknown'})

    def __init__(self):
        self.load_chord_interval_strings()

    def identify_chord(self, interval_string):
        """Returns an object identifying a chord by the passed string of its intervals."""

        return self.chord_interval_strings[interval_string]

    def load_chord_interval_strings(self):
        """This function reads in every valid combination of note intervals forming a chord defined in the chordIntervals.csv file."""
        
        try:

            with open('chordIntervals.csv', 'r') as chord_file:
                
                chord_reader = csv.reader(chord_file)
                next(chord_reader, None)

                for row in chord_reader:

                    #Rows with less than three fields should be ignored
                    if len(row) < 3:
                        continue

                    else:
                        chord_type = ''

                        #If the chord's ID and/or bass_index aren't numerical, the chord is invalid
                        if row[0].isdigit() == False or row[1].isdigit() == False:
                            continue

                        try: 

                            #If the chord's type is valid, get its string representation
                             chord_type = ChordTypes[row[2]].value

                        except KeyError:
                            continue

                        #Save the chord to the class's list of possible chords
                        self.chord_interval_strings[row[0]] = {'bass_index': int(row[1]), 'quality': chord_type}

        except FileNotFoundError:
            print('Error: The chordIntervals.csv file is missing.')


class Chord:
    """Class defining a chord as a set of 3-4 notes with a specific pattern of intervals between them."""

    _identifier = ChordIdentifier()
    _note_factory = NoteFactory()

    def __init__(self, chord_string):
        self.notes = []
        self.interval_string = ''
        self.name = ''
        self.position = ''
        self.bass_index = 0

        #Parse the chord string into the set of notes for the chord
        try:    
            self.parse_chord_string(chord_string)

        except InvalidChordException as error:
            print(error.value)
            return

        except InvalidNoteException as error:
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

            self.interval_string += str(interval)

    def identify_chord(self):
        """Identifies this chord by setting its name according to its bass index and chord quality."""

        #Get the dictionary object representing the chord for the chord's interval string
        chord_obj = self._identifier.identify_chord(self.interval_string)

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

    def __repr__(self):
        """Returns a simple string representation of the chord for re-creation"""

        chord_string = ""

        #Reconstruct the chord string passed to this class instance
        for _, chord in enumerate(self.notes):
            chord_string += (f"{chord.name}{chord.octave},")
            
        #Remove the trailing comma
        chord_string = chord_string[0:-1]

    def print_chord_info(self):
        """Outputs this chord's name and notes used for debugging purposes."""

        chord_notes = ''

        print(f"Name: {self.name}")

        for note in self.notes:
            chord_notes += note['name'] + str(note['octave']) + " "

        print(f"Notes: {chord_notes}".strip())

    def parse_chord_string(self, chord_string):
        """Parses the passed string detailing this chord's notes into its individual notes."""

        notes = chord_string.split(',')

        #If the user didn't provide enough notes for the chord, it's invalid
        if len(notes) < 3:
            raise InvalidChordException(f"Not enough notes for the chord: {chord_string}")

        for note_string in notes:
            note_string = note_string.strip()

            chord_note = self._note_factory.create_note(note_string)
            self.notes.append(chord_note)

                      

def run_main_menu():
    
    user_input = ''

    while user_input != 'q':
        print('Please enter the chord to identify or q to quit.')
        user_input = str(input('Enter each note below separated by a comma.\n\n> '))
        print('')

        if user_input == 'q':
            print('Goodbye!')
            
        else:
            test_chord = Chord(user_input)

            print("-----Chord Information-----")
            test_chord.print_chord_info()
            print("")


run_main_menu()

# test_chord = Chord("C4, E4, G4")
# test_chord2 = Chord("G#4, E5, B5")
# test_chord.print_chord_info()
# test_chord2.print_chord_info()
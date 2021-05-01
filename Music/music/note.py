'''
    This module exports the Note class with name and octave information and uses the
    NoteFactory class for the creation of notes.
'''

from .music_info import get_note_degree_in_key, get_note_accidental_in_key


class NoteFactory:
    '''This class is responsible for parsing note strings into proper note objects for a chord.'''

    #The set of possible note names recognized by the program
    _note_names = {
        'B#': 0, 'C': 0, 'Dbb': 0, 'Bx': 1, 'C#': 1, 'Db': 1, 'Cx': 2, 'D': 2, 'Ebb': 2, 'D#': 3,
        'Eb': 3, 'Fbb': 3,'Dx': 4, 'E': 4, 'Fb': 4, 'E#': 5, 'F': 5, 'Gbb': 5, 'Ex': 6, 'F#': 6,
        'Gb': 6, 'Fx': 7, 'G': 7, 'Abb': 7, 'G#': 8, 'Ab': 8, 'Gx': 9, 'A': 9, 'Bbb': 9, 'A#': 10,
        'Bb': 10, 'Cbb': 10, 'Ax': 11, 'B': 11, 'Cb': 11
    }

    #The set of octaves a note can be defined as
    _note_octaves = [0,1,2,3,4,5,6,7,8]

    def calculate_note_value(self, name, octave):
        '''Calculates the numerical value of a note by taking its position within an octave
            and multiplying by the number of octaves above C0 it is.
        '''

        return self._note_names[name] + octave * 12

    def create_note(self, note_string):
        '''This factory method creates and returns a note using the passed note string.'''

        #Parse the note into its name and octave
        note_name, note_octave = self.parse_note(note_string)

        if note_name != 'invalid':
            note_index = self._note_names[note_name]

            #Calculate the note's numerical value based on its position on the Keyboard
            note_value = self.calculate_note_value(note_name, note_octave)

        else:
            raise ValueError(note_string)

        return Note(note_name, note_octave, note_value, note_index)

    def parse_note(self, note_string):
        '''Parses a given note string into its letter and octave components.'''

        note_name = 'invalid'
        note_octave = -1

        for j, char in enumerate(note_string):

            #Seperate the note at its octave
            if char.isdigit():
                note_name = note_string[0:j]
                note_octave = int(note_string[j])
                break

        #Validate the parsed name and octave for the note
        if note_name in self._note_names.keys() and note_octave in self._note_octaves:
            return (note_name, note_octave)

        else:
            return ('invalid', -1)


class Note:
    '''Class holding all information relevant for defining a music note.
        name - The letter name of the note, i.e. C, Db, E, A#
        octave - The octave of the note, restricted to 0-7
        index - The semitone index of the note in the range C (0) -> B (11)
        value - The note's position on the keyboard using its index and octave
    '''

    def __init__(self, name, octave, value, index):
        self.name = name
        self.octave = octave
        self.value = value
        self.index = index

    def __repr__(self):
        return f'{self.name},{self.octave},{self.value},{self.index}'

    def __str__(self):
        return f'{self.name}{self.octave}'

    def get_interval(self, other_note, use_octave=False):
        '''Returns the interval between this note and the passed note.'''

        interval = 0

        if use_octave:
            interval = abs(other_note.value - self.value)
            
        else:
            interval = (other_note.index - self.index) % 12

        return interval

    def get_degree_in_key(self, key):
        '''Returns the scale degree of this note in the passed key.'''

        return get_note_degree_in_key(self.name, key)

    def get_accidental_for_key(self, key):
        '''Returns this note's accidental string in the passed key if it has one.'''

        return get_note_accidental_in_key(self.name, key)

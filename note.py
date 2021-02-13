
from exceptions import InvalidNoteError

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
            raise InvalidNoteError(note_string)

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

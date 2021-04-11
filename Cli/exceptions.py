#Custom exception for catching invalid input for a chord
class InvalidChordError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return (repr(self.value))


#Custom exception for catching invalid notes input to a chord
class InvalidNoteError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return (repr(self.value))

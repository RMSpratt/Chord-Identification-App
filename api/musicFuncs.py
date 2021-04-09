from .chord import ChordFactory

apiFactory = ChordFactory()

def analyze_chord_numerals():
    pass

def analyze_chord(notes):
    new_chord = apiFactory.create_chord(notes)

    return (new_chord.get_name())
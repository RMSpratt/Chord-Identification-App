from .chord import ChordFactory
from .chordProgression import ChordProgression

apiFactory = ChordFactory()


def analyze_chord(notes):
    new_chord = apiFactory.create_chord(notes)

    return (new_chord.get_name())


def analyze_progression(chords, key='C', validate=False):

    progression_chords = []

    if chords == None or len(chords) == 0:
        return {'error': 'NO_VALID_CHORDS'}

    #Build each chord and add it to the progression
    for chord_string in chords:
        try:
            new_chord = apiFactory.create_chord(chord_string)
            progression_chords.append(new_chord)
            
        except ValueError:
            continue
        
    if len(progression_chords) == 0:
        return {'error': 'NO_VALID_CHORDS'}

    #Create the chord progression using the gathered valid chords and the key passed
    new_progression = ChordProgression(progression_chords, key)

    #Get the names and numerals from the progression
    chord_names = new_progression.get_progression_chord_names()
    chord_numerals = new_progression.get_progression_chord_numerals()

    progression_obj = {}
    progression_obj['chords'] = []

    #Create the progression object to return
    for (name, numeral, chord) in zip(chord_names, chord_numerals, progression_chords):
        progression_obj['chords'].append({'name': name, 'numeral': numeral, 'notes': str(chord)})

    return progression_obj

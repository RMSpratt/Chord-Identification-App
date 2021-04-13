from collections import defaultdict
from enum import Enum

#Global CONST values

#An index system mapping each note's letter name to their corresponding value on a keyboard
NOTE_INDICES = {
        'B#': 0, 'C': 0, 'Dbb': 0, 'Bx': 1, 'C#': 1, 'Db': 1, 'Cx': 2, 'D': 2, 'Ebb': 2, 'D#': 3, 'Eb': 3, 'Fbb': 3,
        'Dx': 4, 'E': 4, 'Fb': 4, 'E#': 5, 'F': 5, 'Gbb': 5, 'Ex': 6, 'F#': 6, 'Gb': 6, 'Fx': 7, 'G': 7, 'Abb': 7, 
        'G#': 8, 'Ab': 8, 'Gx': 9, 'A': 9, 'Bbb': 9, 'A#': 10, 'Bb': 10, 'Cbb': 10, 'Ax': 11, 'B': 11, 'Cb': 11
}

#The lists of diatonic and modal mixture chords in a major key
MAJOR_KEY_NUMERALS = ['I','ii','iii','IV','V','vi','viio']
MAJOR_MIXTURE_NUMERALS = ['i','iio','bIII','iv','v','bVI','bVII']

#The lists of diatonic and modal mixture chords in a minor key
MINOR_KEY_NUMERALS = ['i','iio','III','iv','v','VI','VII']
MINOR_MIXTURE_NUMERALS = ['I','ii','#iii','IV','V','#vi','viio']

NUMERAL_STRINGS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

#The list of notes naturally found in every major key
MAJOR_KEY_NOTES = {
    'Cb': ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb'],
    'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'C#': ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'],
    'Db': ['Db','Eb','F','Gb','Ab','Bb','C'],
    'D': ['D','E','F#','G','A','B','C#'],
    'Eb': ['Eb','F','G','Ab','Bb','C','D'],
    'E': ['E','F#','G#','A','B','C#','D#'],
    'F': ['F','G','A','Bb','C','D','Eb'],
    'F#': ['F#','G#','A#','B','C#','D#','E#'],
    'Gb': ['Gb','Ab','Bb','Cb','Db','Eb','F'],
    'G': ['G','A','B','C','D','E','F#'],
    'Ab': ['Ab','Bb','C','Db','Eb','F','G'],
    'A': ['A','B','C#','D','E','F#','G#'],
    'Bb': ['Bb','C','D','Eb','F','G','A'],
    'B': ['B','C#','D#','E','F#','G#','A#'],
}

#The list of notes naturally found in every key
MINOR_KEY_NOTES = {
    'C': ['C','D','Eb','F','G','Ab','Bb'],
    'C#': ['C#','D#','E','F#','G#','A','B'],
    'D': ['D','E','F','G','A','Bb','C'],
    'D#': ['D#','E#','F#','G#','A#','B','C#'],
    'Eb': ['Eb','Fb','Gb','Ab','Bb','C','Db'],
    'E': ['E','F#','G','A','B','C','D'],
    'F': ['F','G','Ab','Bb','C','Db','Eb'],
    'F#': ['F#','G#','A','B','C#','D','E'],
    'G': ['G','A','Bb','C','D','Eb','F'],
    'G#': ['G#','A#','B','C#','D#','E#','F#'],
    'Ab': ['Ab','Bb','Cb','Db','Eb','Fb','Gb'],
    'A': ['A','B','C','D','E','F','G'],
    'Bb': ['Bb','C','Db','Eb','F','Gb','Ab'],
    'B': ['B','C#','D','E','F#','G','A'],
}

#The triads naturally found in every major key
MAJOR_KEY_TRIADS = {
    'C': ['C','Dm','Em','F','G','Am','Bo'],
    'C#': ['C#','D#m','E#m','F#','G#','A#m','B#o'],
    'Db': ['Db','Ebm','Fm','Gb','Ab','Bbm','Co'],
    'D': ['D','Em','F#m','G','A','Bm','C#o'],
    'Eb': ['Eb','Fm','Gm','Ab','Bb','Cm','Do'],
    'E': ['E','F#m','G#m','A','B','C#m','D#o'],
    'F': ['F','Gm','Am','Bb','C','Dm','Ebo'],
    'F#': ['F#','G#m','A#m','B','C#','D#m','E#o'],
    'Gb': ['Gb','Abm','Bbm','C','Db','Ebm','Fo'],
    'G': ['G','Am','Bm','C','D','Em','F#o'],
    'Ab': ['Ab','Bbm','Cm','Db','Eb','Fm','Go'],
    'A': ['A','Bm','C#m','D','E','F#m','G#o'],
    'Bb': ['Bb','Cm','Dm','Eb','F','Gm','Ao'],
    'B': ['B','C#m','D#m','E','F#','G#m','A#o'],
}

#The seventh chords naturally found in every major key
MAJOR_KEY_SEVENTHS = {
    'C': ['Cmaj7', 'Dm7', 'Em7', 'Fmaj7', 'G7', 'Am7', 'Bø'],
    'C#': ['C#maj7','D#m7','E#m7','F#maj7','G#7','A#m7','B#ø'],
    'Db': ['Dbmaj7','Ebm7','Fm7','Gbmaj7','Ab7','Bbm7','Cø'],
    'D': ['Dmaj7','Em7','F#m7','Gmaj7','A7','Bm7','C#ø'],
    'Eb': ['Ebmaj7','Fm7','Gm7','Abmaj7','Bb7','Cm7','Dø'],
    'E': ['Emaj7','F#m7','G#m7','Amaj7','B7','C#m7','D#ø'],
    'F': ['Fmaj7','Gm7','Am7','Bbmaj7','C7','Dm7','Eø'],
    'F#': ['F#maj7','G#m7','A#m7','Bmaj7','C#7','D#m7','E#ø'],
    'Gb': ['Gbmaj7','Abm7','Bbm7','Cmaj7','Db7','Ebm7','Fø'],
    'G': ['Gmaj7','Am7','Bm7','Cmaj7','D7','Em7','F#ø'],
    'Ab': ['Abmaj7','Bbm7','Cm7','Dbmaj7','Eb7','Fm7','Gø'],
    'A': ['Amaj7','Bm7','C#m7','Dmaj7','E7','F#m7','G#ø'],
    'Bb': ['Bbmaj7','Cm7','Dm7','Ebmaj7','F7','Gm7','Aø'],
    'B': ['Bmaj7','C#m7','D#m7','Emaj7','F#7','G#m7','A#ø'],
}

#The chords naturally found in every minor key
MINOR_KEY_TRIADS = {
    'C': ['Cm','Do','Eb','Fm','Gm','Ab','Bb'],
    'C#': ['C#m','D#o','E','F#m','G#m','A','B'],
    'D': ['Dm','Eo','F','Gm','Am','Bb','C'],
    'D#': ['D#m','Eo','F#','G#m','A#m','B#','C#'],
    'Eb': ['Ebm','Fbo','Gb','Abm','Bbm','C','Db'],
    'E': ['Em','F#o','G','Am','Bm','C','D'],
    'F': ['Fm','Go','Ab','Bbm','Cm','Db','Eb'],
    'F#': ['F#m','G#o','A','Bm','C#m','D','E'],
    'G': ['Gm','Ao','Bb','Cm','Dm','Eb','F'],
    'G#': ['G#m','A#o','B','C#m','D#m','E#','F#'],
    'Ab': ['Abm','Bbo','Cb','Dbm','Ebm','Fb','Gb'],
    'A': ['Am','Bo','C','Dm','Em','F','G'],
    'Bb': ['Bbm','Co','Db','Ebm','Fm','Gb','Ab'],
    'B': ['Bm','C#o','D','Em','F#m','G','A'],
}

#The seventh chords naturally found in every minor key including the leading tone diminished seventh chord
MINOR_KEY_SEVENTHS = {
    'C': ['Cm7','Do7','Ebmaj7','Fm','Gm','Abmaj7','Bb7','Bo7'],
    'C#': ['C#m7','D#o7','Emaj7','F#m7','G#m7','Amaj7','B7','B#o7'],
    'D': ['Dm7','Eo7','Fmaj7','Gm7','Am7','Bbmaj7','C7','C#o7'],
    'D#': ['D#m7','Eo7','F#maj7','G#m7','A#m7','B#maj7','C#7','Cxo7'],
    'Eb': ['Ebm7','Fbo7','Gbmaj7','Abm7','Bbm7','Cmaj7','Db7','Do7'],
    'E': ['Em7','F#o7','Gmaj7','Am7','Bm7','Cmaj7','D7','D#o7'],
    'F': ['Fm7','Go7','Abmaj7','Bbm7','Cm7','Dbmaj7','Eb7','Eo7'],
    'F#': ['F#m7','G#o7','Amaj7','Bm7','C#m7','Dmaj7','E7','E#o7'],
    'G': ['Gm7','Ao7','Bbmaj7','Cm7','Dm7','Ebmaj7','F7','F#o7'],
    'G#': ['G#m7','A#o7','Bmaj7','C#m7','D#m7','E#maj7','F#7','Fxo7'],
    'Ab': ['Abm7','Bbo7','Cbmaj7','Dbm7','Ebm7','Fbmaj7','Gb7','Go7'],
    'A': ['Am7','Bo7','Cmaj7','Dm7','Em7','Fmaj7','G7','G#o7'],
    'Bb': ['Bbm7','Co7','Dbmaj7','Ebm7','Fm7','Gbmaj7','Ab7','Ao7'],
    'B': ['Bm7','C#o7','Dmaj7','Em7','F#m7','Gmaj7','A7','A#o7'],
}

INVERSION_TRIAD_STRINGS = ['','6','6/4']
INVERSION_SEVENTH_STRINGS = ['7','6/5','4/3','4/2']

#The mapping of interval strings to a matching chord quality and chord inversion
INTERVAL_STRINGS = defaultdict(lambda: {'bass_index': 'unknown', 'quality': 'unknown'})
INTERVAL_STRINGS.update(
    {
        '3': {'bass_index': 0, 'quality': 'm', 'position': 0},
        '4': {'bass_index': 0, 'quality': '', 'position': 0},
        '5': {'bass_index': 1, 'quality': 'add5', 'position': 0},
        '7': {'bass_index': 0, 'quality': 'add5', 'position': 0},
        '8': {'bass_index': 1, 'quality': '', 'position': 1},
        '9': {'bass_index': 2, 'quality': 'm', 'position': 1},
        '33': {'bass_index': 0, 'quality': 'o', 'position': 0},
        '34': {'bass_index': 0, 'quality': 'm', 'position': 0},
        '35': {'bass_index': 2, 'quality': '', 'position': 1},
        '36': {'bass_index': 2, 'quality': 'o', 'position': 1},
        '43': {'bass_index': 0, 'quality': '', 'position': 0},
        '44': {'bass_index': 0, 'quality': '+', 'position': 0},
        '45': {'bass_index': 2, 'quality': 'm', 'position': 1},
        '53': {'bass_index': 1, 'quality': 'm', 'position': 2},
        '54': {'bass_index': 1, 'quality': '', 'position': 2},
        '63': {'bass_index': 1, 'quality': 'o', 'position': 2},
        '69': {'bass_index': 0, 'quality': 'o', 'position': 0},
        '78': {'bass_index': 0, 'quality': 'm', 'position': 0},
        '79': {'bass_index': 0, 'quality': '', 'position': 0},
        '87': {'bass_index': 1, 'quality': '', 'position': 1},
        '88': {'bass_index': 1, 'quality': '+', 'position': 1},
        '89': {'bass_index': 2, 'quality': 'm', 'position': 2},
        '96': {'bass_index': 1, 'quality': 'o', 'position': 1},
        '97': {'bass_index': 1, 'quality': 'm', 'position': 1},
        '98': {'bass_index': 2, 'quality': '', 'position': 2},
        '99': {'bass_index': 2, 'quality': 'o', 'position': 2},
        '14': {'bass_index': 1, 'quality': 'maj7', 'position': 3},
        '17': {'bass_index': 1, 'quality': 'add5/maj7', 'position': 0},
        '23': {'bass_index': 1, 'quality': 'm7', 'position': 3},
        '24': {'bass_index': 1, 'quality': '7', 'position': 3},
        '37': {'bass_index': 0, 'quality': 'm7', 'position': 0},
        '41': {'bass_index': 2, 'quality': 'add5/maj7', 'position': 0},
        '46': {'bass_index': 0, 'quality': '7', 'position': 0},
        '47': {'bass_index': 0, 'quality': 'maj7', 'position': 0},
        '58': {'bass_index': 2, 'quality': 'maj7', 'position': 3},
        '59': {'bass_index': 2, 'quality': 'm7', 'position': 3},
        '62': {'bass_index': 2, 'quality': '7', 'position': 1},
        '68': {'bass_index': 2, 'quality': 'maj7', 'position': 3},
        '71': {'bass_index': 2, 'quality': 'maj7', 'position': 1},
        '72': {'bass_index': 2, 'quality': 'm7', 'position': 1},
        '74': {'bass_index': 0, 'quality': 'add5/maj7', 'position': 0},
        '105': {'bass_index': 0, 'quality': 'm7', 'position': 0},
        '106': {'bass_index': 0, 'quality': '7', 'position': 0},
        '115': {'bass_index': 0, 'quality': 'maj7', 'position': 0},
        '118': {'bass_index': 0, 'quality': 'add5/maj7', 'position': 0},
        '143': {'bass_index': 1, 'quality': 'maj7', 'position': 3},
        '179': {'bass_index': 1, 'quality': 'maj7', 'position': 3},
        '233': {'bass_index': 1, 'quality': 'ø', 'position': 3},
        '234': {'bass_index': 1, 'quality': 'm7', 'position': 3},
        '243': {'bass_index': 1, 'quality': '7', 'position': 3},
        '269': {'bass_index': 1, 'quality': 'ø', 'position': 3},
        '278': {'bass_index': 1, 'quality': 'm7', 'position': 3},
        '279': {'bass_index': 1, 'quality': '7', 'position': 3},
        '323': {'bass_index': 2, 'quality': 'm7', 'position': 2},
        '324': {'bass_index': 2, 'quality': '7', 'position': 2},
        '332': {'bass_index': 3, 'quality': '7', 'position': 1},
        '333': {'bass_index': 0, 'quality': 'o7', 'position': 0},
        '334': {'bass_index': 0, 'quality': 'ø', 'position': 0},
        '341': {'bass_index': 3, 'quality': 'maj7', 'position': 1},
        '342': {'bass_index': 3, 'quality': 'ø', 'position': 1},
        '343': {'bass_index': 0, 'quality': 'm7', 'position': 0},
        '359': {'bass_index': 3, 'quality': 'm7', 'position': 2},
        '368': {'bass_index': 3, 'quality': '7', 'position': 2},
        '369': {'bass_index': 0, 'quality': 'o7', 'position': 0},
        '378': {'bass_index': 0, 'quality': 'ø', 'position': 0},
        '379': {'bass_index': 0, 'quality': 'm7', 'position': 0},
        '414': {'bass_index': 2, 'quality': 'maj7', 'position': 2},
        '423': {'bass_index': 2, 'quality': 'ø', 'position': 2},
        '432': {'bass_index': 3, 'quality': 'm7', 'position': 1},
        '433': {'bass_index': 0, 'quality': '7', 'position': 0},
        '434': {'bass_index': 0, 'quality': 'maj7', 'position': 0},
        '453': {'bass_index': 3, 'quality': 'maj7', 'position': 2},
        '459': {'bass_index': 3, 'quality': 'ø', 'position': 2},
        '469': {'bass_index': 0, 'quality': '7', 'position': 0},
        '478': {'bass_index': 0, 'quality': 'maj7', 'position': 0},
        '535': {'bass_index': 3, 'quality': 'maj7', 'position': 1},
        '536': {'bass_index': 3, 'quality': 'ø', 'position': 3},
        '537': {'bass_index': 1, 'quality': 'm7', 'position': 2},
        '545': {'bass_index': 3, 'quality': 'm7', 'position': 3},
        '546': {'bass_index': 1, 'quality': '7', 'position': 2},
        '547': {'bass_index': 1, 'quality': 'maj7', 'position': 2},
        '574': {'bass_index': 1, 'quality': 'maj7', 'position': 2},
        '587': {'bass_index': 2, 'quality': 'maj7', 'position': 3},
        '596': {'bass_index': 2, 'quality': 'ø', 'position': 3},
        '597': {'bass_index': 2, 'quality': 'm7', 'position': 3},
        '627': {'bass_index': 2, 'quality': '7', 'position': 1},
        '635': {'bass_index': 3, 'quality': '7', 'position': 3},
        '636': {'bass_index': 0, 'quality': 'o7', 'position': 0},
        '637': {'bass_index': 1, 'quality': 'ø', 'position': 2},
        '645': {'bass_index': 0, 'quality': 'ø', 'position': 0},
        '687': {'bass_index': 2, 'quality': '7', 'position': 3},
        '695': {'bass_index': 3, 'quality': '7', 'position': 1},
        '696': {'bass_index': 0, 'quality': 'o7', 'position': -1},
        '697': {'bass_index': 0, 'quality': 'ø', 'position': 0},
        '711': {'bass_index': 1, 'quality': 'add5/maj7', 'position': 0},
        '714': {'bass_index': 2, 'quality': 'maj7', 'position': 1},
        '717': {'bass_index': 2, 'quality': 'maj7', 'position': 1},
        '726': {'bass_index': 2, 'quality': 'ø', 'position': 1},
        '727': {'bass_index': 2, 'quality': 'm7', 'position': 1},
        '735': {'bass_index': 0, 'quality': 'm7', 'position': 0},
        '736': {'bass_index': 0, 'quality': '7', 'position': 0},
        '745': {'bass_index': 0, 'quality': 'maj7', 'position': 0},
        '785': {'bass_index': 3, 'quality': 'maj7', 'position': 1},
        '786': {'bass_index': 3, 'quality': 'ø', 'position': 1},
        '787': {'bass_index': 0, 'quality': 'm7', 'position': 0},
        '795': {'bass_index': 3, 'quality': 'm7', 'position': 1},
        '796': {'bass_index': 0, 'quality': '7', 'position': 0},
        '797': {'bass_index': 0, 'quality': 'maj7', 'position': 0},
        '810': {'bass_index': 1, 'quality': '7', 'position': 1},
        '811': {'bass_index': 1, 'quality': 'maj7', 'position': 1},
        '854': {'bass_index': 2, 'quality': 'maj7', 'position': 3},
        '863': {'bass_index': 2, 'quality': 'ø', 'position': 3},
        '872': {'bass_index': 3, 'quality': 'm7', 'position': 2},
        '873': {'bass_index': 1, 'quality': '7', 'position': 1},
        '874': {'bass_index': 1, 'quality': 'maj7', 'position': 1},
        '898': {'bass_index': 3, 'quality': 'maj7', 'position': 3},
        '910': {'bass_index': 1, 'quality': 'm7', 'position': 1},
        '953': {'bass_index': 2, 'quality': 'm7', 'position': 3},
        '954': {'bass_index': 2, 'quality': '7', 'position': 3},
        '958': {'bass_index': 3, 'quality': '7', 'position': 3},
        '962': {'bass_index': 3, 'quality': '7', 'position': 2},
        '963': {'bass_index': 0, 'quality': 'o7', 'position': 0},
        '964': {'bass_index': 1, 'quality': 'ø', 'position': 1},
        '971': {'bass_index': 3, 'quality': 'maj7', 'position': 2},
        '972': {'bass_index': 3, 'quality': 'ø', 'position': 2},
        '973': {'bass_index': 1, 'quality': 'm7', 'position': 1},
        '989': {'bass_index': 3, 'quality': 'm7', 'position': 3},
        '999': {'bass_index': 0, 'quality': 'o7', 'position': 0},
        '1053': {'bass_index': 0, 'quality': 'ø', 'position': 0},
        '1054': {'bass_index': 0, 'quality': 'm7', 'position': 0},
        '1063': {'bass_index': 0, 'quality': '7', 'position': 0},
        '1089': {'bass_index': 0, 'quality': 'ø', 'position': 0},
        '1098': {'bass_index': 0, 'quality': 'm7', 'position': 0},
        '1099': {'bass_index': 0, 'quality': '7', 'position': 0},
        '1153': {'bass_index': 0, 'quality': 'maj7', 'position': 0},
        '1189': {'bass_index': 0, 'quality': 'maj7', 'position': 0},
        '3510': {'bass_index': 2, 'quality': '7', 'position': 1},
        '3511': {'bass_index': 2, 'quality': 'maj7', 'position': 1},
        '3610': {'bass_index': 2, 'quality': 'ø', 'position': 1},
        '4510': {'bass_index': 2, 'quality': 'm7', 'position': 1},
        '5105': {'bass_index': 1, 'quality': 'm7', 'position': 2},
        '5106': {'bass_index': 1, 'quality': '7', 'position': 2},
        '5115': {'bass_index': 1, 'quality': 'maj7', 'position': 2},
        '6105': {'bass_index': 1, 'quality': 'ø', 'position': 2},
        '8109': {'bass_index': 1, 'quality': '7', 'position': 1},
        '8118': {'bass_index': 1, 'quality': 'maj7', 'position': 1},
        '8910': {'bass_index': 2, 'quality': 'm7', 'position': 2},
        '9108': {'bass_index': 1, 'quality': 'ø', 'position': 1},
        '9109': {'bass_index': 1, 'quality': 'm7', 'position': 1},
        '9311': {'bass_index': 2, 'quality': 'maj7', 'position': 2},
        '9810': {'bass_index': 2, 'quality': '7', 'position': 2},
        '9910': {'bass_index': 2, 'quality': 'ø', 'position': 2},
    }
)


#Enum class defining strings for every recognized chord type in this program 
class ChordTypes(Enum):
    major = ""
    minor = "m"
    diminished = "o"
    augmented = "+"
    add5 = "add5"
    add5maj7 = "add5/maj7"
    sus2 = "sus2"
    sus4 = "sus4"
    major7 = "maj7"
    dominant7 = "7"
    minor7 = "m7"
    halfdim7 = "ø"
    dim7 = "o7"


#### PUBLIC METHODS ####
def get_chord_relation_for_key(key, numeral):
    """Returns the relation of a chord with the given numeral relative to the given key."""

    #If the numeral has a slash, it indicates an applied chord
    if '/' in numeral:
        return 'applied'

    #Check for the numeral relative to a major key
    if key[0].isupper():

        if numeral in MAJOR_KEY_NUMERALS[key]:
            return 'diatonic'

        elif numeral in MINOR_KEY_NUMERALS[key]:
            return 'mixture'

        else:
            return 'chromatic'

    #Check for the numeral relative to a minor key
    else:

        if numeral in MINOR_KEY_NUMERALS[key]:
            return 'diatonic'

        elif numeral in MAJOR_KEY_NUMERALS[key]:
            return 'mixture'

        else: 
            return 'chromatic'

        
def get_chord_for_intervals(interval_string):
    """Returns a chord's identification based on its intervals"""
    return INTERVAL_STRINGS[interval_string]


def get_key_note_for_degree(key, degree):
    """Returns the name of the note at the specified scale degree within the passed key."""
    
    if (key[0].isupper()):
        return MAJOR_KEY_NOTES[key][degree]

    else:
        key = key[0].upper() + key[1:]
        return MINOR_KEY_NOTES[key][degree]


def get_leading_tone_in_key(key):
    """Returns the leading tone for the passed key whether major or minor."""
    key = key[0].upper() + key[1:]

    return MAJOR_KEY_NOTES[key][6]


def get_note_accidental_in_key(search_name, key):
    """Searches for the given note in the passed key and returns its accidental string if it doesn't exist within the key."""
    
    accidental_strings = ['bb', 'b', 'n', '#', 'x']
    accidental_index = 0
   
    #Get the notes for the passed key
    if (key[0].isupper()):
        key_notes = MAJOR_KEY_NOTES[key]

    else:
        key = key[0].upper() + key[1:]
        key_notes = MINOR_KEY_NOTES[key]

    #Search for the note by its letter name in the passed key
    for note_name in key_notes:

        #Get the index of the note being searched for and the note as it appears in the key, i.e. C = 0, C# = 1, Cx = 2
        if note_name[0] == search_name[0]:
            key_note_index = NOTE_INDICES[note_name]
            key_note_name = note_name
            search_note_index = NOTE_INDICES[search_name]

    #Get the sign of the note as it normally appears in the key
    if 'bb' in key_note_name: 
        accidental_index = 0

    elif 'b' in key_note_name:
        accidental_index = 1

    elif '#' in key_note_name:
        accidental_index = 3

    elif 'x' in key_note_name:
        accidental_index = 4

    #No sign indicates the note is natural, no sharp(s) or flat(s)
    else:
        accidental_index = 2

    #Return the appropriate accidental string for the note
    if search_note_index == key_note_index + 2 or search_note_index == key_note_index - 10:
        return accidental_strings[accidental_index + 2]

    elif search_note_index == key_note_index + 1 or search_note_index == key_note_index - 11:
        return accidental_strings[accidental_index + 1]

    elif search_note_index == key_note_index - 1 or search_note_index == key_note_index + 11:
        return accidental_strings[accidental_index - 1]
 
    elif search_note_index == key_note_index - 2 or search_note_index == key_note_index + 10:
        return accidental_strings[accidental_index - 2]

    else:
        return ''


def get_note_degree_in_key(name, key):
    """Searches for the given note in the passed key and returns the index where it occurs or -1 if it doesn't exist within the key."""

    if (key[0].isupper()):
        key_notes = MAJOR_KEY_NOTES[key]

    else:
        key = key[0].upper() + key[1:]
        key_notes = MINOR_KEY_NOTES[key]

    #Search for the note in the key and return the matching note's index
    for i, note_name in enumerate(key_notes):

        if note_name == name:
            return i

    return -1


def identify_chord_numeral_for_key(key, bass_note, quality, position, has_seventh=False, get_inversion=True):
    """Gets and returns the roman numeral for this chord relative to the passed key.
    
    This function searches through the major and minor triads or sevenths for this chord to determine its function within the passed key.
    If the chord is found within the passed key, and get_inversion == True, the inversion string is appended to the numeral.
    """

    chord_numeral = ''
    note_index_in_key = 0

    key_diatonic_notes = None


    #1) Get the notes for the appropriate key to search through
    if key[0].isupper():
        key_diatonic_notes = MAJOR_KEY_NOTES[key]

    else:
        key = key[0].upper() + key[1:]
        key_diatonic_notes = MINOR_KEY_NOTES[key]

    #If the note is diatonic to the key, get the appropriate numeral by index
    if bass_note in key_diatonic_notes:
        note_index_in_key = key_diatonic_notes.index(bass_note)
        chord_numeral = NUMERAL_STRINGS[note_index_in_key]
        
    #If the note is not diatonic to the key, determine its altered numeral
    else:

        #Extract the note name from the passed bass_note, i.e. Bbb --> B, C# --> C
        bass_note_name = bass_note[0]

        diatonic_note_index = 0
        diatonic_note_value = 0
        chromatic_note_value = NOTE_INDICES[bass_note]

        #Search for the stripped note_name in the key's notes
        for i, note in enumerate(key_diatonic_notes):

            if bass_note_name == note[0]:
                diatonic_note_index = i
                diatonic_note_value = NOTE_INDICES[note]
                break

        #Chromatic note uses a raised (sharp) note
        if chromatic_note_value == diatonic_note_value + 1:
            chord_numeral = f'#{NUMERAL_STRINGS[diatonic_note_index]}'

        #Chromatic note uses a raised (double sharp) note
        elif chromatic_note_value == diatonic_note_value + 2:
            chord_numeral = f'x{NUMERAL_STRINGS[diatonic_note_index]}'

        #Chromatic note uses a lowered (flat) note
        elif chromatic_note_value == diatonic_note_value - 1:
            chord_numeral = f'b{NUMERAL_STRINGS[diatonic_note_index]}'

        #Chromatic note uses a lowered (double flat) note
        else:
            chord_numeral = f'bb{NUMERAL_STRINGS[diatonic_note_index]}'

    #2) Adjust the numeral based on chord quality if necessary
    if quality == '+':
        chord_numeral += '+'

    elif quality == 'maj7':
        chord_numeral += 'M'

    elif quality in ['m', 'm7', 'ø', 'o', 'o7']:
        chord_numeral = chord_numeral.lower()
    
        if quality == 'ø':
            chord_numeral += 'ø'

        elif quality == 'o' or quality == 'o7':
            chord_numeral += 'o'

    #3) Append the appropriate inversion string to the numeral if requested
    if get_inversion:

        if has_seventh:
            chord_numeral += INVERSION_SEVENTH_STRINGS[position]

        else:
            chord_numeral += INVERSION_TRIAD_STRINGS[position]

    return chord_numeral


def identify_chord_type_by_key(key, bass_note, quality, has_seventh):
    """Function to return the relationship of the passed chord (described by bass_note, quality, and seventh) and the passed key."""

    diatonic_chords = None
    mixture_chords = None

    chord_name = f'{bass_note}{quality}'

    #Check if we're searching for a major key
    if key[0].isupper():

        if not has_seventh:
            diatonic_chords = MAJOR_KEY_TRIADS
            mixture_chords = MINOR_KEY_TRIADS

        else: 
            diatonic_chords = MAJOR_KEY_SEVENTHS
            mixture_chords = MINOR_KEY_SEVENTHS

    #Else, we're searching for a minor key
    else:

        if not has_seventh:
            diatonic_chords = MINOR_KEY_TRIADS
            mixture_chords = MAJOR_KEY_TRIADS

        else:
            diatonic_chords = MINOR_KEY_SEVENTHS
            mixture_chords = MAJOR_KEY_SEVENTHS

    if chord_name in diatonic_chords[key]:
        return 'diatonic'

    elif chord_name in mixture_chords[key]:
        return 'mixture'

    else: 
        return 'other'


def identify_secondary_dominant_numeral(applied_chord_name, applied_chord_position, applied_chord_has_seventh, base_chord_key, base_chord_quality):
    """Identifies and returns the numeral for the applied chord if it is an applied dominant to the base chord."""

    applied_dominant_numeral = ''

    #Fully-diminished applied-dominant seventh chords are a special case, inversions must be checked for
    if 'o7' in applied_chord_name:

        diminished_numeral = identify_chord_numeral_for_key(base_chord_key, applied_chord_name[0:-2], 'o7', 0, True)

        if diminished_numeral == 'bvio7':
            applied_dominant_numeral = 'viio4/2'

        elif diminished_numeral == 'ivo7':
            applied_dominant_numeral = 'viio4/3'

        elif diminished_numeral == 'iio7':
            applied_dominant_numeral = 'viio6/5'

        elif diminished_numeral == 'viio7':
            applied_dominant_numeral = diminished_numeral

        return applied_dominant_numeral

    else:

        #Only major and minor chords can have an applied dominant
        if base_chord_quality in ['','m','maj7','7','m7']:

            if applied_chord_has_seventh:
                base_major_chords = MAJOR_KEY_SEVENTHS[base_chord_key]
                base_minor_chords = MINOR_KEY_SEVENTHS[base_chord_key]

                #Check if the applied chord is V7 in some form
                if applied_chord_name == base_major_chords[4]:
                    applied_dominant_numeral += MAJOR_KEY_NUMERALS[4]

                #Check if the applied chord is viiø in some form (special case requiring altered numeral)
                elif applied_chord_name == base_major_chords[6]:
                    applied_dominant_numeral += 'viiø'

                #Check if the applied chord is viio7 in some form
                elif applied_chord_name == base_minor_chords[7]:
                    applied_dominant_numeral += base_minor_chords[6]

            else:
                base_major_chords = MAJOR_KEY_TRIADS[base_chord_key]
                base_minor_chords = MINOR_KEY_TRIADS[base_chord_key]

                #Check if the applied chord is V in root position (exclusive)
                if applied_chord_name == base_major_chords[4] and applied_chord_position == 0:
                    applied_dominant_numeral += MAJOR_KEY_NUMERALS[4]

                #Check if the applied chord is viio in root position (exclusive)
                elif applied_chord_name == base_major_chords[6] and applied_chord_position == 0:
                    applied_dominant_numeral += MAJOR_KEY_NUMERALS[6]


    #If the chord was a applied dominant, get its inversion string
    if applied_dominant_numeral != '':

        if applied_chord_has_seventh:
            applied_dominant_numeral += INVERSION_SEVENTH_STRINGS[applied_chord_position]
        
        else:
            applied_dominant_numeral += INVERSION_TRIAD_STRINGS[applied_chord_position]

    return applied_dominant_numeral

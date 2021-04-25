'''
This module holds a series of constant values and functions used for calculating properties of
notes and chords according to musical notation rules. 
'''

from collections import defaultdict

#CONST file-scope values

#The common accidentals that can precede a note
ACCIDENTAL_STRINGS = ['bb', 'b', 'n', '#', 'x']

#A mapping of chords of a certain quality to a string that decorates their numeral
CHORD_QUALITY_STRINGS = defaultdict(lambda: '')
CHORD_QUALITY_STRINGS.update({
    'o': 'o',
    '+': '+',
    'sus2': 'sus2',
    'sus4': 'sus4',
    'b5': 'b5',
    'maj7': 'M',
    'mM7': 'M7',
    'm7': '',
    'ø': 'ø',
    'o7': 'o',
    '7b5': '7b5'
})

#Chord inversion strings to decorate a chord numeral
INVERSION_TRIAD_STRINGS = ['','6','6/4']
INVERSION_SEVENTH_STRINGS = ['7','6/5','4/3','4/2']

#Index system mapping each note's letter name to a value based on the 12 semitones in an octave
NOTE_INDICES = {
    'B#': 0, 'C': 0, 'Dbb': 0, 'Bx': 1, 'C#': 1, 'Db': 1, 'Cx': 2, 'D': 2, 'Ebb': 2, 'D#': 3,
    'Eb': 3, 'Fbb': 3,'Dx': 4, 'E': 4, 'Fb': 4, 'E#': 5, 'F': 5, 'Gbb': 5, 'Ex': 6, 'F#': 6,
    'Gb': 6, 'Fx': 7, 'G': 7, 'Abb': 7, 'G#': 8, 'Ab': 8, 'Gx': 9, 'A': 9, 'Bbb': 9, 'A#': 10,
    'Bb': 10, 'Cbb': 10, 'Ax': 11, 'B': 11, 'Cb': 11
}

#The numeral strings used for denoting chords without decorations
NUMERAL_STRINGS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

#The lists of diatonic and modal mixture chord numerals in a major key
MAJOR_KEY_NUMERALS = [
    'I','ii','iii','IV','V','vi','viio','IM7','ii7','iiim7','IVM7','V7','vi7','viiø','viio7'
]

MAJOR_MIXTURE_NUMERALS = [
    'i','iio','bIII','iv','v','bVI','bVII','i7','iiø','bIIIM7','iv7','v7','bVIM7','bVII7'
]

#The lists of diatonic and modal mixture chord numerals in a minor key
MINOR_KEY_NUMERALS = [
    'i','iio','III','iv','v','VI','VII','i7','iiø','IIIM7','iv7','v7','VIM7','VII7'
]

MINOR_MIXTURE_NUMERALS = [
    'I','ii','#iii','IV','V','#vi','viio','IM7','ii7','#iii7','IVM7','V7','#vi7','viiø', 'viio7'
]

#The list of notes naturally found in a series of major scales
MAJOR_KEY_NOTES = {
    'Cb': ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb'],
    'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'C#': ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'],
    'Db': ['Db','Eb','F','Gb','Ab','Bb','C'],
    'D': ['D','E','F#','G','A','B','C#'],
    'D#': ['D#','E#','Fx','G#','A#','B#','Cx'],
    'Eb': ['Eb','F','G','Ab','Bb','C','D'],
    'E': ['E','F#','G#','A','B','C#','D#'],
    'F': ['F','G','A','Bb','C','D','E'],
    'F#': ['F#','G#','A#','B','C#','D#','E#'],
    'Gb': ['Gb','Ab','Bb','Cb','Db','Eb','F'],
    'G': ['G','A','B','C','D','E','F#'],
    'G#': ['G#','A#','B#','C#','D#','E#','Fx'],
    'Ab': ['Ab','Bb','C','Db','Eb','F','G'],
    'A': ['A','B','C#','D','E','F#','G#'],
    'A#': ['A#','B#','Cx','D#','E#','Fx','Gx'],
    'Bb': ['Bb','C','D','Eb','F','G','A'],
    'B': ['B','C#','D#','E','F#','G#','A#'],
}

#The list of notes naturally found in a series of minor scales
MINOR_KEY_NOTES = {
    'Cb': ['Db','Ebb','Fb','Gb','Abb','Bbb','Cb'],
    'C': ['C','D','Eb','F','G','Ab','Bb'],
    'C#': ['C#','D#','E','F#','G#','A','B'],
    'Db': ['Db','Eb','Fb','Gb','Ab','Bbb','Cb'],
    'D': ['D','E','F','G','A','Bb','C'],
    'D#': ['D#','E#','F#','G#','A#','B','C#'],
    'Eb': ['Eb','Fb','Gb','Ab','Bb','Cb','Db'],
    'E': ['E','F#','G','A','B','C','D'],
    'F': ['F','G','Ab','Bb','C','Db','Eb'],
    'F#': ['F#','G#','A','B','C#','D','E'],
    'Gb': ['Db','Ebb','Fb','Gb','Ab','Bbb','Cb'],
    'G': ['G','A','Bb','C','D','Eb','F'],
    'G#': ['G#','A#','B','C#','D#','E','F#'],
    'Ab': ['Ab','Bb','Cb','Db','Eb','Fb','Gb'],
    'A': ['A','B','C','D','E','F','G'],
    'A#': ['A#','B#','C#','D#','E#','F#','G#'],
    'Bb': ['Bb','C','Db','Eb','F','Gb','Ab'],
    'B': ['B','C#','D','E','F#','G','A'],
}

#The mapping of interval strings to a matching chord quality and chord inversion
INTERVAL_STRINGS = defaultdict(lambda: {'root_index': 0, 'quality': 'unknown', 'position': 0})
INTERVAL_STRINGS.update({
   '3': {'root_index': 0, 'quality': 'm', 'position': 0},
    '4': {'root_index': 0, 'quality': '', 'position': 0},
    '5': {'root_index': 1, 'quality': 'add5', 'position': 0},
    '7': {'root_index': 0, 'quality': 'add5', 'position': 0},
    '8': {'root_index': 1, 'quality': '', 'position': 1},
    '9': {'root_index': 2, 'quality': 'm', 'position': 1},
    '25': {'root_index': 0, 'quality': 'sus2', 'position': 0},
    '26': {'root_index': 2, 'quality': 'b5', 'position': 1},
    '33': {'root_index': 0, 'quality': 'o', 'position': 0},
    '34': {'root_index': 0, 'quality': 'm', 'position': 0},
    '35': {'root_index': 2, 'quality': '', 'position': 1},
    '36': {'root_index': 2, 'quality': 'o', 'position': 1},
    '42': {'root_index': 0, 'quality': 'b5', 'position': 0},
    '43': {'root_index': 0, 'quality': '', 'position': 0},
    '44': {'root_index': 0, 'quality': '+', 'position': 0},
    '45': {'root_index': 2, 'quality': 'm', 'position': 1},
    '53': {'root_index': 1, 'quality': 'm', 'position': 2},
    '52': {'root_index': 0, 'quality': 'sus4', 'position': 0},
    '54': {'root_index': 1, 'quality': '', 'position': 2},
    '63': {'root_index': 1, 'quality': 'o', 'position': 2},
    '64': {'root_index': 1, 'quality': 'b5', 'position': 2},
    '69': {'root_index': 0, 'quality': 'o', 'position': 0},
    '78': {'root_index': 0, 'quality': 'm', 'position': 0},
    '79': {'root_index': 0, 'quality': '', 'position': 0},
    '86': {'root_index': 1, 'quality': 'b5', 'position': 1},
    '87': {'root_index': 1, 'quality': '', 'position': 1},
    '88': {'root_index': 1, 'quality': '+', 'position': 1},
    '89': {'root_index': 2, 'quality': 'm', 'position': 2},
    '96': {'root_index': 1, 'quality': 'o', 'position': 1},
    '97': {'root_index': 1, 'quality': 'm', 'position': 1},
    '98': {'root_index': 2, 'quality': '', 'position': 2},
    '99': {'root_index': 2, 'quality': 'o', 'position': 2},
    '108': {'root_index': 2, 'quality': 'b5', 'position': 2},
    '610': {'root_index': 0, 'quality': 'b5', 'position': 0},
    '14': {'root_index': 1, 'quality': 'maj7', 'position': 3},
    '17': {'root_index': 1, 'quality': 'add5/maj7', 'position': 0},
    '23': {'root_index': 1, 'quality': 'm7', 'position': 3},
    '24': {'root_index': 1, 'quality': '7', 'position': 3},
    '37': {'root_index': 0, 'quality': 'm7', 'position': 0},
    '41': {'root_index': 2, 'quality': 'add5/maj7', 'position': 0},
    '46': {'root_index': 0, 'quality': '7', 'position': 0},
    '47': {'root_index': 0, 'quality': 'maj7', 'position': 0},
    '58': {'root_index': 2, 'quality': 'maj7', 'position': 3},
    '59': {'root_index': 2, 'quality': 'm7', 'position': 3},
    '62': {'root_index': 2, 'quality': '7', 'position': 1},
    '68': {'root_index': 2, 'quality': '7', 'position': 3},
    '71': {'root_index': 2, 'quality': 'maj7', 'position': 1},
    '72': {'root_index': 2, 'quality': 'm7', 'position': 1},
    '74': {'root_index': 0, 'quality': 'add5/maj7', 'position': 0},
    '105': {'root_index': 0, 'quality': 'm7', 'position': 0},
    '106': {'root_index': 0, 'quality': '7', 'position': 0},
    '115': {'root_index': 0, 'quality': 'maj7', 'position': 0},
    '118': {'root_index': 0, 'quality': 'add5/maj7', 'position': 0},
    '134': {'root_index': 1, 'quality': 'mM7', 'position': 3},
    '143': {'root_index': 1, 'quality': 'maj7', 'position': 3},
    '178': {'root_index': 1, 'quality': 'mM7', 'position': 3},
    '179': {'root_index': 1, 'quality': 'maj7', 'position': 3},
    '233': {'root_index': 1, 'quality': 'ø', 'position': 3},
    '234': {'root_index': 1, 'quality': 'm7', 'position': 3},
    '242': {'root_index': 3, 'quality': '7b5', 'position': 1},
    '243': {'root_index': 1, 'quality': '7', 'position': 3},
    '269': {'root_index': 1, 'quality': 'ø', 'position': 3},
    '278': {'root_index': 1, 'quality': 'm7', 'position': 3},
    '279': {'root_index': 1, 'quality': '7', 'position': 3},
    '323': {'root_index': 2, 'quality': 'm7', 'position': 2},
    '324': {'root_index': 2, 'quality': '7', 'position': 2},
    '332': {'root_index': 3, 'quality': '7', 'position': 1},
    '333': {'root_index': 0, 'quality': 'o7', 'position': 0},
    '334': {'root_index': 0, 'quality': 'ø', 'position': 0},
    '341': {'root_index': 3, 'quality': 'maj7', 'position': 1},
    '342': {'root_index': 3, 'quality': 'ø', 'position': 1},
    '343': {'root_index': 0, 'quality': 'm7', 'position': 0},
    '344': {'root_index': 0, 'quality': 'mM7', 'position': 0},
    '359': {'root_index': 3, 'quality': 'm7', 'position': 2},
    '368': {'root_index': 3, 'quality': '7', 'position': 2},
    '369': {'root_index': 0, 'quality': 'o7', 'position': 0},
    '378': {'root_index': 0, 'quality': 'ø', 'position': 0},
    '379': {'root_index': 0, 'quality': 'm7', 'position': 0},
    '388': {'root_index': 0, 'quality': 'mM7', 'position': 0},
    '413': {'root_index': 2, 'quality': 'mM7', 'position': 2},
    '414': {'root_index': 2, 'quality': 'maj7', 'position': 2},
    '424': {'root_index': 0, 'quality': '7b5', 'position': 0},
    '423': {'root_index': 2, 'quality': 'ø', 'position': 2},
    '432': {'root_index': 3, 'quality': 'm7', 'position': 1},
    '433': {'root_index': 0, 'quality': '7', 'position': 0},
    '434': {'root_index': 0, 'quality': 'maj7', 'position': 0},
    '441': {'root_index': 3, 'quality': 'mM7', 'position': 1},
    '443': {'root_index': 3, 'quality': 'mM7', 'position': 2},
    '445': {'root_index': 3, 'quality': 'mM7', 'position': 3},
    '453': {'root_index': 3, 'quality': 'maj7', 'position': 2},
    '459': {'root_index': 3, 'quality': 'ø', 'position': 2},
    '468': {'root_index': 0, 'quality': '7b5', 'position': 0},
    '469': {'root_index': 0, 'quality': '7', 'position': 0},
    '478': {'root_index': 0, 'quality': 'maj7', 'position': 0},
    '497': {'root_index': 2, 'quality': 'mM7', 'position': 3},
    '514': {'root_index': 1, 'quality': 'mM7', 'position': 2},
    '535': {'root_index': 3, 'quality': 'maj7', 'position': 1},
    '536': {'root_index': 3, 'quality': 'ø', 'position': 3},
    '537': {'root_index': 1, 'quality': 'm7', 'position': 2},
    '538': {'root_index': 1, 'quality': 'mM7', 'position': 2},
    '545': {'root_index': 3, 'quality': 'm7', 'position': 3},
    '546': {'root_index': 1, 'quality': '7', 'position': 2},
    '547': {'root_index': 1, 'quality': 'maj7', 'position': 2},
    '574': {'root_index': 1, 'quality': 'maj7', 'position': 2},
    '587': {'root_index': 2, 'quality': 'maj7', 'position': 3},
    '596': {'root_index': 2, 'quality': 'ø', 'position': 3},
    '597': {'root_index': 2, 'quality': 'm7', 'position': 3},
    '626': {'root_index': 2, 'quality': '7b5', 'position': 1},
    '627': {'root_index': 2, 'quality': '7', 'position': 1},
    '635': {'root_index': 3, 'quality': '7', 'position': 3},
    '636': {'root_index': 0, 'quality': 'o7', 'position': 0},
    '637': {'root_index': 1, 'quality': 'ø', 'position': 2},
    '645': {'root_index': 0, 'quality': 'ø', 'position': 0},
    '646': {'root_index': 0, 'quality': '7b5', 'position': 0},
    '686': {'root_index': 3, 'quality': '7b5', 'position': 1},
    '687': {'root_index': 2, 'quality': '7', 'position': 3},
    '695': {'root_index': 3, 'quality': '7', 'position': 1},
    '696': {'root_index': 0, 'quality': 'o7', 'position': 0},
    '697': {'root_index': 0, 'quality': 'ø', 'position': 0},
    '711': {'root_index': 1, 'quality': 'add5/maj7', 'position': 0},
    '714': {'root_index': 2, 'quality': 'maj7', 'position': 1},
    '717': {'root_index': 2, 'quality': 'maj7', 'position': 1},
    '726': {'root_index': 2, 'quality': 'ø', 'position': 1},
    '727': {'root_index': 2, 'quality': 'm7', 'position': 1},
    '735': {'root_index': 0, 'quality': 'm7', 'position': 0},
    '736': {'root_index': 0, 'quality': '7', 'position': 0},
    '744': {'root_index': 0, 'quality': 'mM7', 'position': 0},
    '745': {'root_index': 0, 'quality': 'maj7', 'position': 0},
    '785': {'root_index': 3, 'quality': 'maj7', 'position': 1},
    '786': {'root_index': 3, 'quality': 'ø', 'position': 1},
    '787': {'root_index': 0, 'quality': 'm7', 'position': 0},
    '788': {'root_index': 0, 'quality': 'mM7', 'position': 0},
    '795': {'root_index': 3, 'quality': 'm7', 'position': 1},
    '796': {'root_index': 0, 'quality': '7', 'position': 0},
    '797': {'root_index': 0, 'quality': 'maj7', 'position': 0},
    '810': {'root_index': 1, 'quality': '7', 'position': 1},
    '811': {'root_index': 1, 'quality': 'maj7', 'position': 1},
    '817': {'root_index': 2, 'quality': 'mM7', 'position': 1},
    '853': {'root_index': 2, 'quality': 'mM7', 'position': 3},
    '854': {'root_index': 2, 'quality': 'maj7', 'position': 3},
    '863': {'root_index': 2, 'quality': 'ø', 'position': 3},
    '864': {'root_index': 1, 'quality': '7b5', 'position': 1},
    '872': {'root_index': 3, 'quality': 'm7', 'position': 2},
    '873': {'root_index': 1, 'quality': '7', 'position': 1},
    '874': {'root_index': 1, 'quality': 'maj7', 'position': 1},
    '881': {'root_index': 3, 'quality': 'mM7', 'position': 2},
    '885': {'root_index': 3, 'quality': 'mM7', 'position': 1},
    '889': {'root_index': 3, 'quality': 'mM7', 'position': 3},
    '891': {'root_index': 2, 'quality': 'mM7', 'position': 2},
    '898': {'root_index': 3, 'quality': 'maj7', 'position': 3},
    '910': {'root_index': 1, 'quality': 'm7', 'position': 1},
    '953': {'root_index': 2, 'quality': 'm7', 'position': 3},
    '954': {'root_index': 2, 'quality': '7', 'position': 3},
    '958': {'root_index': 3, 'quality': '7', 'position': 3},
    '962': {'root_index': 3, 'quality': '7', 'position': 2},
    '963': {'root_index': 0, 'quality': 'o7', 'position': 0},
    '964': {'root_index': 1, 'quality': 'ø', 'position': 1},
    '971': {'root_index': 3, 'quality': 'maj7', 'position': 2},
    '972': {'root_index': 3, 'quality': 'ø', 'position': 2},
    '973': {'root_index': 1, 'quality': 'm7', 'position': 1},
    '974': {'root_index': 1, 'quality': 'mM7', 'position': 1},
    '989': {'root_index': 3, 'quality': 'm7', 'position': 3},
    '998': {'root_index': 3, 'quality': '7', 'position': 3},
    '999': {'root_index': 0, 'quality': 'o7', 'position': 0},
    '1053': {'root_index': 0, 'quality': 'ø', 'position': 0},
    '1054': {'root_index': 0, 'quality': 'm7', 'position': 0},
    '1062': {'root_index': 0, 'quality': '7b5', 'position': 0},
    '1063': {'root_index': 0, 'quality': '7', 'position': 0},
    '1089': {'root_index': 0, 'quality': 'ø', 'position': 0},
    '1098': {'root_index': 0, 'quality': 'm7', 'position': 0},
    '1099': {'root_index': 0, 'quality': '7', 'position': 0},
    '1153': {'root_index': 0, 'quality': 'maj7', 'position': 0},
    '1188': {'root_index': 0, 'quality': 'mM7', 'position': 0},
    '1189': {'root_index': 0, 'quality': 'maj7', 'position': 0},
    '1194': {'root_index': 0, 'quality': 'mM7', 'position': 0},
    '2610': {'root_index': 2, 'quality': '7b5', 'position': 1},
    '3510': {'root_index': 2, 'quality': '7', 'position': 1},
    '3511': {'root_index': 2, 'quality': 'maj7', 'position': 1},
    '3610': {'root_index': 2, 'quality': 'ø', 'position': 1},
    '4510': {'root_index': 2, 'quality': 'm7', 'position': 1},
    '4511': {'root_index': 2, 'quality': 'mM7', 'position': 1},
    '5105': {'root_index': 1, 'quality': 'm7', 'position': 2},
    '5106': {'root_index': 1, 'quality': '7', 'position': 2},
    '5115': {'root_index': 1, 'quality': 'maj7', 'position': 2},
    '6105': {'root_index': 1, 'quality': 'ø', 'position': 2},
    '6106': {'root_index': 0, 'quality': '7b5', 'position': 0},
    '8108': {'root_index': 1, 'quality': '7b5', 'position': 1},
    '8109': {'root_index': 1, 'quality': '7', 'position': 1},
    '8118': {'root_index': 1, 'quality': 'maj7', 'position': 1},
    '8910': {'root_index': 2, 'quality': 'm7', 'position': 2},
    '9108': {'root_index': 1, 'quality': 'ø', 'position': 1},
    '9109': {'root_index': 1, 'quality': 'm7', 'position': 1},
    '9118': {'root_index': 1, 'quality': 'mM7', 'position': 1},
    '9311': {'root_index': 2, 'quality': 'maj7', 'position': 2},
    '9810': {'root_index': 2, 'quality': '7', 'position': 2},
    '9910': {'root_index': 2, 'quality': 'ø', 'position': 2},
    '10810': {'root_index': 0, 'quality': '7b5', 'position': 0},

})


#### PRIVATE METHODS ####
def __get_notes_for_key(key):
    '''Returns the notes for the passed key as an array.'''

    key_notes = []

    if (key[0].isupper()):
        key_notes = MAJOR_KEY_NOTES[key]

    else:
        key = key[0].upper() + key[1:]
        key_notes = MINOR_KEY_NOTES[key]

    return key_notes


def __strip_inversion_string(numeral):
    '''
    Strips the passed numeral of its inversion string if present.
    
    Note: This function will not strip the '7' from seventh numerals, as it is required for identifying 
    the chord's quality.
    '''

    stripped_numeral = numeral

    #Remove inversion strings from seventh chords
    if '6/5' in numeral or '4/3' in numeral or '4/2' in numeral:
        stripped_numeral = numeral[0:-3]

        #Half-dim7 chords don't need an additional 7
        if 'ø' not in numeral:
            stripped_numeral += '7'

    #Remove inversion strings from triads
    elif '6' in numeral or '6/4' in numeral:
        stripped_numeral = numeral[0:-1]

    return stripped_numeral


#### PUBLIC METHODS ####
def get_aug6_numeral(numeral, key, note_names):
    '''
    Convert a chord numeral acting as an augmented sixth chord into a more common notation 
    found in 20th-century classical music.

        Parameters:
            numeral (string): The numeral to convert
            key (string): The key contextualizing the numeral.
            note_names (array): The array of note names defining the chord the numeral represents.

        Return: 
            aug6_numeral: The numeral passed, converted if deemed necessary.
    '''
    
    #The augmented-sixth numeral to return
    aug6_numeral = numeral
    
    stripped_numeral = __strip_inversion_string(numeral)

    #Accidentals and distinct notes making up the chord
    note_accidentals = []
    distinct_notes = []

    for note in note_names:
        note_accidentals.append(get_note_accidental_in_key(note, key))

        if note not in distinct_notes:
            distinct_notes.append(note)

    #Italian and German augmented sixth chords for a minor key
    if stripped_numeral == 'VI7' and '#' in note_accidentals:

        if len(distinct_notes) == 4:
            aug6_numeral = 'Ger+6'

        else:
            aug6_numeral = 'It+6'

    #Italian and German augmented sixth chords for a Major key
    elif stripped_numeral == 'bVI7':

        if len(distinct_notes) == 4:
            aug6_numeral = 'Ger+6'

        else:
            aug6_numeral = 'It+6'

    #French augmented sixth chord
    elif stripped_numeral in ['II7b5','VI7b5','bVI7b5']:
        aug6_numeral = 'Fr+6'

    return aug6_numeral


def get_chord_relation_for_key(key, search_numeral):
    '''Returns the relation of a chord numeral relative to the passed key.'''

    chord_relation = ''

    #Strip the numeral if it has an inversion string
    search_numeral = __strip_inversion_string(search_numeral)

    #Check for the numeral relative to a major key
    if key[0].isupper():

        if search_numeral in MAJOR_KEY_NUMERALS:
            chord_relation = 'diatonic'

        elif search_numeral in MAJOR_MIXTURE_NUMERALS:
            chord_relation = 'mixture'

        else:
            chord_relation = 'chromatic'

    #Check for the numeral relative to a minor key
    else:

        if search_numeral in MINOR_KEY_NUMERALS:
            chord_relation = 'diatonic'

        elif search_numeral in MINOR_MIXTURE_NUMERALS:
            chord_relation = 'mixture'

        else: 
            chord_relation = 'chromatic'

    return chord_relation
        

def get_chord_for_intervals(interval_string):
    '''Returns a chord's identification information based on its intervals.'''

    return INTERVAL_STRINGS[interval_string]


def get_lt_numeral_for_dim7(diminished_numeral):
    '''
    Returns the passed numeral as its equivalent built from the leading tone.
    
    Note: If the numeral cannot be re-arranged relative to the leading tone,
    the numeral is instead returned un-altered.
    '''

    lt_numeral = diminished_numeral

    if lt_numeral == 'iio7':
        lt_numeral = 'viio6/5'

    elif lt_numeral == 'ivo7':
        lt_numeral = 'viio4/3'

    elif lt_numeral in ['bvio7', 'vio7']:
        lt_numeral = 'viio4/2'

    elif lt_numeral in ['viio7', '#viio7']:
        lt_numeral = 'viio7'
        
    return lt_numeral


def get_leading_tone_in_key(key):
    '''Returns the leading tone for the passed key whether major or minor.'''
    
    key = key[0].upper() + key[1:]

    return get_note_name_for_degree(key, 7)


def get_note_name_for_degree(key, degree):
    '''Returns the name of the note at the specified scale degree within the passed key.'''
    
    key_notes = __get_notes_for_key(key)

    return key_notes[degree-1]


def get_note_degree_in_key(name, key):
    '''
    Returns the index of the passed note in the given key if it exists within the key.
    
    If the note does not exist in the key, -1 is returned instead.
    '''

    key_notes = __get_notes_for_key(key)
    
    #Search for the note in the key and return the matching note's index
    for i, note_name in enumerate(key_notes):

        if note_name == name:
            return i

    return -1


def get_note_accidental_in_key(search_name, key):
    '''
    Searches for the given note in the passed key and returns its accidental string 
    if it doesn't exist within the key.

    Note: This function's output is meant for proper chord notation visually, i.e.
    when chord numerals are to be rendered in a graphical setting.
    '''
    
    accidental_index = 0

    #The accidental string to return for the passed note
    note_accidental = ''
   
    key_notes = __get_notes_for_key(key)

    #Search for the note by its letter name in the passed key
    for note_name in key_notes:

        #Get the index of the note being searched for and its index within the key, i.e. C=0, C#=1
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
    if search_note_index in (key_note_index + 2, key_note_index - 10):
        note_accidental = ACCIDENTAL_STRINGS[accidental_index + 2]

    elif search_note_index in (key_note_index + 1, key_note_index - 11):
        note_accidental = ACCIDENTAL_STRINGS[accidental_index + 1]

    elif search_note_index in (key_note_index - 1, key_note_index + 11):
        note_accidental = ACCIDENTAL_STRINGS[accidental_index - 1]
 
    elif search_note_index in (key_note_index - 2, key_note_index + 10):
        note_accidental = ACCIDENTAL_STRINGS[accidental_index - 2]

    return note_accidental


def identify_chord_numeral_for_key(key, chord_info):
    '''
    Identifies and returns the numeral for this chord relative to the passed key.

    This function will alter the numeral with accidental strings and an inversion string
    if required.

        Parameters:
            key (str): The key the chord is being identified for.
            chord_info (dict): Information defining the chord to identify.

        Return:
            chord_numeral (str)
    '''

    chord_numeral = ''

    #Extract the chord's information passed
    root_note = chord_info['root']
    position = chord_info['position']
    quality = chord_info['quality']

    #1) Get the notes for the appropriate key to search through
    key_diatonic_notes = __get_notes_for_key(key)  

    #2a) If the note is diatonic to the key, get the appropriate numeral by index
    if root_note in key_diatonic_notes:
        chord_numeral = NUMERAL_STRINGS[key_diatonic_notes.index(root_note)]
        
    #2b) If the note is not diatonic to the key, determine its altered numeral
    else:

        #The index and value of the note diatonic to the key
        diatonic_note_index = 0
        diatonic_note_value = 0

        #The value of the root note, chromatic to the key
        chromatic_note_value = NOTE_INDICES[root_note]

        #Search for the stripped note_name in the key's notes
        for i, note in enumerate(key_diatonic_notes):

            #Compare the root_note's letter name to the given note
            if root_note[0] == note[0]:
                diatonic_note_index = i
                diatonic_note_value = NOTE_INDICES[note]
                break

        #Set the accidental string for the chromatic note relative to the key's diatonic note
        if chromatic_note_value == diatonic_note_value + 1:
            chord_numeral = f'#{NUMERAL_STRINGS[diatonic_note_index]}'

        elif chromatic_note_value == diatonic_note_value + 2:
            chord_numeral = f'x{NUMERAL_STRINGS[diatonic_note_index]}'

        elif chromatic_note_value == diatonic_note_value - 1:
            chord_numeral = f'b{NUMERAL_STRINGS[diatonic_note_index]}'

        else:
            chord_numeral = f'bb{NUMERAL_STRINGS[diatonic_note_index]}'

    #3) Chords of these qualities use a lower-case numeral
    if quality in ['m', 'm7', 'ø', 'o', 'o7', 'mM7']:
        chord_numeral = chord_numeral.lower()

    chord_numeral += CHORD_QUALITY_STRINGS[quality]

    #4) Append the appropriate inversion string to the numeral
    if quality in ['', 'm', 'o', '+']:
        chord_numeral += INVERSION_TRIAD_STRINGS[position]

    elif quality in ['7', 'm7', 'maj7', 'ø', 'o7']:
        chord_numeral += INVERSION_SEVENTH_STRINGS[position]

        #Half-diminished chords don't add a 7 in root position 
        if quality == 'ø' and position == 0:
            chord_numeral = chord_numeral[0:-1]

    return chord_numeral


def identify_applied_numeral(base_chord_key, base_chord_quality, applied_chord_info):
    '''
    Returns an applied dominant numeral describing the passed applied chord's relation
    to the passed 'base' chord.

    Parameters:
        base_chord_key (str): The key to base the applied chord in
        base_chord_quality (str): The quality of the base chord
        applied_chord_info (dict): Chord properties defining the applied chord

    Return:
        applied_numeral or '' if the applied chord doesn't act as a dominant to the base chord

    Note: Fully-diminished seventh chords act as applied dominants if they can be represented
    as a leading tone fully-diminished seventh chord.
    '''

    #The applied numeral to reutrn
    applied_numeral = ''

    if base_chord_quality in ['','m','maj7','7','m7']:

        if base_chord_quality in ['m', 'm7']:
            base_chord_key = base_chord_key.lower()

        #Check if a fully-diminished seventh chord can be based on the leading tone
        if applied_chord_info['quality'] == 'o7':

            diminished_numeral = identify_chord_numeral_for_key(base_chord_key, applied_chord_info)
            diminished_numeral = get_lt_numeral_for_dim7(diminished_numeral)

            if diminished_numeral in ['viio7', 'viio6/5', 'viio4/3', 'viio4/2']:
                applied_numeral = diminished_numeral

        else:
            retrieved_numeral = identify_chord_numeral_for_key(base_chord_key, applied_chord_info)
            stripped_numeral = __strip_inversion_string(retrieved_numeral)

            #Dominant or leading tone triad or seventh chord
            if stripped_numeral in ['V', 'V7', 'viio', 'viiø', 'viio7']:
                applied_numeral = retrieved_numeral

            #Leading tone triad or seventh chord in a minor key
            elif stripped_numeral in ['#viio', '#viiø']:
                applied_numeral = retrieved_numeral[1:]

    return applied_numeral

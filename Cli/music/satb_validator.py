'''
Module containing functions for validating a chord progression by 20th-century 
four-part harmony writing rules.

Note: The validation rules in this progression assume the following fully-diminished seventh
chords to be based on the leading tone: iio7, ivo7, vio7, bvio7.
'''

from .music_info import get_note_name_for_degree, get_leading_tone_in_key
from .music_info import get_chord_relation_for_key, get_lt_numeral_for_dim7

#Set of validation parameters used for validating the SATB chord progression
_VALIDATION_SETTINGS = {
    'max_distance': [12, 12, 24],
    'voice_range': [[26,50],[36,57],[43,62],[47,69]],
    'chord_types': ['','m','o','+','7','M7','m7','ø','o7', '7b5'],
    'seventh_chords': ['7','maj7','m7','ø','o7'],
    'special_chromatic_chords': ['bII','bVI7','VI7','II7b5','VI7b5']
}


def __check_chord_doubling(chord, chord_index, key, tendancy_tone):
    '''
    Validates a chord's doubled notes and returns errors for doubled tendancy tones.

    Parameters:
        chord (Chord): The chord to validate
        chord_index (int): The index of the chord in the progression
        key (str): The key the chord progression is in
        tendancy_tone (str): The tendancy tone to check for, (leading tone or chordal seventh)

    Return:
        doubling_error: An error for the chord's doubling or None
    '''

    doubling_error = None

    if tendancy_tone == 'leading':
        leading_tone = get_leading_tone_in_key(key)

        if len(chord.find_notes_by_name(leading_tone)) > 1:
            doubling_error = {'type': 'spelling', 'code': 'ERR_DOUBLED_LT', 'details': {'chord_index': chord_index}}
        
    else:
        seventh_index = None

        #Special case for fully-diminished chords to convert them to their vii counterpart
        if chord.quality == 'o7':
            seventh_index = __get_dim7_seventh_index(chord, key)

        else:
            seventh_index = chord.get_seventh_index()

        seventh_name = chord.get_note_name_at_index(seventh_index)

        if len(chord.find_notes_by_name(seventh_name)) > 1:
            doubling_error = {'type': 'spelling', 'code': 'ERR_DOUBLED_7TH', 'details': {'chord_index': chord_index}}

    return doubling_error

def __check_voice_spacing(chord, chord_index):
    '''Validates the passed chord by the intervals (spacing) between voices.'''

    max_distances = _VALIDATION_SETTINGS['max_distance']

    distance_errors = []

    #Get the distance between each adjacent pairing of voices
    soprano_alto_distance = chord.notes[3].get_interval(chord.notes[2], True)
    alto_tenor_distance = chord.notes[2].get_interval(chord.notes[1], True)
    tenor_bass_distance = chord.notes[1].get_interval(chord.notes[0], True)

    #Verify that none of the distances exceed the maximum distance allowed
    if soprano_alto_distance > max_distances[0]:
        distance_errors.append({'type': 'spacing', 'code': 'ERR_SA_DISTANCE', 'details': {'chord_index': chord_index}})

    if alto_tenor_distance > max_distances[1]:
        distance_errors.append({'type': 'spacing', 'code': 'ERR_AT_DISTANCE', 'details': {'chord_index': chord_index}})

    if tenor_bass_distance > max_distances[2]:
        distance_errors.append({'type': 'spacing', 'code': 'ERR_TB_DISTANCE', 'details': {'chord_index': chord_index}})

    return distance_errors

def __check_voice_in_range(chord, chord_index):
    '''
    Rule validation to ensure that the note for the specified voice is within its proper range.
    
    Parameters:
        chord - The chord to validate
        chord_index - The index (position) of the chord in the progression
    '''

    max_voice_ranges = _VALIDATION_SETTINGS['voice_range']

    range_low_codes = ['ERR_BASS_LOW', 'ERR_TENOR_LOW', 'ERR_ALTO_LOW', 'ERR_SOPRANO_LOW']
    range_high_codes = ['ERR_BASS_HIGH', 'ERR_TENOR_HIGH', 'ERR_ALTO_HIGH', 'ERR_SOPRANO_HIGH']

    range_errors = []

    for i, note in enumerate(chord.notes):

        if note.value < max_voice_ranges[i][0]:
            range_errors.append({'type': 'range', 'code': range_low_codes[i], 'details': {'chord_index': chord_index}})

        elif note.value > max_voice_ranges[i][1]:
            range_errors.append({'type': 'range', 'code': range_high_codes[i], 'details': {'chord_index': chord_index}})

    return range_errors

def __check_voice_movement(prev_chord, curr_chord, curr_chord_index):
    '''Pairwise chord rule validation to check for parallel 5th/8ve movement errors or hidden 5th/8ve errors.'''

    movement_errors = []

    #Form every pair of notes in the previous chord and check the interval between the notes in semitones
    for i in range(0, len(prev_chord.notes) - 1):
        for j in range(i+1, len(prev_chord.notes)):
            prev_interval = prev_chord.notes[i].get_interval(prev_chord.notes[j])

            #Check for parallel 5ths
            if prev_interval == 7:
                curr_interval = curr_chord.notes[i].get_interval(curr_chord.notes[j])

                if prev_interval == curr_interval:
                    movement_errors.append({'type': 'movement', 'code': 'ERR_PARALLEL_5TH', 'details': {'prev_chord_index': curr_chord_index - 1, 
                    'curr_chord_index': curr_chord_index, 'voice_one': i, 'voice_two': j}})

            #Check for parallel 8ves
            elif prev_interval == 0:
                curr_interval = curr_chord.notes[i].get_interval(curr_chord.notes[j])

                if prev_interval == curr_interval:
                    movement_errors.append({'type': 'movement', 'code': 'ERR_PARALLEL_8TH', 'details': {'prev_chord_index': curr_chord_index - 1, 
                    'curr_chord_index': curr_chord_index, 'voice_one': i, 'voice_two': j}})

    return movement_errors

def __check_leading_resolution(prev_chord, curr_chord, key, prev_chord_index):
    '''
    This function checks if the previous chord passed has a leading tone for the key passed, 
    and ensures it resolves in the following chord or was passed to the next chord if it is.
    '''

    #The error to return for the chord or None if there isn't an error
    resolution_error = None

    #The value of the note the leading tone must resolve to
    resolution_values = []
    
    leading_tone_index = -1
    leading_tone_name = get_leading_tone_in_key(key)

    prev_numeral = prev_chord.get_numeral_for_key(key)

    #Search for the leading tone in the previous chord
    for i, note in enumerate(prev_chord.get_note_names()):
        print(note)
        if note == leading_tone_name:
            leading_tone_index = i
            break

    #If the chord contains the leading tone, validate its resolution
    if leading_tone_index != -1:

        #Set the possible resolution notes for the leading tone
        resolution_values.append(get_note_name_for_degree(key, 1))

        #V7 chords can resolve the lt to scale degree 5 if the lt isn't in the soprano voice
        if prev_numeral == 'V7' and leading_tone_index != 3:
            resolution_values.append(get_note_name_for_degree(key, 5))

        #If the leading tone doesn't resolve, check if it was passed to the next chord
        if curr_chord.get_note_name_at_index(leading_tone_index) not in resolution_values:
            new_leading_tone_index = -1

            for i, note in enumerate(curr_chord.get_note_names()):
                if note == leading_tone_name:
                    new_leading_tone_index = i

            #If the leading tone was passed to the current chord, return a warning for a delayed resolution
            if new_leading_tone_index != -1:
                resolution_error = {'type': 'warning', 'code': 'WARN_DELAYED_LT', 
                'details': {'chord_index': prev_chord_index, 'lt_index': new_leading_tone_index, 
                'resolve_notes': resolution_values}}

            #Else, return a resolution error
            else:
                print('Add the error')
                resolution_error = {'type': 'resolution', 'code': 'ERR_UNRESOLVED_LT', 
                'details': {'chord_index': prev_chord_index, 'voice_index': leading_tone_index}}

    return resolution_error

    
def __check_seventh_resolution(prev_chord, curr_chord, key, curr_chord_index):
    '''
    This function gets the index of the seventh in the previous chord passed, and ensures it resolves 
    in the following chord or is passed to that chord otherwise.
    '''

    resolution_error = None

    seventh_index = None
    resolution_note = ''

    #1) Determine the index of the chordal seventh

    if prev_chord.quality == 'o7':
        seventh_index = __get_dim7_seventh_index(prev_chord, key)
        
    else:
        seventh_index = prev_chord.get_seventh_index()

    seventh_name = prev_chord.notes[seventh_index].name
    seventh_degree = prev_chord.notes[seventh_index].get_degree_in_key(key)

    #2) Get the name of the note that the chordal seventh must resolve to
    resolution_note = get_note_name_for_degree(key, seventh_degree)

    #Check if the voice in the current chord at the index of the seventh is the resolution note
    if curr_chord.notes[seventh_index].name != resolution_note:

        passed_seventh = False

        #If the seventh wasn't resolved, check if it was passed to the next chord (delayed resolution)
        for note in curr_chord.notes:
            if note.name == seventh_name:
                passed_seventh = True

        #If the seventh note doesn't appear in the current chord declare a seventh resolution error
        if not passed_seventh:
            resolution_error = {'type': 'resolution', 'code': 'ERR_UNRESOLVED_7TH', 'details': 
            {'chord_index': curr_chord_index - 1, 'voice_index': seventh_index}}

    return resolution_error

        
def __get_dim7_seventh_index(chord, key):
    '''Helper function to get the proper seventh of a fully-diminished vii chord.'''

    seventh_index = 0

    #Third-inversion, 7th is the base note
    if chord.get_numeral_for_key(key) in ['bvio7', 'vio7']:
        seventh_index = 0

    #Second-inversion, 7th is a minor 3rd above the base
    elif chord.get_numeral_for_key(key) == 'ivo7':
        seventh_index = chord.get_indices_from_interval(3)[0]

    #First-inversion, 7th is a minor 6th above the base
    elif chord.get_numeral_for_key(key) == 'iio7':
        seventh_index = chord.get_indices_from_interval(6)[0]

    #Root-position, get the seventh normally
    else:
        seventh_index = chord.get_seventh_index()

    return seventh_index


def validate_progression(progression, key):
    '''Central function to validate the passed chord progression according to SATB notation rules.'''

    progression_warnings = []
    progression_errors = []

    #Hold the previous chord while iterating for resolution errors
    prev_chord = None
    prev_relation = None

    for i, curr_chord in enumerate(progression, start=1):
        current_key = key
        chord_numeral = curr_chord.get_numeral_for_key(current_key, False)

        if curr_chord.quality == 'o7':
            chord_numeral = get_lt_numeral_for_dim7(chord_numeral)

        chord_relation = get_chord_relation_for_key(current_key, chord_numeral)

        #1) Check for spelling errors or unknown chords
        if len(curr_chord) != 4:
            progression_errors.append({'type': 'spelling', 'code': 'ERR_NUM_VOICES', 'details': {'chord_index': i}})
            continue    
        
        if curr_chord.quality not in _VALIDATION_SETTINGS['chord_types']:
            progression_errors.append({'type': 'spelling', 'code': 'ERR_UNKNOWN_CHORD', 'details': {'chord_index': i}})

        #Check for applied chords or including the special case V/iv
        elif chord_relation == 'chromatic' or (chord_relation == 'mixture' and chord_numeral == 'I'):

            #If this chord isn't a recognizable chromatic chord, check if it's an applied chord
            if chord_numeral not in _VALIDATION_SETTINGS['special_chromatic_chords']:
                    
                try: 
                    next_chord = progression[i]
                    applied_numeral = curr_chord.get_applied_numeral(next_chord, False)
        
                    if applied_numeral != '':
                        chord_numeral = applied_numeral
                        chord_relation = 'applied'
                        current_key = next_chord.get_root_name()
        
                        if next_chord.quality in ['m', 'm7']:
                            current_key = current_key.lower()

                    else:
                        progression_errors.append({'type': 'spelling', 'code': 'ERR_UNKNOWN_CHORD', 'details': {'chord_index': i}})

                except IndexError:
                    progression_errors.append({'type': 'spelling', 'code': 'ERR_UNKNOWN_CHORD', 'details': {'chord_index': i}})

        #2) Get voice spacing errors
        progression_errors.extend(__check_voice_spacing(curr_chord, i))

        #3) Check for range errors between voices in the current chord
        progression_errors.extend(__check_voice_in_range(curr_chord, i))

        #4) Get tendancy tone doubling errors
        if error := __check_chord_doubling(curr_chord, i, current_key, 'leading'): 
            progression_errors.append(error)

        if curr_chord.quality in _VALIDATION_SETTINGS['seventh_chords']:
            if error := __check_chord_doubling(curr_chord, i, current_key, 'seventh'): 
                progression_errors.append(error)

        #4) Get movement and resolution errors between chords
        if prev_chord:
            progression_errors.extend(__check_voice_movement(prev_chord, curr_chord, i))

            #If the previous chord was an applied chord, adjust the key to use
            if prev_relation == 'applied':
                altered_key = curr_chord.get_root_name()

                if prev_chord.quality in _VALIDATION_SETTINGS['seventh_chords']:
                    if error := __check_seventh_resolution(prev_chord, curr_chord, altered_key, i): 
                        progression_errors.append(error)
                
                if error := __check_leading_resolution(prev_chord, curr_chord, altered_key, i-1): 
                    progression_errors.append(error)

            #Else, check the chords for the progression key as normal
            else:

                if prev_chord.quality in _VALIDATION_SETTINGS['seventh_chords']:
                    if error := __check_seventh_resolution(prev_chord, curr_chord, current_key, i): 
                        progression_errors.append(error)
                
                if error := __check_leading_resolution(prev_chord, curr_chord, current_key, i-1): 

                    if error['type'] == 'warning':
                        progression_warnings.append(error)

                    else:
                        progression_errors.append(error)

        #Save the current chord's information for validating cross-chord errors
        prev_chord = curr_chord
        prev_relation = chord_relation

    return progression_errors
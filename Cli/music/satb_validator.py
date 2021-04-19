"""Module containing functions for validating a chord progression by 20th-century
four-part harmony writing rules.
"""

from .music_info import get_key_note_for_degree, get_leading_tone_in_key, get_chord_relation_for_key, get_lt_numeral_for_dim7

_validation_settings = {
    'max_distance': [12, 12, 24],
    'voice_range': [[26,50],[36,57],[43,62],[47,69]]
}


def __check_chord_doubling(chord, chord_index, key, type='seventh'):
    """Individual chord rule validation for the notes doubled within the chord."""

    doubling_error = None

    if type == 'leading':
        leading_tone = get_leading_tone_in_key(key)

        if len(chord.find_notes_by_name(leading_tone)) > 1:
            doubling_error = {'type': 'spelling', 'code': 'ERR_DOUBLED_LT', 'details': {'chord_index': chord_index}}
        
    else:
        seventh_index = None
        seventh_name = ''

        #Special case for fully-diminished chords to convert them to their more likely vii counterpart
        if chord.quality == 'o7':
            seventh_index = __get_dim7_seventh_index(chord, key)

        else:
            seventh_index = chord.get_seventh_index()

        seventh_name = chord.notes[seventh_index].name

        if len(chord.find_notes_by_name(seventh_name)) > 1:
            doubling_error = {'type': 'spelling', 'code': 'ERR_DOUBLED_7TH', 'details': {'chord_index': chord_index}}

    return doubling_error


def __check_voice_spacing(chord, chord_index):
    """Individual chord rule validation for the spacing of the voices within the chord."""

    max_distances = [12, 12, 24]

    distance_errors = []

    #Get the note for each SATB voice in the chord
    soprano_value = chord.notes[3].value 
    alto_value = chord.notes[2].value
    tenor_value = chord.notes[1].value
    bass_value = chord.notes[0].value

    #Check the distances between the four voices
    if (soprano_value - alto_value) > _validation_settings['max_distance'][0]:
        distance_errors.append({'type': 'spacing', 'code': 'ERR_SA_DISTANCE', 'details': {'chord_index': chord_index}})

    if alto_value - tenor_value > max_distances[1]:
        distance_errors.append({'type': 'spacing', 'code': 'ERR_AT_DISTANCE', 'details': {'chord_index': chord_index}})

    if tenor_value - bass_value > max_distances[2]:
        distance_errors.append({'type': 'spacing', 'code': 'ERR_TB_DISTANCE', 'details': {'chord_index': chord_index}})

    return distance_errors

def __check_voice_in_range(voice_index, note, chord_index):
    """Rule validation to ensure that the note for the specified voice is within its proper range.
    
    Parameter: voice - An ENUM (S, A, T, B) indicating which voice the corresponding note is associated with.
    Parameter: note - The note the voice is written for as an integer value.
    """

    max_voice_ranges = [[26,50],[36,57],[43,62],[47,69]]

    range_errors = []

    #Check if the passed note's value exceeds its lowest note for its voice
    if note.value < max_voice_ranges[voice_index-1][0]:

        if voice_index == 1:
            range_errors.append({'type': 'range', 'code': 'ERR_BASS_LOW', 'details': {'chord_index': chord_index}})

        elif voice_index == 2:
            range_errors.append({'type': 'range', 'code': 'ERR_TENOR_LOW', 'details': {'chord_index': chord_index}})

        elif voice_index == 3:
            range_errors.append({'type': 'range', 'code': 'ERR_ALTO_LOW', 'details': {'chord_index': chord_index}})

        else:
            range_errors.append({'type': 'range', 'code': 'ERR_SOPRANO_LOW', 'details': {'chord_index': chord_index}})

    #Check if the passed note's value exceeds its highest note for its voice
    elif note.value > max_voice_ranges[voice_index-1][1]:

        if voice_index == 1:
            range_errors.append({'type': 'range', 'code': 'ERR_BASS_HIGH', 'details': {'chord_index': chord_index}})

        elif voice_index == 2:
            range_errors.append({'type': 'range', 'code': 'ERR_TENOR_HIGH', 'details': {'chord_index': chord_index}})

        elif voice_index == 3:
            range_errors.append({'type': 'range', 'code': 'ERR_ALTO_HIGH', 'details': {'chord_index': chord_index}})

        else:
            range_errors.append({'type': 'range', 'code': 'ERR_SOPRANO_HIGH', 'details': {'chord_index': chord_index}})

    return range_errors

def __check_voice_movement(prev_chord, curr_chord, curr_chord_index):
    """Pairwise chord rule validation to check for parallel 5th/8ve movement errors or hidden 5th/8ve errors."""

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

def __check_leading_resolution(prev_chord, curr_chord, key, curr_chord_index):
    """This function checks if the previous chord passed has a leading tone for the key passed, 
    and ensures it resolves in the following chord or was passed to the next chord if it is.
    """

    leading_tone_name = None
    leading_tone_index = None
    resolution_value = None
    resolution_error = None

    leading_tone_name =  get_leading_tone_in_key(key)

    #Search for the leading tone in the previous chord
    for i, note in enumerate(prev_chord.notes):
        if note.name == leading_tone_name:
            leading_tone_index = i
            resolution_value = note.value + 1
            break

    #Ensure that the leading tone appears in the chord (catches sus chords)
    if leading_tone_index != None:

        #If the leading tone doesn't resolve, check if it was passed to the next chord
        if curr_chord.notes[leading_tone_index].value != resolution_value:
            passed_leading_tone = False

            for note in curr_chord.notes:
                if note.name == leading_tone_name:
                    passed_leading_tone = True

            #If the seventh note doesn't appear in the current chord declare a seventh resolution error
            if not passed_leading_tone:
                resolution_error = {'type': 'resolution', 'code': 'ERR_UNRESOLVED_LT', 
                'details': {'chord_index': curr_chord_index - 1, 'voice_index': leading_tone_index}}

    return resolution_error

    
def __check_seventh_resolution(prev_chord, curr_chord, key, curr_chord_index):
    """This function gets the index of the seventh in the previous chord passed, and ensures it resolves 
    in the following chord or is passed to that chord otherwise.
    """

    resolution_error = None

    #Get the index of the seventh from the previous chord, and its name and note value accordingly
    seventh_index = None

    #Special case for fully-diminished chords to convert them to their more likely vii counterpart
    if prev_chord.quality == 'o7':
        seventh_index = __get_dim7_seventh_index(prev_chord, key)
        
    else:
        seventh_index = prev_chord.get_seventh_index()

    seventh_name = prev_chord.notes[seventh_index].name
    seventh_degree = prev_chord.notes[seventh_index].get_degree_in_key(key)

    #Get the name of the note that the seventh must resolve to
    if seventh_degree != 0:    
        resolved_note = get_key_note_for_degree(key, seventh_degree - 1)

    else:
        resolved_note = get_key_note_for_degree(key, 6)

    #Check if the voice in the current chord at the index of the seventh is the resolution note
    if curr_chord.notes[seventh_index].name != resolved_note:

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
    """Helper function to get the proper seventh of a fully-diminished vii chord."""

    seventh_index = 0

    if chord.get_numeral_for_key(key, False) in ['vio', 'bvio']:
        seventh_index = 0

    elif chord.get_numeral_for_key(key, False) == 'ivo':
        seventh_index = chord.get_indices_from_interval(3)[0]

    elif chord.get_numeral_for_key(key, False) == 'iio':
        seventh_index = chord.get_indices_from_interval(6)[0]

    else:
        seventh_index = chord.get_seventh_index()

    return seventh_index


def validate_progression(progression, key):
    """Central function to validate the passed chord progression according to SATB notation rules."""

    #Create an instance variable to hold
    progression_errors = []

    #Holder for the previous chord while iterating
    prev_chord = None
    prev_relation = None

    for i, chord in enumerate(progression, start=1):
        current_key = key
        chord_numeral = chord.get_numeral_for_key(current_key, False)

        if chord.quality == 'o7':
            chord_numeral = get_lt_numeral_for_dim7(chord_numeral)

        chord_relation = get_chord_relation_for_key(current_key, chord_numeral)

        #1) Check for spelling errors
        if len(chord) != 4:
            progression_errors.append({'type': 'spelling', 'code': 'ERR_NUM_VOICES', 'details': {'chord_index': i}})
            continue    

        if chord.quality not in ['','m','o','+','ø','o7','maj7','m7','7']:
            progression_errors.append({'type': 'spelling', 'code': 'ERR_UNKNOWN_CHORD', 'details': {'chord_index': i}})

        #Check for applied chords including special cases V/iv, V/VI and V7/VI 
        elif chord_relation == 'chromatic' or (chord_relation == 'mixture' and chord_numeral in ['I', 'III', 'III7', 'III6/5', 'III4/3', 'III4/2']):

            try: 
                next_chord = progression[i]
                secondary_numeral = chord.get_secondary_dominant_numeral(next_chord, False)
    
                if secondary_numeral != '':
                    chord_numeral = secondary_numeral
                    chord_relation = 'applied'
                    current_key = next_chord.get_root_name()
    
                    if next_chord.quality in ['m', 'm7']:
                        current_key = current_key.lower()

                else:
                    progression_errors.append({'type': 'spelling', 'code': 'ERR_UNKNOWN_CHORD', 'details': {'chord_index': i}})

            except IndexError:
                progression_errors.append({'type': 'spelling', 'code': 'ERR_UNKNOWN_CHORD', 'details': {'chord_index': i}})

        #2) Get voice spacing errors
        progression_errors.extend(__check_voice_spacing(chord, i))

        #3) Check for range errors between voices in the current chord
        for j, note in enumerate(chord.notes, start=1):
            progression_errors.extend(__check_voice_in_range(j, note, i))

        #4) Get tendancy tone doubling errors
        if chord_numeral in ['Imaj7', 'iii', 'V', 'viio', 'viiø']:
            if error := __check_chord_doubling(chord, i, current_key, 'leading') : progression_errors.append(error)

        if chord.has_seventh:
            if error := __check_chord_doubling(chord, i, current_key, 'seventh') : progression_errors.append(error)

        #4) Get movement and resolution errors between chords
        if prev_chord:
            progression_errors.extend(__check_voice_movement(prev_chord, chord, i))

            #If the previous chord was an applied chord, adjust the key to use
            if prev_relation == 'applied':
                altered_key = chord.get_root_name()

                if prev_chord.has_seventh:
                    if error := __check_seventh_resolution(prev_chord, chord, altered_key, i): progression_errors.append(error)
                
                if prev_chord.get_numeral_for_key(altered_key, False) in ['Imaj7', 'iii', 'V', 'viio', 'viiø']:
                    if error := __check_leading_resolution(prev_chord, chord, altered_key, i) : progression_errors.append(error)

            #Else, check the chords for the progression key as normal
            else:

                if prev_chord.has_seventh:
                    if error := __check_seventh_resolution(prev_chord, chord, current_key, i): progression_errors.append(error)
                
                if prev_chord.get_numeral_for_key(current_key, False) in ['Imaj7', 'iii', 'V', 'vii']:
                    if error := __check_leading_resolution(prev_chord, chord, current_key, i) : progression_errors.append(error)

        prev_chord = chord
        prev_relation = chord_relation

    return progression_errors
import json

from .chord import ChordFactory
from .chord_progression import ChordProgression

apiFactory = ChordFactory()

def analyze_progression(chords, key='C', validate=True):
    '''
    Main API function to analyze and return information about the received chord progression.
    
    Parameters:
        chords (list): An array of the chords to be analyzed in a progression.
        key (str): The key that the chord progression is written for
        validate (bool): Whether or not the progression should be analyzed for SATB errors

    Return:
        progression_obj (dict)
    '''

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

    if ('m' in key):
        key = key[0:-1]
        key = key.lower()
        
    #Create the chord progression using the gathered valid chords and the key passed
    new_progression = ChordProgression(progression_chords, key)

    #Get the names and numerals from the progression
    chord_names = new_progression.get_progression_chord_names(True)
    chord_numerals = new_progression.get_progression_chord_numerals(True)

    #Get any accidentals for the chords in this key
    chord_accidentals = new_progression.get_progression_chord_accidentals()

    progression_obj = {}
    progression_obj['chords'] = []

    #Create the progression object to return
    for i, (name, numeral, chord) in enumerate(zip(chord_names, chord_numerals, progression_chords)):
        formatted_notes = __format_chord(chord)
        progression_obj['chords'].append({'name': name, 'numeral': numeral, 'notes': formatted_notes, 
        'accidentals': chord_accidentals[i]})

    #If the user requested the SATB errors for the progression, retrieve and format them
    if validate:
        progression_errors = new_progression.validate_progression()
        progression_error_messages = __format_satb_errors(progression_errors)
        progression_obj['satb_errors'] = progression_error_messages

    return progression_obj


def __format_chord(chord):
    '''Function to format the set of chords to return to be suitable for VexFlow's expected format.'''
    
    formatted_notes = []

    notes = str(chord)

    for note in notes.split(','):
        note = note.strip()
        note = note.lower()
        note = note[:-1] + '/' + note[-1]
        formatted_notes.append(note)

    return formatted_notes

def __format_satb_errors(satb_errors):
    '''Converts retrieved errors in a SATB progression to user-friendly messages.'''

    satb_voice_indices = {0: 'Soprano', 1: 'Alto', 2: 'Tenor', 3: 'Bass'}

    error_messages = []

    for error in satb_errors:
        new_message = ''

        #Spelling errors
        if error['type'] == 'spelling':
            chord_index = error['details']['chord_index']

            if error['code'] == 'ERR_NUM_VOICES':
                new_message = f'Chord {chord_index} does not have four voices.'

            elif error['code'] == 'ERR_DOUBLED_LT':
                new_message = f'Chord {chord_index} has a doubled leading tone.'

            elif error['code'] == 'ERR_DOUBLED_7TH':
                new_message = f'Chord {chord_index} has a doubled chordal seventh.'

            else:
                new_message = f'Chord {chord_index} is unknown for the key.'

        #Voice out of range errors
        if error['type'] == 'range':
            chord_index = error['details']['chord_index']
            voice_index = error['details']['voice_index']
            voice_name = satb_voice_indices[voice_index]

            if error['code'] == 'ERR_VOICE_HIGH':
                new_message = f'{voice_name} exceeds its highest allowed note in chord {chord_index}.'

            else:
                new_message = f'{voice_name} exceeds its lowest allowed note in chord {chord_index}.'

        #Spacing between voices errors
        elif error['type'] == 'spacing':
            chord_index = error['details']['chord_index']

            if error['code'] == 'ERR_SA_DISTANCE':
                new_message = f'Too much distance between soprano and alto voices in chord {chord_index}.'
            
            elif error['code'] == 'ERR_SA_DISTANCE':
                new_message = f'Too much distance between alto and tenor voices in chord {chord_index}.'

            if error['code'] == 'ERR_TB_DISTANCE':
                new_message = f'Too much distance between tenor and bass voices in chord {chord_index}.'

        #Tendancy tone resolution errors
        elif error['type'] == 'resolution':
            voice_index = error['details']['voice_index']
            voice_name = satb_voice_indices[voice_index]

            if error['code'] == 'ERR_UNRESOLVED_LT':
                new_message = f'Unresolved {voice_name} leading tone in chord {chord_index}.'

            else:
                new_message = f'Unresolved {voice_name} chordal seventh in chord {chord_index}.'
            
        #Movement errors
        elif error['type'] == 'movement':
            prev_chord_index = error['details']['prev_chord_index']
            curr_chord_index = error['details']['curr_chord_index']
            voice_one = error['details']['voice_one']
            voice_two = error['details']['voice_two']
            voice_one_name = satb_voice_indices[voice_one]
            voice_two_name = satb_voice_indices[voice_two]

            if error['code'] == 'ERR_PARALLEL_5TH':
                new_message = f'Parallel 5ths between chords {prev_chord_index} and {curr_chord_index}'
                new_message += f' in the voices {voice_one_name} {voice_two_name}.'

            else:
                if error['code'] == 'ERR_PARALLEL_5TH':
                    new_message = f'Parallel 8ves between chords {prev_chord_index} and {curr_chord_index}'
                    new_message += f' in the voices {voice_one_name} {voice_two_name}.'

        error_messages.append(new_message)

    return error_messages
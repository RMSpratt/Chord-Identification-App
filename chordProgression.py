import enum
from enum import Enum

from chord import Chord, ChordFactory
from musicInfo import get_key_note_for_degree, get_leading_tone_in_key

class SATBErrors(Enum):
    ERR_SA_DISTANCE = 'Too much distance between soprano and alto voices'
    ERR_AT_DISTANCE = 'Too much distance between alto and tenor voices'
    ERR_TB_DISTANCE = 'Too much distance between tenor and bass voices'
    ERR_SOPRANO_HIGH = 'The Soprano voice exceeds its highest allowable note'
    ERR_SOPRANO_LOW = 'The Soprano voice exceeds its lowest allowable note'
    ERR_ALTO_HIGH = 'The Alto voice exceeds its highest allowable note'
    ERR_ALTO_LOW = 'The Alto voice exceeds its lowest allowable note'
    ERR_TENOR_HIGH = 'The Tenor voice exceeds its highest allowable note'
    ERR_TENOR_LOW = 'The Tenor voice exceeds its lowest allowable note'
    ERR_BASS_HIGH = 'The Bass voice exceeds its highest allowable note'
    ERR_BASS_LOW = 'The Bass voice exceeds its lowest allowable note'
    ERR_PARALLEL_5TH = 'Movement between voicings in a chord creates parallel 5ths'
    ERR_PARALLEL_8TH = 'Movement between voicings in a chord creates parallel octaves'
    ERR_HIDDEN_5TH = 'Movement between voicings in a chord creates hidden 5ths'
    ERR_HIDDEN_8TH = 'Movement between voicings in a chord creates hidden octaves'
    ERR_VOICE_CROSS = 'Movement between voicings in a chord creates a voice crossing'
    ERR_UNRESOLVED_LT = 'A leading tone is unresolved between adjacent chords'
    ERR_UNRESOLVED_7TH ='A 7th is unresolved between adjacent chords'
    ERR_UNKNOWN_CHORD = 'One or more chords are marked as unknown and may have improper notes'


class SATBValidator():
    """Class responsible for validating chord progressions according to a set of voice-leading rules expected in SATB four-part harmony voicings."""

    _validation_settings = {
        'max_distance': [12, 12, 24],
        'voice_range': [[26,50],[36,57],[43,62],[47,69]]
    }

    def __check_voice_distances(self, chord, chord_index):
        """Individual chord rule validation for the spacing of the voices within the chord."""

        distance_errors = []

        #Get the note for each SATB voice in the chord
        soprano_value = chord.notes[3].value 
        alto_value = chord.notes[2].value
        tenor_value = chord.notes[1].value
        bass_value = chord.notes[0].value

        #Check the distances between the four voices
        if (soprano_value - alto_value) > self._validation_settings['max_distance'][0]:
            print(chord.notes[3], soprano_value, chord.notes[2], alto_value)
            print(soprano_value - alto_value)
            distance_errors.append({'type': 'spacing', 'code': 'ERR_SA_DISTANCE', 'details': {'chord_index': chord_index}})

        if alto_value - tenor_value > self._validation_settings['max_distance'][1]:
            distance_errors.append({'type': 'spacing', 'code': 'ERR_AT_DISTANCE', 'details': {'chord_index': chord_index}})

        if tenor_value - bass_value > self._validation_settings['max_distance'][2]:
            distance_errors.append({'type': 'spacing', 'code': 'ERR_TB_DISTANCE', 'details': {'chord_index': chord_index}})

        return distance_errors

    def __check_voice_in_range(self, voice_index, note, chord_index):
        """Individual chord rule validation to ensure that the given note for the specified voice is within its proper range.
        
        Parameter: voice - An ENUM (S, A, T, B) indicating which voice the corresponding note is associated with.
        Parameter: note - The note the voice is written for as an integer value.
        """

        range_errors = []

        #Check if the passed note's value exceeds its lowest note for its voice
        if note.value < self._validation_settings['voice_range'][voice_index-1][0]:

            if voice_index == 1:
                range_errors.append({'type': 'range', 'code': 'ERR_BASS_LOW', 'details': {'chord_index': chord_index}})

            elif voice_index == 2:
                range_errors.append({'type': 'range', 'code': 'ERR_TENOR_LOW', 'details': {'chord_index': chord_index}})

            elif voice_index == 3:
                range_errors.append({'type': 'range', 'code': 'ERR_ALTO_LOW', 'details': {'chord_index': chord_index}})

            else:
                range_errors.append({'type': 'range', 'code': 'ERR_SOPRANO_LOW', 'details': {'chord_index': chord_index}})

        #Check if the passed note's value exceeds its highest note for its voice
        elif note.value > self._validation_settings['voice_range'][voice_index-1][1]:

            if voice_index == 1:
                range_errors.append({'type': 'range', 'code': 'ERR_BASS_HIGH', 'details': {'chord_index': chord_index}})

            elif voice_index == 2:
                range_errors.append({'type': 'range', 'code': 'ERR_TENOR_HIGH', 'details': {'chord_index': chord_index}})

            elif voice_index == 3:
                range_errors.append({'type': 'range', 'code': 'ERR_ALTO_HIGH', 'details': {'chord_index': chord_index}})

            else:
                range_errors.append({'type': 'range', 'code': 'ERR_SOPRANO_HIGH', 'details': {'chord_index': chord_index}})

        return range_errors

    def __check_voice_movement(self, prev_chord, curr_chord, curr_chord_index):
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

    def __check_leading_resolution(self, prev_chord, curr_chord, key):
        """This function checks if the previous chord passed has a leading tone for the key passed, and ensures it resolves in 
            the following chord or was passed to the next chord if it is.
        """

        leading_tone_name = None
        leading_tone_index = None
        resolution_value = None

        prev_numeral = prev_chord.get_numeral_for_key_root(key)

        #If the numeral for the previous chord contains the leading tone of this progression's key, check its resolution
        if prev_numeral in ['Imaj7', 'iii', 'V', 'vii']:
            leading_tone_name =  get_leading_tone_in_key(key)

            for i, note in enumerate(prev_chord.notes):

                if note.name == leading_tone_name:
                    
                    leading_tone_index = i
                    resolution_value = note.value + 1
                    break

            #The leading tone should resolve upward by a semitone
            if curr_chord.notes[leading_tone_index].value == resolution_value:
                return None

            #Check if the leading tone was passed to the next chord for a delayed resolution
            else: 
                passed_leading_tone = False

                #If the seventh wasn't resolved, check if it was passed to the next chord (delayed resolution)
                for note in curr_chord.notes:
                    if note.name == leading_tone_name:
                        passed_leading_tone = True

                #If the seventh note doesn't appear in the current chord declare a seventh resolution error
                if not passed_leading_tone:
                    return {'type': 'resolution', 'description': SATBErrors.ERR_UNRESOLVED_LT.value}

            return None

        return None
    
        
    def __check_seventh_resolution(self, prev_chord, curr_chord, key, curr_chord_index):
        """This function gets the index of the seventh in the previous chord passed, and ensures it resolves in the following chord
            or is passed to that chord otherwise.
        """

        #Get the index of the seventh from the previous chord, and its name and note value accordingly
        seventh_index = prev_chord.get_seventh_index()

        #Special case for fully-diminished chords to convert them to their more likely vii counterpart
        if (prev_chord.quality == 'o7'):

            if prev_chord.get_numeral_for_key(key) == 'vio7':
                seventh_index = 0

            elif prev_chord.get_numeral_for_key(key)  == 'ivo7':
                seventh_index = prev_chord.get_index_from_interval(3)

            elif prev_chord.get_numeral_for_key(key) == 'iio7':
                seventh_index = prev_chord.get_index_from_interval(6)

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
                return {'type': 'resolution', 'code': 'ERR_UNRESOLVED_7TH', 'details': {'chord_index': curr_chord_index - 1, 'voice_index': seventh_index}}
 
        return None

    def validate_progression(self, progression, key):
        """Public function to validate the passed chord progression according to SATB notation rules."""

        #Create an instance variable to hold
        progression_errors = []

        #Holder for the previous chord while iterating
        prev_chord = None

        for i, chord in enumerate(progression, start=1):
            print(f'\nValidating chord: {i} {chord.get_numeral_for_key(key)}')

            progression_errors.extend(self.__check_voice_distances(chord, i))
    
            #Check for movement or resolution errors between the previous chord and the current one
            if prev_chord != None:
                progression_errors.extend(self.__check_voice_movement(prev_chord, chord, i))

                if prev_chord.has_seventh == True:
                    if error := self.__check_seventh_resolution(prev_chord, chord, key, i): progression_errors.append(error)

                if error := self.__check_leading_resolution(prev_chord, chord, key) : progression_errors.append(error)

            #Check for range errors between voices in the current chord
            for j, note in enumerate(chord.notes, start=1):
                progression_errors.extend(self.__check_voice_in_range(j, note, i))

            prev_chord = chord

        return progression_errors

class ChordProgression():
    _chord_factory = ChordFactory()

    def __init__(self, chords=None, key=None):
        self.chords = []
        self.key = None

        if chords:
            self.chords.extend(chords)

        if key:
            self.key = key

    def add_chord(self, chord_string, index=None):
        """Creates a chord from the chord_string passed and adds it to this class's set of chords."""

        try:
            new_chord = self._chord_factory.create_chord(chord_string)

        except ValueError:
            print(f'The chord {chord_string} could not be created.')

        else:

            if index:
                self.chords.insert(index, new_chord)

            else:
                self.chords.append(new_chord)

    def get_progression_chord_numerals(self):
        """Returns the numerals for each chord within this progression."""

        chord_numerals = []

        if self.key:
            
            for chord in self.chords:
                chord_numerals.append(chord.get_numeral_for_key(self.key))

        return chord_numerals

    def get_progression_chord_names(self, slash_notation=False):
        """Returns the names of each chord within this progression."""

        chord_names = []

        for chord in self.chords:
            chord_names.append(chord.get_name(slash_notation))

        return chord_names

    def remove_chord(self, index=None):
        """Removes the chord at the specified index from this chord progression."""

        if index:
            self.chords.pop(index)

    def update_chord(self, index):
        pass

    def validate_progression(self, validator):
        """Validates this chord progression using the passed progression SATB validator"""
        return validator.validate_progression(self.chords, self.key)

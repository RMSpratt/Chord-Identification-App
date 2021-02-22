import enum
from enum import Enum

from chord import Chord, ChordFactory

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
    ERR_UNRESOLVED_LT = 'A leading tone is unresolved between parallel chords'
    ERR_UNRESOLVED_7TH ='A 7th is unresolved between parallel chords'
    ERR_UNKNOWN_CHORD = 'One or more chords are marked as unknown and may have improper notes'


class SATBVoices(Enum):
    Bass = 1
    Tenor = 2
    Alto = 3
    Soprano = 4


class SATBValidator():
    """Class responsible for validating chord progressions according to a set of voice-leading rules expected in SATB four-part harmony voicings."""

    _validation_settings = {
        'max_distance': [12, 12, 24],
        'voice_range': [[29,49],[40,55],[44,62],[51,67]]
    }

    def __check_voice_distances(self, chord):
        """Individual chord rule validation for the spacing of the voices within the chord."""

        distance_errors = []

        #Get the note for each SATB voice in the chord
        soprano_value = chord.notes[3].value 
        alto_value = chord.notes[2].value
        tenor_value = chord.notes[1].value
        bass_value = chord.notes[0].value

        #Check the distances between the four voices
        if (soprano_value - alto_value) > self._validation_settings['max_distance'][0]:
            distance_errors.append({'type': 'spacing', 'description': SATBErrors.ERR_SA_DISTANCE})

        if alto_value - tenor_value > self._validation_settings['max_distance'][1]:
            distance_errors.append({'type': 'spacing', 'description': SATBErrors.ERR_AT_DISTANCE})

        if tenor_value - bass_value > self._validation_settings['max_distance'][2]:
            distance_errors.append({'type': 'spacing', 'description': SATBErrors.ERR_TB_DISTANCE})

        return distance_errors

    def __check_voice_in_range(self, voice, note):
        """Individual chord rule validation to ensure that the given note for the specified voice is within its proper range.
        
        Parameter: voice - An ENUM (S, A, T, B) indicating which voice the corresponding note is associated with.
        Parameter: note - The note the voice is written for as an integer value.
        """

        range_errors = []

        #Get the proper name for the voice by the index passed
        voice_name = SATBVoices(voice).name

        #Check if the passed note's value exceeds its lowest note for its voice
        if note.value < self._validation_settings['voice_range'][voice-1][0]:
            range_errors.append({'type': 'range', 'description': f'{voice_name} voice is too low.'})

        #Check if the passed note's value exceeds its highest note for its voice
        elif note.value > self._validation_settings['voice_range'][voice-1][1]:
            range_errors.append({'type': 'range', 'description': f'{voice_name} voice is too high.'})

        return range_errors

    def __check_voice_movement(self, prev_chord, curr_chord):
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
                        movement_errors.append({'type': 'movement', 'description': SATBErrors.ERR_PARALLEL_5TH})

                #Check for parallel 8ves
                elif prev_interval == 0:
                    curr_interval = curr_chord.notes[i].get_interval(curr_chord.notes[j])

                    if prev_interval == curr_interval:
                        movement_errors.append({'type': 'movement', 'description': SATBErrors.ERR_PARALLEL_8TH})

        return movement_errors

    def validate_progression(self, chords, key):

        #Create an instance variable to hold
        progression_errors = []

        #Holder for the previous chord while iterating
        prev_chord = None

        for i, chord in enumerate(chords, start=1):
            print(f'\nValidating chord: {i}')

            chord_numeral = chord.get_numeral_for_key(key)

            if chord_numeral == 'Unknown':
                progression_errors.append({'type': 'chord', 'description': SATBErrors.ERR_UNKNOWN_CHORD})

            progression_errors.extend(self.__check_voice_distances(chord))

            #Check for movement or resolution errors between the previous chord and the current one
            if prev_chord != None:
                progression_errors.extend(self.__check_voice_movement(prev_chord, chord))

            #Check for range errors between the current chord
            for j, note in enumerate(chord.notes, start=1):
                progression_errors.extend(self.__check_voice_in_range(j, note))

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

    def add_chord(self, chord_info, index=None):
        """Creates a chord from the information passed and adds it to this progression."""

        try:
            new_chord = self._chord_factory.create_chord(chord_info)

        except ValueError:
            print('The chord could not be created.')

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
                chord_numerals.append(chord.identify_numeral_by_key(self.key))

        return chord_numerals

    def get_progression_chord_names(self, slash_notation=False):
        """Returns the names of each chord within this progression."""

        chord_names = []

        for chord in self.chords:
            chord_names.append(chord.get_name(slash_notation))


    def remove_chord(self, index=None):
        """Removes the chord at the specified index from this chord progression."""

        if index:
            self.chords.pop(index)

    def update_chord(self, index):
        pass

    def validate_progression(self, validator):
        """Calls this class's SATB_Validator """
        self.satb_errors = validator.validate_progression(self.chords, self.key)


#Temporary testing until proper tests are written
chord_factory = ChordFactory()
satb_validator = SATBValidator()

chord_one = chord_factory.create_chord('C3, G3, E4, C5')
chord_two = chord_factory.create_chord('B2, G3, F4, D5')
chord_three = chord_factory.create_chord('D3, G3, F4, B4')
chord_four = chord_factory.create_chord('E3, G3, E4, C5')

sample_progression = ChordProgression([chord_one, chord_two, chord_three, chord_four], 'C')
sample_progression.validate_progression(satb_validator)
print(sample_progression.satb_errors)
print(sample_progression.get_progression_chord_numerals())

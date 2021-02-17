import enum
from enum import Enum

from chord import Chord, ChordFactory

"""
LIST OF SETTINGS:

SETTING_SA_MAX_DISTANCE - Max distance allowed between Soprano and Alto voices
SETTING_AT_MAX_DISTANCE - Max distance allowed between Alto and Tenor voices
SETTING_TB_MAX_DISTANCE - Max distance allowed between Tenor and Bass voices

MAX_SOP_VALUE - Highest note a Soprano voice can be written as
MIN_SOP_VALUE - Lowest note a Soprano voice can be written as

MAX_ALTO_VALUE - Highest note an Alto voice can be written as
MIN_ALTO_VALUE - Lowest note an Alto voice can be written as

MAX_TEN_VALUE - Highest note a Tenor voice can be written as
MIN_TEN_VALUE - Lowest note a Tenor voice can be written as

MAX_BASS_VALUE - Highest note a Bass voice can be written as
MIN_BASS_VALUE - Lowest note a Bass voice can be written as

MIDDLE_C - Whether Middle C is considered to be C3 or C4

settings = 
{
    distance: 
    {
        "SA": 12,
        "AT": 12,
        "TB": 24
    },

    range:
    {
        "S": [51, 67],      (D4 - F#5)
        "A": [44, 62],      (G3 - C#5)
        "T": [40, 55],      (Eb3 - F#4)
        "B": [29, 49]       (E2 - C4)
    }
}

"""

"""
LIST OF ERRORS:

-----Spacing Errors-----
ERR_SA_DISTANCE - Too much distance between soprano and alto voices
ERR_AT_DISTANCE - Too much distance between alto and tenor voices
ERR_TB_DISTANCE - Too much distance between tenor and bass voices

-----Range Errors-----
ERR_SOPRANO_HIGH - The Soprano voice exceeds its highest allowable note
ERR_SOPRANO_LOW - The Soprano voice exceeds its lowest allowable note
ERR_ALTO_HIGH - The Alto voice exceeds its highest allowable note
ERR_ALTO_LOW - The Alto voice exceeds its lowest allowable note
ERR_TENOR_HIGH - The Tenor voice exceeds its highest allowable note
ERR_TENOR_LOW - The Tenor voice exceeds its lowest allowable note
ERR_BASS_HIGH - The Bass voice exceeds its highest allowable note
ERR_BASS_LOW - The Bass voice exceeds its lowest allowable note

----Movement Errors-----

ERR_PARALLEL_5TH - Movement between voicings in a chord creates parallel 5ths
ERR_PARALLEL_8TH - Movement between voicings in a chord creates parallel octaves
ERR_HIDDEN_5TH - Movement between voicings in a chord creates hidden 5ths
ERR_HIDDEN_8TH - Movement between voicings in a chord creates hidden octaves
ERR_VOICE_CROSS - Movement between voicings in a chord creates a voice crossing

-----Resolution Errors-----

ERR_UNRESOLVED_LT - A leading tone is unresolved between parallel chords
ERR_UNRESOLVED_7TH - A 7th is unresolved between parallel chords

-----Other Errors-----

ERR_UNKNOWN_CHORD - One or more chords are marked as 'unknown' and may have improper notes

"""


class SATBVoices(Enum):
    Bass = 1
    Tenor = 2
    Alto = 3
    Soprano = 4



class SATBValidator():

    _validation_settings = {
        'max_distance': [12, 12, 24],
        'voice_range': [[29,49],[40,55],[44,62],[51,67]]
    }

    def __init__(self):
        self._errors = []

    def __check_voice_distances(self, chord):
        """Individual chord rule validation for the spacing of the voices within the chord."""

        #Get the note for each SATB voice in the chord
        soprano_value = chord.notes[3].value 
        alto_value = chord.notes[2].value
        tenor_value = chord.notes[1].value
        bass_value = chord.notes[0].value

        #Check the distances between the four voices
        if (soprano_value - alto_value) > self._validation_settings['max_distance'][0]:
            self._errors.append({"type": "spacing", "description": "Too much distance between soprano and alto voices."})

        if alto_value - tenor_value > self._validation_settings['max_distance'][1]:
            self._errors.append({"type": "spacing", "description": "Too much distance between alto and tenor voices."})

        if tenor_value - bass_value > self._validation_settings['max_distance'][2]:
            self._errors.append({"type": "spacing", "description": "Too much distance between tenor and bass voices."})

    def __check_voice_in_range(self, voice, note):
        """Individual chord rule validation to ensure that the given note for the specified voice is within its proper range.
        
        Parameter: voice - An ENUM (S, A, T, B) indicating which voice the corresponding note is associated with.
        Parameter: note - The note the voice is written for as an integer value.
        """

        #Get the proper name for the voice by the index passed
        voice_name = SATBVoices(voice).name

        #Check if the passed note's value exceeds its lowest note for its voice
        if note.value < self._validation_settings['voice_range'][voice-1][0]:
            self._errors.append({"type": "range", "description": f"{voice_name} voice is too low."})
            print(f"{voice_name} voice too low error.")

        #Check if the passed note's value exceeds its highest note for its voice
        elif note.value > self._validation_settings['voice_range'][voice-1][1]:
            self._errors.append({"type": "range", "description": f"{voice_name} voice is too high."})
            print(f"{voice_name} voice too high error.")

    def __check_voice_movement(self, prev_chord, curr_chord):
        """Pairwise chord rule validation to check for parallel 5th/8ve movement errors or hidden 5th/8ve errors."""

        #Form every pair of notes in the previous chord and check the interval between the notes in semitones
        for i in range(0, len(prev_chord.notes) - 1):
            for j in range(i+1, len(prev_chord.notes)):
                prev_interval = prev_chord.notes[i].get_interval(prev_chord.notes[j])

                #Check for parallel 5ths
                if prev_interval == 7:
                    curr_interval = curr_chord.notes[i].get_interval(curr_chord.notes[j])

                    if prev_interval == curr_interval:
                        self._errors.append({"type": "movement", "description": "Parallel 5ths between two chords."})
                        print("Parallel 5th movement error.")

                #Check for parallel 8ves
                elif prev_interval == 0:
                    curr_interval = curr_chord.notes[i].get_interval(curr_chord.notes[j])

                    if prev_interval == curr_interval:
                        self._errors.append({"type": "movement", "description": "Parallel 8ves between two chords."})
                        print("Parallel 8ve movement error.")

    def validate_progression(self, chords, key):

        #Create an instance variable to hold
        self._errors = []

        #Holder for the previous chord while iterating
        prev_chord = None

        for i, chord in enumerate(chords, start=1):
            print(f"\nValidating chord: {i}")

            chord_numeral = chord.identify_numeral_by_key(key)

            if chord_numeral == "Unknown":
                self._errors.append({"type": "chord", "description": "Unknown chord in progression."})

            self.__check_voice_distances(chord)

            #Check for movement or resolution errors between the previous chord and the current one
            if prev_chord != None:
                self.__check_voice_movement(prev_chord, chord)

            #Check for range errors between the current chord
            for j, note in enumerate(chord.notes, start=1):
                self.__check_voice_in_range(j, note)

            prev_chord = chord


class ChordProgression():
    _chord_factory = ChordFactory()
    _validator = SATBValidator()

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
            print("The chord could not be created.")

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
                numeral = chord.identify_numeral_by_key(self.key)
                chord_numerals.append(numeral)

        return chord_numerals

    def get_progression_chord_names(self):
        pass

    def remove_chord(self, index=None):
        """Removes the chord at the specified index from this chord progression."""

        if index:
            self.chords.pop(index)

    def update_chord(self, index):
        pass

    def validate_progression(self):
        """Calls this class's SATB_Validator """
        self._validator.validate_progression(self.chords, self.key)


chord_factory = ChordFactory()

chord_one = chord_factory.create_chord('C3, G3, E4, C5')
chord_two = chord_factory.create_chord('B2, G3, F4, D5')
chord_three = chord_factory.create_chord('D3, G3, F4, B4')
chord_four = chord_factory.create_chord('E3, G3, E4, C5')

sample_progression = ChordProgression([chord_one, chord_two, chord_three, chord_four], 'C')
sample_progression.validate_progression()
print(sample_progression.get_progression_chord_numerals())

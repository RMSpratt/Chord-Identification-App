import enum
from enum import Enum

from main import Chord

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


class ChordProgression():
    
    def __init__(self, chords=None, key=None):
        self.chords = []
        self.numerals = []
        self.key = None
        self.errors = []
        self.warnings = []

        if chords:
            self.chords.extend(chords)

        if key:
            self.key = key

        
class SATBProgression(ChordProgression):
    
    def __init__(self, chords=None, key=None):
        super().__init__(chords, key)

        self.soprano_line = []
        self.alto_line = []
        self.tenor_line = []
        self.bass_line = []

        self.cadence = []

    def add_chord(self, new_chord):
        """Adds a chord to the end of this progression."""
        self.chords.append(new_chord)

    def check_voicing_distances(self, chord):
        """Individual chord rule validation for the spacing of the voices within the chord."""
        
        SETTING_SA_MAX_DISTANCE = 12
        SETTING_AT_MAX_DISTANCE = 12
        SETTING_TB_MAX_DISTANCE = 24

        soprano_value = chord.notes[3]["value"] 
        alto_value = chord.notes[2]["value"]
        tenor_value = chord.notes[1]["value"]
        bass_value = chord.notes[0]["value"]

        if (soprano_value - alto_value) > SETTING_SA_MAX_DISTANCE:
            self.errors.append({"type": "spacing", "description": "Too much distance between soprano and alto voices."})
            print("Soprano Alto spacing error.")

        if alto_value - tenor_value > SETTING_AT_MAX_DISTANCE:
            self.errors.append({"type": "spacing", "description": "Too much distance between alto and tenor voices."})
            print("Alto Tenor spacing error.")

        if tenor_value - bass_value > SETTING_TB_MAX_DISTANCE:
            self.errors.append({"type": "spacing", "description": "Too much distance between tenor and bass voices."})
            print("Tenor Bass spacing error.")

    def check_voice_movements(self, prev_chord, curr_chord):
        """Pairwise chord rule validation to check for parallel 5th/8ve movement errors or hidden 5th/8ve errors."""

        prev_intervals = prev_chord.intervals
        curr_intervals = curr_chord.intervals

        for prev, curr in zip(prev_intervals, curr_intervals):

            if prev == 7 and curr == 7:
                self.errors.append({"type": "movement", "description": "Parallel 5ths between two chords."})
                print("Parallel 5th movement error.")

            elif prev == 12 and curr == 12:
                self.errors.append({"type": "movement", "description": "Parallel octaves between two chords."})
                print("Parallel octave movement error.")

    def check_voice_in_range(self, voice, note):
        """Individual chord rule validation to ensure that the given note for the specified voice is within its proper range."""

        #Get the proper name for the voice by the index passed
        voice_name = SATBVoices(voice).name

        settings = [[29,49], [40,55], [44,62], [51,67]]

        #Check if the passed note's value exceeds its lowest note for its voice
        if note["value"] < settings[voice-1][0]:
            print(str(note["value"]) + " " + str(settings[voice-1][0]))

            self.errors.append({"type": "range", "description": f"{voice_name} voice is too low."})
            print(f"{voice_name} voice too low error.")

        #Check if the passed note's value exceeds its highest note for its voice
        elif note["value"] > settings[voice-1][1]:
            print(str(note["value"]) + " " + str(settings[voice-1][1]))
            self.errors.append({"type": "range", "description": f"{voice_name} voice is too high."})
            print(f"{voice_name} voice too high error.")

    def get_line(self, line):
        """Returns all of the notes for one of the four SATB voices"""
        pass

    def get_full_progression(self):
        """Returns all of the chords within this progression as a detailed object"""
        pass

    def print_progression(self):
        """Displays this full chord progression in a well-formatted manner."""
        pass

    def validate_progression(self):
        """Multipart function that validates all of the chords in this progression for a series of voice-leading rules."""

        if self.key == None:
            print("ERR: A key must be specified for the chord progression for analysis.")
            return

        prev_chord = None

        for index, chord in enumerate(self.chords, start=1):
            print(f"\nValidating chord: {index}")

            new_numeral = chord.identify_numeral_by_key(self.key)
            self.numerals.append(new_numeral)

            if new_numeral == "Unknown":
                self.errors.append({"type": "chord", "description": "Unknown chord in progression."})

            self.check_voicing_distances(chord)

            #Check for movement or resolution errors between the previous chord and the current one
            if prev_chord != None:
                self.check_voice_movements(prev_chord, chord)

            for index, note in enumerate(chord.notes, start=1):
                self.check_voice_in_range(index, note)

            prev_chord = chord

    def get_errors(self, level):
        """Returns all of the errors discovered while validating the chord progression"""
        pass



chord_one = Chord("C3, G3, E4, C5")
chord_two = Chord("B2, G3, F4, D5")
chord_three = Chord("D3, G3, F4, B4")
chord_four = Chord("E3, G3, E4, C5")
chord_five = Chord('D0, Bb0, G1')

# sample_progression = SATBProgression([chord_one, chord_two, chord_three, chord_four], 'C')
# sample_progression.validate_progression()

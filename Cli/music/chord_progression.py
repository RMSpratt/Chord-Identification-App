"""This module exports the ChordProgression class and makes use of the SATB validator."""

from .chord import ChordFactory
from .music_info import get_chord_relation_for_key, identify_secondary_dominant_numeral
from .satb_validator import validate_progression


class ChordProgression():
    """This class represents a sequence of chords possibly defined relative to some key.
    
        The option to validate this class's chords according to SATB voice leading rules
        is available.
    """
    _chord_factory = ChordFactory()

    def __init__(self, chords=None, key=None):
        self.chords = []
        self.key = None

        if chords:
            self.chords.extend(chords)

        if key:
            self.key = key

    def add_chord(self, chord_string, index=None):
        """Creates a chord from the chord_string passed and adds it to the progression."""

        try:
            new_chord = self._chord_factory.create_chord(chord_string)

        except ValueError:
            print(f'The chord {chord_string} could not be created and added to the progression.')

        else:

            if index:
                self.chords.insert(index, new_chord)

            else:
                self.chords.append(new_chord)

    def get_progression_chord_accidentals(self):
        """Returns the accidentals for each chord in this progression for the progression key"""

        accidentals = []

        if self.key:
            for chord in self.chords:
                accidentals.append(chord.get_accidentals_for_key(self.key))

        return accidentals

    def get_progression_chord_numerals(self, use_applied=False):
        """Returns the numerals for each chord within this progression.
        If use_applied is True, the appplied dominant numerals for chords will be used where possible.
        """

        chord_numerals = []

        if self.key:

            for i, chord in enumerate(self.chords):
                chord_numeral = chord.get_numeral_for_key(self.key)
                chord_relation = get_chord_relation_for_key(self.key, chord_numeral)

                if use_applied and chord_relation == 'chromatic' and i < len(self.chords) - 1:
                    applied_numeral = chord.get_secondary_dominant_numeral(self.chords[i+1])

                    if applied_numeral != '':
                        chord_numeral = applied_numeral + '/' + self.chords[i+1].get_numeral_for_key(self.key, False)

                chord_numerals.append(chord_numeral)

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

    def validate_progression(self):
        """Validates this chord progression using the passed progression SATB validator"""

        return validate_progression(self.chords, self.key)

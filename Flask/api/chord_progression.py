'''This module exports the ChordProgression class and makes use of the SATB validator.'''

from .chord import ChordFactory
from .music_info import get_chord_relation_for_key, get_lt_numeral_for_dim7, get_aug6_numeral
from .satb_validator import validate_progression


class ChordProgression():
    '''This class represents a sequence of chords possibly defined relative to some key.
    
        The option to validate this class's chords according to SATB voice leading rules 
        is available.

        Attributes:
            chords (array): The chords making up the progression.
            key (str): The key the progression is based in. Required for SATB validation.
    '''

    _chord_factory = ChordFactory()

    def __init__(self, chords=None, key=None):
        self.chords = []
        self.key = None

        if chords:
            self.chords.extend(chords)

        if key:
            self.key = key

    def add_chord(self, chord_string, index=None):
        '''Creates a chord from the string or dict passed and adds it to the progression.'''

        try:
            new_chord = self._chord_factory.create_chord(chord_string)

        except ValueError:
            raise ValueError('The chord to create: ' + str(new_chord) + ' is invalid.') from ValueError

        else:
            if index:
                self.chords.insert(index, new_chord)

            else:
                self.chords.append(new_chord)

    def get_progression_chord_accidentals(self):
        '''Returns accidentals for each chord in the progression based on the progression's key.'''

        accidentals = []

        if self.key:
            for chord in self.chords:
                accidentals.append(chord.get_accidentals_for_key(self.key))

        return accidentals

    def get_progression_chord_numerals(self, use_applied=True, use_satb=True):
        '''
        Returns the numerals for each chord within this progression.
        
        Parameters:
            use_applied (bool): If True, applied dominant numerals will be used where possible
            use_satb (bool): If True, chords will use more common names where possible

        Return:
            chord_numerals (array): The progression's chord numerals.
        '''

        chord_numerals = []

        if self.key:

            for i, chord in enumerate(self.chords):
                chord_numeral = chord.get_numeral_for_key(self.key)

                #Convert fully-diminished seventh chords to be relative to the leading tone if applicable
                if chord.quality == 'o7':
                    chord_numeral = get_lt_numeral_for_dim7(chord_numeral)

                chord_relation = get_chord_relation_for_key(self.key, chord_numeral)

                #Convert chromatic chords acting as applied dominants to the proceding chord to have an applied numeral
                if use_applied and chord_relation == 'chromatic' or (chord_relation == 'mixture' and chord_numeral == 'I'):
                    
                    try:
                        applied_numeral = chord.get_applied_numeral(self.chords[i+1])

                        if applied_numeral != '':
                            chord_numeral = applied_numeral + '/' + self.chords[i+1].get_numeral_for_key(self.key, False)

                    except IndexError:
                        pass

                if use_satb:

                    #Convert augmented sixth numerals to their more common name
                    chord_numeral = get_aug6_numeral(chord_numeral, self.key, chord.get_note_names())

                    if 'bII' in chord_numeral:
                        chord_numeral = chord_numeral.replace('bII', 'N')

                chord_numerals.append(chord_numeral)

        return chord_numerals

    def get_progression_chord_names(self, slash_notation=False):
        '''Returns the names of each chord in the progression, with or without slash names.'''

        chord_names = []

        for chord in self.chords:
            chord_names.append(chord.get_name(slash_notation))

        return chord_names

    def remove_chord(self, index=None):
        '''Removes the chord at the specified index from this progression.'''

        if isinstance(index, int) and index in [0, len(self.chords) - 1]:
            self.chords.pop(index)
        
        else:
            raise IndexError('The index provided is out of range.')

    def validate_progression(self):
        '''Validates this chord progression using a SATB validator'''

        return validate_progression(self.chords, self.key)

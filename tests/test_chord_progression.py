import pytest

from chord import Chord, ChordFactory
from chordProgression import ChordProgression, SATBValidator

class TestChordProgressions:
    
    def create_progression(self, chords, key):
        """Helper function to create a chord progression using a passed set of chords."""

        test_progression = ChordProgression([], key)

        for chord_string in chords:
            test_progression.add_chord(chord_string)
    
        return test_progression

    def test_no_errors(self):
        """Test for chord progression with no errors."""
        test_validator = SATBValidator()

        #I - V4/3 - viio4/3 - I6 - bVI - iv - iio6/5 - V - I
        normal_progression = self.create_progression(
            ['E2,B3,E4,G#4', 'F#2,B3,D#4,A4', 'A2,C#4,F#4,D#5', 'G#2,B3,G#4,E5', 'C3,G3,E4,C5', 'A2,A3,E4,C5', 'A2,C4,F#4,E5', 
            'B2,B3,F#4,D#5', 'E2,B3,G#4,E5'], 'E')

        test_errors = normal_progression.validate_progression(test_validator)

        assert len(test_errors) == 0

    def test_movement_errors(self):
        """Test for movement errors in a chord progression."""
        test_validator = SATBValidator()

        #I - iii - IV - I
        parallel_prog = self.create_progression(['C3,G3,E4,C5','E3,B3,G4,E5','F3,C4,A4,F5','E3,C4,G4,E5'], 'C')

        parallel_expected = [
            {'code': 'ERR_PARALLEL_5TH', 'prev_chord_index': 1, 'curr_chord_index': 2, 'voice_one': 0, 'voice_two': 1},
            {'code': 'ERR_PARALLEL_8TH', 'prev_chord_index': 1, 'curr_chord_index': 2, 'voice_one': 0, 'voice_two': 3},
            {'code': 'ERR_PARALLEL_5TH', 'prev_chord_index': 2, 'curr_chord_index': 3, 'voice_one': 0, 'voice_two': 1},
            {'code': 'ERR_PARALLEL_8TH', 'prev_chord_index': 2, 'curr_chord_index': 3, 'voice_one': 0, 'voice_two': 3},
            {'code': 'ERR_PARALLEL_8TH', 'prev_chord_index': 3, 'curr_chord_index': 4, 'voice_one': 0, 'voice_two': 3}
        ]

        parallel_errors = parallel_prog.validate_progression(test_validator)

        assert len(parallel_errors) == len(parallel_expected)

        for (error, expected) in zip(parallel_errors, parallel_expected):
            assert error['code'] == expected['code']
            assert error['details']['prev_chord_index'] == expected['prev_chord_index']
            assert error['details']['curr_chord_index'] == expected['curr_chord_index']
            assert error['details']['voice_one'] == expected['voice_one']
            assert error['details']['voice_two'] == expected['voice_two']
        
    def test_seventh_resolution(self):
        
        test_validator = SATBValidator()

        #i - V4/3 - i6 - iv6/5 - V (Validate chord quality 7 and m7 resolution)
        seventh_prog_one = self.create_progression(['F#2,A3,F#4,C#5','G#2,B3,E#4,C#5','A2,C#4,F#4,A4','D3,B3,F#4,A4','C#3,G#3,E#4,C#5'], 'f#')
        
        #i - viio - i - viio4/2 - i (Validate chord quality o7 resolution)
        seventh_prog_two = self.create_progression(['Ab3,Ab2,Cb4,Eb4','G2,Bb3,Fb4,Db5','Ab2,Cb4,Ab4,Eb5','G3,Fb2,Db4,Bb4','Ab2,Ab3,Eb4,Cb4'],'ab')

        #I - IV7 - iiø6/5 - V (Validate chord quality maj7 and ø resolution)
        seventh_prog_three = self.create_progression(['Eb2,G3,Eb4,Bb4','Ab2,G3,Eb4,C5','Ab2,C4,F4,Eb5','Bb2,D4,F4,Bb4'], 'Eb')

        seventh_errors_one = seventh_prog_one.validate_progression(test_validator)
        seventh_errors_two = seventh_prog_two.validate_progression(test_validator)
        seventh_errors_three = seventh_prog_three.validate_progression(test_validator)

        seventh_expected_one = [
            {'code': 'ERR_UNRESOLVED_7TH', 'chord_index': 2, 'voice_index': 1},
            {'code': 'ERR_UNRESOLVED_7TH', 'chord_index': 4, 'voice_index': 3}
        ]

        seventh_expected_two = [
            {'code': 'ERR_UNRESOLVED_7TH', 'chord_index': 2, 'voice_index': 2},
            {'code': 'ERR_UNRESOLVED_7TH', 'chord_index': 4, 'voice_index': 0}
        ]

        seventh_expected_three = [
            {'code': 'ERR_UNRESOLVED_7TH', 'chord_index': 2, 'voice_index': 1},
            {'code': 'ERR_UNRESOLVED_7TH', 'chord_index': 3, 'voice_index': 3}
        ]

        assert len(seventh_errors_one) == len(seventh_expected_one)

        for (error, expected) in zip(seventh_errors_one, seventh_expected_one):
            assert error['code'] == expected['code']
            assert error['details']['chord_index'] == expected['chord_index']
            assert error['details']['voice_index'] == expected['voice_index']

        assert len(seventh_errors_two) == len(seventh_expected_two)

        for (error, expected) in zip(seventh_errors_two, seventh_expected_two):
            assert error['code'] == expected['code']
            assert error['details']['chord_index'] == expected['chord_index']
            assert error['details']['voice_index'] == expected['voice_index']

        assert len(seventh_errors_three) == len(seventh_expected_three)

        for (error, expected) in zip(seventh_errors_three, seventh_expected_three):
            assert error['code'] == expected['code']
            assert error['details']['chord_index'] == expected['chord_index']
            assert error['details']['voice_index'] == expected['voice_index']

    def test_leading_tone_resolution(self):
        pass


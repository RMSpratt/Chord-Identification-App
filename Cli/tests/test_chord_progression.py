"""Contains the TestChordProgression class for testing the ChordProgression class."""

from music.chord_progression import ChordProgression

class TestChordProgressions:
    """Test functions for ChordProgression functionality."""

    def create_progression(self, chords, key):
        """Helper function to create a chord progression using a passed set of chords."""

        test_progression = ChordProgression([], key)

        for chord_string in chords:
            test_progression.add_chord(chord_string)
    
        return test_progression

    def validate_satb_errors(self, expected_errors, actual_errors, error_filter=None):
        """Helper function to compare a list of expected errors with a list of actual errors"""

        #Only validate a certain type of error if specified
        if error_filter:
            actual_errors = list(filter(lambda error: error['type'] == error_filter, actual_errors))

        assert len(expected_errors) == len(actual_errors)

        for (expected, actual) in zip(expected_errors, actual_errors):
            assert expected['code'] == actual['code']
            assert expected['type'] == actual['type']
            
            if expected['type'] in ['spacing', 'range', 'spelling']:
                assert expected['chord_index'] == actual['details']['chord_index']

            elif expected['type'] == 'resolution':
                assert expected['chord_index'] == actual['details']['chord_index']
                assert expected['voice_index'] == actual['details']['voice_index']

            elif expected['type'] == 'movement':
                assert expected['prev_chord_index'] == actual['details']['prev_chord_index']
                assert expected['curr_chord_index'] == actual['details']['curr_chord_index']
                assert expected['voice_one'] == actual['details']['voice_one']
                assert expected['voice_two'] == actual['details']['voice_two']

    def test_no_errors(self):
        """Test for chord progression with no errors."""

        #I - V4/3 - viio4/3 - I6 - bVI - iv - iio6/5 - V - I
        normal_progression = self.create_progression(
            ['E2,B3,E4,G#4', 'F#2,B3,D#4,A4', 'A2,C#4,F#4,D#5', 'G#2,B3,G#4,E5', 'C3,G3,E4,C5', 'A2,A3,E4,C5', 'A2,C4,F#4,E5', 'B2,B3,F#4,D#5', 'E2,B3,G#4,E5'], 'E')

        test_errors = normal_progression.validate_progression()

        assert len(test_errors) == 0

    def test_leading_tone_resolution(self):
        """Test for leading tone resolution errors."""

        #I - V4/3 - V6/5 - I6
        lt_prog_one = self.create_progression(['G2,B3,D4,G4','A2,F#3,D4,C5','F#2,A3,D4,C5','B2,G3,D4,B4'],'G')
        lt_errors_one = lt_prog_one.validate_progression()

        #I - iii - IV - V7
        lt_prog_two = self.create_progression(['Cb2,Cb3,Gb4,Eb5','Eb3,Bb3,Gb4,Eb5','Fb3,Ab3,Fb4,Cb4',
        'Gb3,Gb3,Fb4,Bb4'],'Cb')

        lt_errors_two = lt_prog_two.validate_progression()

        lt_expected_one = [{'code': 'ERR_UNRESOLVED_LT', 'type': 'resolution', 'chord_index': 3, 'voice_index': 0}]
        lt_expected_two = [{'code': 'ERR_UNRESOLVED_LT', 'type': 'resolution', 'chord_index': 2, 'voice_index': 1}]
        
        self.validate_satb_errors(lt_expected_one, lt_errors_one, 'resolution')
        self.validate_satb_errors(lt_expected_two, lt_errors_two, 'resolution')

    def test_movement_errors(self):
        """Test for movement errors in a chord progression."""
  
        #I - iii - IV - I
        parallel_prog = self.create_progression(['C3,G3,E4,C5','E3,B3,G4,E5','F3,C4,A4,F5','E3,C4,G4,E5'], 'C')

        parallel_expected = [
            {'code': 'ERR_PARALLEL_5TH', 'type': 'movement', 'prev_chord_index': 1, 'curr_chord_index': 2, 'voice_one': 0, 'voice_two': 1},
            {'code': 'ERR_PARALLEL_8TH', 'type': 'movement', 'prev_chord_index': 1, 'curr_chord_index': 2, 'voice_one': 0, 'voice_two': 3},
            {'code': 'ERR_PARALLEL_5TH', 'type': 'movement', 'prev_chord_index': 2, 'curr_chord_index': 3, 'voice_one': 0, 'voice_two': 1},
            {'code': 'ERR_PARALLEL_8TH', 'type': 'movement', 'prev_chord_index': 2, 'curr_chord_index': 3, 'voice_one': 0, 'voice_two': 3},
            {'code': 'ERR_PARALLEL_8TH', 'type': 'movement', 'prev_chord_index': 3, 'curr_chord_index': 4, 'voice_one': 0, 'voice_two': 3}
        ]

        parallel_errors = parallel_prog.validate_progression()

        self.validate_satb_errors(parallel_expected, parallel_errors, 'movement')
        
    def test_seventh_resolution(self):
        """Test for seventh resolution errors."""

        #i - V4/3 - i6 - iv6/5 - V (Validate chord quality 7 and m7 resolution)
        seventh_prog_one = self.create_progression(['F#2,A3,F#4,C#5','G#2,B3,E#4,C#5','A2,C#4,F#4,A4','D3,B3,F#4,A4','C#3,G#3,E#4,C#5'], 'f#')
        seventh_errors_one = seventh_prog_one.validate_progression()

        #i - viio - i - viio4/2 - i (Validate chord quality o7 resolution)
        seventh_prog_two = self.create_progression(['Ab3,Ab2,Cb4,Eb4','G2,Bb3,Fb4,Db5','Ab2,Cb4,Ab4,Eb5','G3,Fb2,Db4,Bb4','Ab2,Ab3,Eb4,Cb4'],'ab')
        seventh_errors_two = seventh_prog_two.validate_progression()

        #I - IV7 - iiø6/5 - V (Validate chord quality maj7 and ø resolution)
        seventh_prog_three = self.create_progression(['Eb2,G3,Eb4,Bb4','Ab2,G3,Eb4,C5','Ab2,C4,F4,Eb5','Bb2,D4,F4,Bb4'], 'Eb')
        seventh_errors_three = seventh_prog_three.validate_progression()

        seventh_expected_one = [
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 2, 'voice_index': 1},
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 4, 'voice_index': 3}
        ]

        seventh_expected_two = [
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 2, 'voice_index': 2},
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 4, 'voice_index': 0}
        ]

        seventh_expected_three = [
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 2, 'voice_index': 1},
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 3, 'voice_index': 3}
        ]

        self.validate_satb_errors(seventh_expected_one, seventh_errors_one, 'resolution')
        self.validate_satb_errors(seventh_expected_two, seventh_errors_two, 'resolution')
        self.validate_satb_errors(seventh_expected_three, seventh_errors_three, 'resolution')

    def test_spelling_errors(self):
        """Testing for basic chordal spelling errors including voice range, voice spacing, and notes used."""

        #i - iiø6/5 - viio6/5 - i  (Test voice spacing errors)
        test_spacing_prog = self.create_progression(['A2,E3,A4,E5','D3,A3,B3,F5','B2,G3,D4,F5','A2,A3,C4,E5'],'a')
        test_spacing_errors = test_spacing_prog.validate_progression()

        test_spacing_expected = [
            {'code': 'ERR_AT_DISTANCE', 'type': 'spacing', 'chord_index': 1},
            {'code': 'ERR_SA_DISTANCE', 'type': 'spacing', 'chord_index': 2},
            {'code': 'ERR_SA_DISTANCE', 'type': 'spacing', 'chord_index': 3},
            {'code': 'ERR_SA_DISTANCE', 'type': 'spacing', 'chord_index': 4},
        ]

        #I6 - iii - V4/3 (Test voice high and low range errors)
        test_range_prog = self.create_progression(['F4,Bb4,F5,D6','D3,F3,D4,A4','C2,A2,Eb3,F3'],'Bb')
        test_range_errors = test_range_prog.validate_progression()

        print(test_range_errors)
        test_range_expected = [
            {'code': 'ERR_BASS_HIGH', 'type': 'range', 'chord_index': 1},
            {'code': 'ERR_TENOR_HIGH', 'type': 'range', 'chord_index': 1},
            {'code': 'ERR_ALTO_HIGH', 'type': 'range', 'chord_index': 1},
            {'code': 'ERR_SOPRANO_HIGH', 'type': 'range', 'chord_index': 1},
            {'code': 'ERR_BASS_LOW', 'type': 'range', 'chord_index': 3},
            {'code': 'ERR_TENOR_LOW', 'type': 'range', 'chord_index': 3},
            {'code': 'ERR_ALTO_LOW', 'type': 'range', 'chord_index': 3},
            {'code': 'ERR_SOPRANO_LOW', 'type': 'range', 'chord_index': 3}
        ]

        self.validate_satb_errors(test_spacing_expected, test_spacing_errors, 'spacing')
        self.validate_satb_errors(test_range_expected, test_range_errors, 'range')

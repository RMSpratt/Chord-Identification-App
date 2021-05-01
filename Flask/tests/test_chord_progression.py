"""Contains the TestChordProgression class for testing the ChordProgression class."""

from api.chord_progression import ChordProgression

class TestChordProgressions:
    """Test functions for ChordProgression functionality."""

    def create_progression(self, chords, key):
        """Helper function to create a chord progression using a passed set of chords."""

        test_progression = ChordProgression([], key)

        for chord_string in chords:
            test_progression.add_chord(chord_string)
    
        return test_progression

    def validate_chord_numerals(self, expected_numerals, actual_numerals):
        """Helper function to validate a chord progression's identified numerals."""

        for (expected, actual) in zip(expected_numerals, actual_numerals):
            assert expected == actual
                    
    def validate_satb_errors(self, expected_errors, actual_errors, error_filter=None):
        """Helper function to compare a list of expected errors with a list of actual errors"""

        #Only validate a certain type of error if specified
        if error_filter:
            actual_errors = list(filter(lambda error: error['type'] == error_filter, actual_errors))

        assert len(expected_errors) == len(actual_errors), "# errors E:" + str(len(expected_errors)) + " A:" + str(len(actual_errors))

        for (expected, actual) in zip(expected_errors, actual_errors):
            assert expected['code'] == actual['code']
            assert expected['type'] == actual['type']
            
            if expected['type'] in ('spacing', 'spelling'):
                assert expected['chord_index'] == actual['details']['chord_index']

            elif expected['type'] in ('resolution', 'range'):
                assert expected['chord_index'] == actual['details']['chord_index']
                assert expected['voice_index'] == actual['details']['voice_index']

            elif expected['type'] == 'movement':
                assert expected['prev_chord_index'] == actual['details']['prev_chord_index']
                assert expected['curr_chord_index'] == actual['details']['curr_chord_index']
                assert expected['voice_one'] == actual['details']['voice_one']
                assert expected['voice_two'] == actual['details']['voice_two']


    ### TESTING BASIC CHORD PROGRESSION FUNCTIONS ###
    def test_numeral_identification(self):
        """Test the chord progression class's ability to identify chord numerals.
        
        Note: The main goal of this test is to check that fully-diminished seventh chords are converted properly.
        """

        #i - viio7 - i - viio6/5 - i6 - iv - V7 - VI
        progression_one = self.create_progression(
            ['G2,G3,D4,Bb4','F#2,A3,Eb4,C5','G2,G3,D4,Bb4','A2,F#3,Eb4,C5','Bb2,G3,D4,D5','C3,G3,Eb4,C5',
            'D3,F#3,C4,A4','Eb3,G3,Bb3,G4'],'g')

        progression_numerals = progression_one.get_progression_chord_numerals(use_satb=True)
        expected_numerals = ['i','viio7','i','viio6/5','i6','iv','V7','VI']

        self.validate_chord_numerals(expected_numerals, progression_numerals)

        #I - V4/2 - I6 - viiø6/5 --> IV - Fr+6 - V - bVI
        progression_two = self.create_progression(
            ['Gb2,Bb3,Gb4,Db4','Cb2,Ab3,F4,Db4','Bb2,Bb3,Gb4,Db5','Db3,Bb3,Ab4,Fb5','Cb2,Cb3,Gb4,Eb5','C3,Bbb3,Gb4,Ebb5','Db3,Ab3,F4,Db5','Ebb3,Gb3,Gb4,Bbb4'],'Gb'
        )

        progression_numerals = progression_two.get_progression_chord_numerals(True,use_satb=True)
        expected_numerals = ['I','V4/2','I6','viiø6/5/IV','IV','Ger+6','V','bVI']

        self.validate_chord_numerals(expected_numerals, progression_numerals)

        
    ### TESTING FOUR-PART HARMONY RULE VIOLATIONS ###
    def test_no_errors(self):
        """Test for chord progression with no errors."""

        #I - V4/3 - viiø4/3 - I6 - bVI - iv - iio6/5 - V - I
        progression_one = self.create_progression(
            ['E2,B3,E4,G#4', 'F#2,B3,D#4,A4', 'A2,C#4,F#4,D#5', 'G#2,B3,G#4,E5', 'C3,G3,E4,C5', 'A2,A3,E4,C5', 
            'A2,C4,F#4,E5', 'B2,B3,F#4,D#5', 'E2,B3,G#4,E5'], 'E'
        )

        prog_one_errors = progression_one.validate_progression()

        #i - viio7 - V4/3 - i6 - iv6 - N6 - V - VI - V6-> - iv - i6 - G6 - V7 - i
        progression_two = self.create_progression(
            ['F#2,A3,F#4,C#5','E#2,B3,G#4,D5','G#2,B3,E#4,C#5','A2,A3,F#4,C#5','D3,B3,F#4,D5','B2,B3,G4,D5',
            'C#3,B3,E#4,C#5','D3,A3,F#4,F#5','A#2,F#3,F#4,C#5','B2,F#3,D4,B4','A2,A3,F#4,C#5','B#3,G#3,F#4,D4',
            'C#3,G#3,E#4,C#5','F#2,A3,F#4,C#5'], 'f#'
        ) 

        prog_two_errors = progression_two.validate_progression()

        assert len(prog_one_errors) == 0
        assert len(prog_two_errors) == 0

    def test_doubling_errors(self):
        """Test for errors with doubling tendancy tones in a chord."""

        #I - V6 - I - iii - IV - V
        lt_double_prog = self.create_progression(['F2,A3,F4,C5','E2,C4,G5,E5','F2,C4,A4,F5','A2,C4,E4,E5','Bb2,Bb3,F4,D5','C3,E3,G4,E5'],'F')
        lt_double_errors = lt_double_prog.validate_progression()

        lt_double_expected = [
            {'code': 'ERR_DOUBLED_LT', 'type': 'spelling', 'chord_index': 2},
            {'code': 'ERR_DOUBLED_LT', 'type': 'spelling', 'chord_index': 4},
            {'code': 'ERR_DOUBLED_LT', 'type': 'spelling', 'chord_index': 6},
        ]

        #i - iv7 - i6 - iiø6/5 (iim7 technically) - V7
        seventh_double_prog = self.create_progression(['E3,B3,G4,E5','A2,G3,G4,C5','G2,G3,E4,B4','A2,F#3,E4,E5','B2,A3,A4,D#5'],'e')
        seventh_double_errors = seventh_double_prog.validate_progression()

        seventh_double_expected = [
            {'code': 'ERR_DOUBLED_7TH', 'type': 'spelling', 'chord_index': 2},
            {'code': 'ERR_DOUBLED_7TH', 'type': 'spelling', 'chord_index': 4},
            {'code': 'ERR_DOUBLED_7TH', 'type': 'spelling', 'chord_index': 5}
        ]

        self.validate_satb_errors(lt_double_expected, lt_double_errors, 'spelling')
        self.validate_satb_errors(seventh_double_expected, seventh_double_errors, 'spelling')

    def test_lt_resolution_errors(self):
        """Test for leading tone resolution errors."""

        #I - V4/3 - V6/5 - I6
        lt_prog_one = self.create_progression(['G2,B3,D4,G4','A2,F#3,D4,C5','F#2,A3,D4,C5','B2,G3,D4,B4'],'G')
        
        lt_errors_one = lt_prog_one.validate_progression()
        lt_expected_one = [{'code': 'ERR_UNRESOLVED_LT', 'type': 'resolution', 'chord_index': 3, 'voice_index': 0}]

        self.validate_satb_errors(lt_expected_one, lt_errors_one, 'resolution')

        #I - iii - IV - V7
        lt_prog_two = self.create_progression(['Cb2,Cb3,Gb4,Eb5','Eb3,Bb3,Gb4,Eb5','Fb3,Ab3,Fb4,Cb4',
        'Gb3,Gb3,Fb4,Bb4'],'Cb')

        lt_errors_two = lt_prog_two.validate_progression() 
        lt_expected_two = [{'code': 'ERR_UNRESOLVED_LT', 'type': 'resolution', 'chord_index': 2, 'voice_index': 1}]

        self.validate_satb_errors(lt_expected_two, lt_errors_two, 'resolution')

        #i - V/iv - iv
        lt_prog_three = self.create_progression(['D#3,A#3,F#4,D#5','D#3,A#3,Fx4,D#5','G#2,B3,D#4,B4'],'d#')
        
        lt_errors_three = lt_prog_three.validate_progression()
        lt_expected_three = [{'code': 'ERR_UNRESOLVED_LT', 'type': 'resolution', 'chord_index': 2, 'voice_index': 2}]

        self.validate_satb_errors(lt_expected_three, lt_errors_three, 'resolution')

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

    def test_seventh_resolution_errors(self):
        """Test for seventh resolution errors."""

        #i - V4/3 - i6 - iv6/5 - V (Validate chord quality 7 and m7 resolution)
        seventh_prog_one = self.create_progression(['F#2,A3,F#4,C#5','G#2,B3,E#4,C#5','A2,C#4,F#4,A4','D3,B3,F#4,A4','C#3,G#3,E#4,C#5'], 'f#')
        
        seventh_errors_one = seventh_prog_one.validate_progression()
        seventh_expected_one = [
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 2, 'voice_index': 1},
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 4, 'voice_index': 3}
        ]

        #i - viio7 - i - viio4/2 - i (Validate chord quality o7 resolution)
        seventh_prog_two = self.create_progression(['Ab3,Ab2,Cb4,Eb4','G2,Bb3,Fb4,Db5','Ab2,Cb4,Ab4,Eb5','G3,Fb2,Db4,Bb4','Ab2,Ab3,Eb4,Cb4'],'ab')
        
        seventh_errors_two = seventh_prog_two.validate_progression()
        seventh_expected_two = [
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 2, 'voice_index': 2},
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 4, 'voice_index': 0}
        ]

        #I - IVM7 - ii6/5 - V (Validate chord quality maj7)
        seventh_prog_three = self.create_progression(['Eb2,G3,Eb4,Bb4','Ab2,G3,Eb4,C5','Ab2,C4,F4,Eb5','Bb2,D4,F4,Bb4'], 'Eb')
        seventh_errors_three = seventh_prog_three.validate_progression()
        seventh_expected_three = [
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 2, 'voice_index': 1},
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 3, 'voice_index': 3}
        ]

        #ii - V7/V - V
        seventh_prog_four = self.create_progression(['C#3,C#4,G#4,E5','C#3,B3,G#4,E#5','F#3,C#4,A#4,F#5'],'B')
        
        seventh_errors_four = seventh_prog_four.validate_progression()
        seventh_expected_four = [
            {'code': 'ERR_UNRESOLVED_7TH', 'type': 'resolution', 'chord_index': 2, 'voice_index': 1}
        ]

        self.validate_satb_errors(seventh_expected_one, seventh_errors_one, 'resolution')
        self.validate_satb_errors(seventh_expected_two, seventh_errors_two, 'resolution')
        self.validate_satb_errors(seventh_expected_three, seventh_errors_three, 'resolution')
        self.validate_satb_errors(seventh_expected_four, seventh_errors_four, 'resolution')

    def test_range_errors(self):
        """Testing that the voices in a chord stay within their acceptable range."""

        #I6 - iii - V4/3 (Test voice high and low range errors)
        test_range_prog = self.create_progression(['F4,Bb4,F5,D6','D3,F3,D4,A4','C2,A2,Eb3,F3'],'Bb')
        test_range_errors = test_range_prog.validate_progression()

        test_range_expected = [
            {'code': 'ERR_VOICE_HIGH', 'type': 'range', 'chord_index': 1, 'voice_index': 0},
            {'code': 'ERR_VOICE_HIGH', 'type': 'range', 'chord_index': 1, 'voice_index': 1},
            {'code': 'ERR_VOICE_HIGH', 'type': 'range', 'chord_index': 1, 'voice_index': 2},
            {'code': 'ERR_VOICE_HIGH', 'type': 'range', 'chord_index': 1, 'voice_index': 3},
            {'code': 'ERR_VOICE_LOW', 'type': 'range', 'chord_index': 3, 'voice_index': 0},
            {'code': 'ERR_VOICE_LOW', 'type': 'range', 'chord_index': 3, 'voice_index': 1},
            {'code': 'ERR_VOICE_LOW', 'type': 'range', 'chord_index': 3, 'voice_index': 2},
            {'code': 'ERR_VOICE_LOW', 'type': 'range', 'chord_index': 3, 'voice_index': 3}
        ]

        self.validate_satb_errors(test_range_expected, test_range_errors, 'range')

    def test_spacing_errors(self):
        """Testing for the spacing between voices in a chord."""

        #i - iiø6/5 - viio6/5 - i  (Test voice spacing errors)
        test_spacing_prog = self.create_progression(['A2,E3,A4,E5','D3,A3,B3,F5','B2,G3,D4,F5','A2,A3,C4,E5'],'a')
        test_spacing_errors = test_spacing_prog.validate_progression()

        test_spacing_expected = [
            {'code': 'ERR_AT_DISTANCE', 'type': 'spacing', 'chord_index': 1},
            {'code': 'ERR_SA_DISTANCE', 'type': 'spacing', 'chord_index': 2},
            {'code': 'ERR_SA_DISTANCE', 'type': 'spacing', 'chord_index': 3},
            {'code': 'ERR_SA_DISTANCE', 'type': 'spacing', 'chord_index': 4},
        ]

        self.validate_satb_errors(test_spacing_expected, test_spacing_errors, 'spacing')

    def test_spelling_errors(self):
        """Testing for basic spelling errors including the number of notes in a chord
        and chords unknown to the progression's key.
        """

        test_unknown_prog = self.create_progression(['C3,F#3,C4,A5','G2,C4,D4,G5','C#3,D#4,E4,C#5'],'C')
        test_unknown_errors = test_unknown_prog.validate_progression()

        test_num_voices_prog = self.create_progression(['C3,F3,C4','C3,C4,C5,C6,C7'],'C')
        test_num_voices_errors = test_num_voices_prog.validate_progression()

        test_unknown_expected = [
            {'code': 'ERR_UNKNOWN_CHORD', 'type': 'spelling', 'chord_index': 1},
            {'code': 'ERR_UNKNOWN_CHORD', 'type': 'spelling', 'chord_index': 2},
            {'code': 'ERR_UNKNOWN_CHORD', 'type': 'spelling', 'chord_index': 3},
        ]

        test_num_voices_expected = [
            {'code': 'ERR_NUM_VOICES', 'type': 'spelling', 'chord_index': 1},
            {'code': 'ERR_NUM_VOICES', 'type': 'spelling', 'chord_index': 2},
        ]
        
        self.validate_satb_errors(test_unknown_expected, test_unknown_errors, 'spelling')
        self.validate_satb_errors(test_num_voices_expected, test_num_voices_errors, 'spelling')

    
    ### SPECIFIC TEST CASES FOR APPLIED CHORDS ### 

    def test_applied_numerals(self):
        """Test for proper recognition of applied chords in a progression."""

        #ii - V4/3-->ii - ii6
        applied_prog_one = self.create_progression(['Eb3,Bb3,Gb4,Eb5','F3,Bb3,Ab4,D5','Gb3,Bb4,Gb4,Eb5'], 'Db')
        applied_one_numerals = applied_prog_one.get_progression_chord_numerals(True)
        applied_one_expected = ['ii', 'V4/3/ii', 'ii6']

        #i - V7/VI - VI
        applied_prog_two = self.create_progression(['C#3,C#4,E4,G#4','E3,B3,D4,G#4','A2,A3,C#4,A4'],'c#')
        applied_two_numerals = applied_prog_two.get_progression_chord_numerals(True)
        applied_two_expected = ['i', 'V7/VI', 'VI']

        self.validate_chord_numerals(applied_one_expected, applied_one_numerals)
        self.validate_chord_numerals(applied_two_expected, applied_two_numerals)

    def test_applied_doubling_errors(self):
        """Test for doubling errors in applied chords."""

        #V - viio6/V - V6/5 
        lt_double_prog = self.create_progression(['C3,C4,G4,E5','D3,B3,F4,B4','E3,C4,G4,Bb4'],'F')

        lt_double_errors = lt_double_prog.validate_progression()
        lt_double_expected = [{'code': 'ERR_DOUBLED_LT', 'type': 'spelling', 'chord_index': 2}]
   
        #I - V7/IV - IV
        seventh_double_prog = self.create_progression(['D3,A3,F#4,D5','D3,C4,F#4,C5','G3,G3,G4,B4'],'D')
        
        seventh_double_errors = seventh_double_prog.validate_progression()
        seventh_double_expected = [{'code': 'ERR_DOUBLED_7TH', 'type': 'spelling', 'chord_index': 2}]

        self.validate_satb_errors(lt_double_expected, lt_double_errors, 'spelling')
        self.validate_satb_errors(seventh_double_expected, seventh_double_errors, 'spelling')

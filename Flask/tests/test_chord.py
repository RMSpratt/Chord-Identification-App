"""This test module holds all testing functions for testing the Chord class functions and the 
Note functions by extension.
"""

import pytest

from api.chord import ChordFactory

class TestChords:
    """Set of functions for testing Chord functionality."""

    @pytest.fixture(scope = 'session')
    def get_test_chords(self):
        """Fixture to get a set of triad or seventh chords for testing."""

        test_factory = ChordFactory()

        #Set of major, minor, diminished, and augmented triads for testing
        test_triads = [
            test_factory.create_chord('C3,E3,G3'),
            test_factory.create_chord('F#0,D1,A0'),
            test_factory.create_chord('E5,A5,C#6,E6'),
            test_factory.create_chord('C1,Eb1,G1,Eb2'),
            test_factory.create_chord('D4,B4,F#5,B5'),
            test_factory.create_chord('D0,Bb0,G1'),
            test_factory.create_chord('D#2,A1,F#1'),
            test_factory.create_chord('F#3,C4,A3'),
            test_factory.create_chord('Bbb6,Eb7,Gb7'),
            test_factory.create_chord('E4,G#4,B#5'),
            test_factory.create_chord('Bb5,F#5,D6'),
            test_factory.create_chord('Bb5,F#6,D6'),
        ]

        #Set of major, minor, and diminished sevenths for testing
        test_sevenths = [
            test_factory.create_chord('Eb2,G2,Bb2,D3'),
            test_factory.create_chord('A1,C2,E2,F2'),
            test_factory.create_chord('G5,E6,Bb6,C7'),
            test_factory.create_chord('C3,F#3,A3,D3'),
            test_factory.create_chord('E0,B0,D1,G1'),
            test_factory.create_chord('F4,Ab4,Bb5,Db5'),
            test_factory.create_chord('B2,E2,G3,C#3'),
            test_factory.create_chord('F#1,B1,D2,G#2'),
            test_factory.create_chord('A6,C7,Eb7,Gb7'),
            test_factory.create_chord('F5,D5,Ab5,Cb6'),
        ]

        def get_chord_type(chord_type):
            
            if chord_type == 'triad':
                return test_triads

            elif chord_type == 'seventh':
                return test_sevenths

        return get_chord_type


    ## HELPER METHODS ##

    def compare_properties(self, chords, expected_out):
        """Helper method to validate each chord's basic identification properties."""

        for i, chord in enumerate(chords):
            assert chord.get_name() == expected_out[i]['name']
            assert chord.get_name(True) == expected_out[i]['slash_name']
            assert chord.root_index == expected_out[i]['root_index']
            assert chord.position == expected_out[i]['position']

    def compare_numerals(self, chords, keys, expected_out):
        """Checks each passed chord's numeral relative to the list of passed keys."""

        for i, key in enumerate(keys):
            for j, chord in enumerate(chords):
                assert chord.get_numeral_for_key(key) == expected_out[i][j]


    ### GENERAL CHORD TESTING ###
    def test_accidentals(self, get_test_chords):
        """Test case to check the accidentals for notes within each chord relative to a key"""

        test_triads = get_test_chords(chord_type='triad')
        test_keys = ['C','f#','Gb']

        expected_out = [
            [
                ['','',''],['#','',''],['','','#',''],['','b','','b'],['','','#',''],['','b',''],
                ['#','','#'],['#','',''],['bb','b','b'],['','#','#'],['#','b',''],['b','','#']
            ],
            [
                ['n','','n'],['','',''],['','','',''],['n','b','n','b'],['','','',''],['','b','n'],
                ['','','#'],['','','n'],['bb','b','b'],['','','#'],['','b',''],['b','','']
            ],
            [
                ['n','n','n'],['#','n','n'],['n','n','#','n'],['n','','n',''],['n','n','#','n'],['n','','n'],
                ['#','n','#'],['#','n','n'],['bb','',''],['n','#','#'],['#','','n'],['','n','#']
            ]
        ]

        #Compare accidentals for each given key
        for (i, key) in enumerate(test_keys):

            expected_key_accidentals = expected_out[i]

            for (j, chord) in enumerate(test_triads):

                expected_accidentals = expected_key_accidentals[j]
                actual_accidentals = chord.get_accidentals_for_key(key)

                for (expected, actual) in zip(expected_accidentals, actual_accidentals):
                    assert expected == actual, 'Chord: j Expected: ' + expected + ', Actual: ' + actual 


    ### TRIAD CHORD TESTING ###

    def test_triad_numerals_major(self, get_test_chords):
        """Test case to check the numerals of triad chords relative to a few major keys."""

        test_triads = get_test_chords(chord_type='triad')
        test_keys = ['C','F#','Bb']

        expected_out = [
            ['I','II6','VI6/4','i','vii6','v6/4','#iio6','#ivo','biiio6/4','III+','#IV+','bVII+'],
            ['bV','bVI6','bIII6/4','bv','iv6','bii6/4','vio6','io','bbviio6/4','bVII+','I+','bIV+'],
            ['II','III6','VII6/4','ii','#i6','vi6/4','#iiio6','#vo','ivo6/4','#IV+','#V+','I+'],
        ]

        self.compare_numerals(test_triads, test_keys, expected_out)

    def test_triad_numerals_minor(self, get_test_chords):
        """Test case to check the numerals of triad chords relative to a few minor keys."""

        test_triads = get_test_chords(chord_type='triad')
        test_keys = ['e','g','a']

        expected_out = [
            ['VI','VII6','IV6/4','vi','v6','iii6/4','#viio6','iio','bio6/4','I+','II+','bV+'],
            ['IV','V6','II6/4','iv','#iii6','i6/4','#vo6','#viio','vio6/4','#VI+','#VII+','III+'],
            ['III','IV6','I6/4','iii','ii6','vii6/4','#ivo6','#vio','bvo6/4','V+','#VI+','bII+']
        ]

        self.compare_numerals(test_triads, test_keys, expected_out)

    def test_triad_properties(self, get_test_chords):
        """Test case to check the properties of triad chords of different qualities and inversions."""

        test_triads = get_test_chords(chord_type='triad')

        expected_out = [
            {'name': 'C', 'slash_name': 'C', 'root_index': 0, 'position': 0},
            {'name': 'D', 'slash_name': 'D/F#', 'root_index': 2, 'position': 1},
            {'name': 'A', 'slash_name': 'A/E', 'root_index': 1, 'position': 2},
            {'name': 'Cm', 'slash_name': 'Cm', 'root_index': 0, 'position': 0},
            {'name': 'Bm', 'slash_name': 'Bm/D', 'root_index': 1, 'position': 1},
            {'name': 'Gm', 'slash_name': 'Gm/D', 'root_index': 2, 'position': 2},
            {'name': 'D#o', 'slash_name': 'D#o/F#', 'root_index': 2, 'position': 1},
            {'name': 'F#o', 'slash_name': 'F#o', 'root_index': 0, 'position': 0},
            {'name': 'Ebo', 'slash_name': 'Ebo/Bbb', 'root_index': 1, 'position': 2},
            {'name': 'E+', 'slash_name': 'E+', 'root_index': 0, 'position': 0},
            {'name': 'F#+', 'slash_name': 'F#+', 'root_index': 0, 'position': 0},
            {'name': 'Bb+', 'slash_name': 'Bb+', 'root_index': 0, 'position': 0},
        ]

        self.compare_properties(test_triads, expected_out)


    ### SEVENTH CHORD TESTING ###

    def test_seventh_numerals_major(self, get_test_chords):
        """Test case to check the numerals of seventh chords relative to a few major keys."""

        test_sevenths = get_test_chords(chord_type='seventh')
        test_keys = ['D','Ab','C#']

        expected_out = [
            ['bIIM7','bIIIM6/5','bVII4/3','I4/2','ii7','bvi4/3','viiø6/5','#ivø4/2','vo7','io7'],
            ['VM7','VIM6/5','III4/3','#IV4/2','#v7','ii4/3','#iiiø6/5','#viiø4/2','#io7','#ivo7'],
            ['bbIIIM7','bIVM6/5','bI4/3','bII4/2','biii7','bbvii4/3','iø6/5','vø4/2','bvio7','biio7']
        ]

        self.compare_numerals(test_sevenths, test_keys, expected_out)

    def test_seventh_numerals_minor(self, get_test_chords):
        """Test case to check the numerals of seventh chords relative to a few minor keys."""

        test_sevenths = get_test_chords(chord_type='seventh')
        test_keys = ['f','b','d#']

        expected_out = [
            ['VIIM7','IM6/5','V4/3','#VI4/2','#vii7','iv4/3','#vø6/5','#iiø4/2','#iiio7','#vio7'],
            ['bIVM7','bVM6/5','bII4/3','III4/2','iv7','bi4/3','iiø6/5','#viø4/2','viio7','iiio7'],
            ['bbIIM7','bIIIM6/5','bVII4/3','bI4/2','bii7','bvi4/3','viiø6/5','ivø4/2','bvo7','bio7'],
        ]

        self.compare_numerals(test_sevenths, test_keys, expected_out)

    def test_seventh_properties(self, get_test_chords):
        """Test case to check seventh chord properties of different qualities and inversions."""

        test_sevenths = get_test_chords(chord_type='seventh')

        expected_out = [
            {'name': 'Ebmaj7', 'slash_name': 'Ebmaj7', 'root_index': 0, 'position': 0},
            {'name': 'Fmaj7', 'slash_name': 'Fmaj7/A', 'root_index': 3, 'position': 1},
            {'name': 'C7', 'slash_name': 'C7/G', 'root_index': 3, 'position': 2},
            {'name': 'D7', 'slash_name': 'D7/C', 'root_index': 1, 'position': 3},
            {'name': 'Em7', 'slash_name': 'Em7', 'root_index': 0, 'position': 0},
            {'name': 'Bbm7', 'slash_name': 'Bbm7/F', 'root_index': 3, 'position': 2},
            {'name': 'C#ø', 'slash_name': 'C#ø/E', 'root_index': 2, 'position': 1},
            {'name': 'G#ø', 'slash_name': 'G#ø/F#', 'root_index': 3, 'position': 3},
            {'name': 'Ao7', 'slash_name': 'Ao7', 'root_index': 0, 'position': 0},
            {'name': 'Do7', 'slash_name': 'Do7', 'root_index': 0, 'position': 0},
        ]

        self.compare_properties(test_sevenths, expected_out)


    # ### APPLIED/SECONDARY DOMINANT CHORD TESTING ###

    def test_applied_dominants(self):
        """Test case to check the numerals of chords as applied dominants to other chords."""

        test_factory = ChordFactory()

        test_base_chords = [
            test_factory.create_chord('F1,A1,C1'),          #F major
            test_factory.create_chord('Eb1,Gb1,Bb1'),       #Eb minor
            test_factory.create_chord('Bb1,D1,F1'),         #Bb major
            test_factory.create_chord('E1,G1,B1'),          #E minor   
            test_factory.create_chord('Bb1,Db2,F2'),        #Bb minor
            test_factory.create_chord('F#1,A1,C#1,E2'),     #F# minor
            test_factory.create_chord('Eb1,G1,Bb1,D2'),     #Eb major
            test_factory.create_chord('F1,A1,C1,E1'),       #F Major
            test_factory.create_chord('Ab1,Cb1,Eb1,Ab1'),   #Ab minor
            test_factory.create_chord('F#1,A1,C#1'),        #F# minor
        ]

        #The set of chords to act as applied dominants to the base chords
        test_applied_chords = [
            test_factory.create_chord('C1,E1,G1'),          #RP major triad (C)
            test_factory.create_chord('Bb3,D3,Bb2,Bb2'),    #RP major triad (Bb)
            test_factory.create_chord('Eb5,A4,C5'),         #RP diminished triad (Ao)
            test_factory.create_chord('F#1,A1,D#1'),        #RP diminished triad (D#o)
            test_factory.create_chord('F2,C3,A2,Eb3'),      #RP dominant seventh (F7)
            test_factory.create_chord('C#3,E#2,C#2,B1'),    #TV dominant seventh (C#7)
            test_factory.create_chord('D6,F6,Ab5,C6'),      #SV Half-diminished seventh (Dø)
            test_factory.create_chord('E3,G2,D2,Bb2'),      #TV Half-diminished seventh (Eø)
            test_factory.create_chord('G4,Db5,Bb4,Fb5'),    #RP Full-diminished seventh (Go7)
            test_factory.create_chord('E#4,G#3,B3,D4'),     #FV Full-diminished seventh (E#o7)
        ]

        expected_out = ['V','V','viio','viio','V7','V4/2','viiø4/3','viiø4/2','viio7','viio6/5']

        #Validate the output numeral for every pair of chords
        for i, (base_chord, applied_chord) in enumerate(zip(test_base_chords, test_applied_chords)):
            actual_out = applied_chord.get_applied_numeral(base_chord)

            assert actual_out == expected_out[i], 'Mismatch - Index ' + str(i)

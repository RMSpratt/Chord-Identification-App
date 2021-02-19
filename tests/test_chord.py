import pytest

from chord import Chord, ChordFactory

class TestChords:

    @pytest.fixture(scope = 'class')
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
            test_factory.create_chord('A6,Eb7,Gb7'),
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

        def get_chord_type(type):
            
            if (type == 'triad'):
                return test_triads

            else:
                return test_sevenths

        return get_chord_type

    def compare_properties(self, chords, expected_out):
        """Helper method to validate each chord's basic identification properties."""

        for i, chord in enumerate(chords):
            assert chord.get_name() == expected_out[i]['name']
            assert chord.bass_index == expected_out[i]['bass_index']
            assert chord.position == expected_out[i]['position']

    def compare_numerals(self, chords, keys, expected_out):
        """Helper method to check each passed chord's numeral relative to the list of passed keys."""

        for i, key in enumerate(keys):
            for j, chord in enumerate(chords):
                assert chord.get_numeral_for_key(key) == expected_out[i][j]

    def test_triad_numerals_major(self, get_test_chords):
        """Test case to check the numerals of triad chords relative to a few major keys."""

        test_triads = get_test_chords(type='triad')
        test_keys = ['C','F#','Bb']

        expected_out = [
            ['I','II6','VI6/4','i','vii6','v6/4','#iio6','#ivo','biiio6/4','III+','#IV+','bVII+'],
            ['bV','bVI6','bIII6/4','bv','iv6','bii6/4','vio6','io','bbviio6/4','bVII+','I+','bIV+'],
            ['II','III6','VII6/4','ii','#i6','vi6/4','#iiio6','#vo','ivo6/4','#IV+','#V+','I+'],
        ]

        self.compare_numerals(test_triads, test_keys, expected_out)

    def test_triad_numerals_minor(self, get_test_chords):
        """Test case to check the numerals of triad chords relative to a few minor keys."""
        
        test_triads = get_test_chords(type='triad')
        test_keys = ['e','g','a']

        expected_out = [
            ['VI','VII6','IV6/4','vi','v6','iii6/4','#viio6','iio','bio6/4','I+','II+','bV+'],
            ['IV','V6','II6/4','iv','#iii6','i6/4','#vo6','#viio','vio6/4','#VI+','#VII+','III+'],
            ['III','IV6','I6/4','iii','ii6','vii6/4','#ivo6','#vio','bvo6/4','V+','#VI+','bII+']
        ]

        self.compare_numerals(test_triads, test_keys, expected_out)

    def test_triad_properties(self, get_test_chords):
        """Test case to check the properties of triad chords of different qualities and inversions."""

        test_triads = get_test_chords(type='triad')

        expected_out = [
            {'name': 'C', 'bass_index': 0, 'position': 0},
            {'name': 'D', 'bass_index': 2, 'position': 1},
            {'name': 'A', 'bass_index': 1, 'position': 2},
            {'name': 'Cm', 'bass_index': 0, 'position': 0},
            {'name': 'Bm', 'bass_index': 1, 'position': 1},
            {'name': 'Gm', 'bass_index': 2, 'position': 2},
            {'name': 'D#o', 'bass_index': 2, 'position': 1},
            {'name': 'F#o', 'bass_index': 0, 'position': 0},
            {'name': 'Ebo', 'bass_index': 1, 'position': 2},
            {'name': 'E+', 'bass_index': 0, 'position': 0},
            {'name': 'F#+', 'bass_index': 0, 'position': 0},
            {'name': 'Bb+', 'bass_index': 0, 'position': 0},
        ]
        
        self.compare_properties(test_triads, expected_out)

    def test_seventh_numerals_major(self, get_test_chords):
        """Test case to check the numerals of seventh chords relative to a few major keys."""

        test_sevenths = get_test_chords(type='seventh')
        test_keys = ['D','Ab','C#']

        expected_out = [
            ['bIIM7','bIIIM6/5','bVII4/3','I4/2','ii7','bvi4/3','viiø6/5','#ivø4/2','vo7','io7'],
            ['VM7','VIM6/5','III4/3','#IV4/2','#v7','ii4/3','#iiiø6/5','#viiø4/2','#io7','#ivo7'],
            ['bbIIIM7','bIVM6/5','bI4/3','bII4/2','biii7','bbvii4/3','iø6/5','vø4/2','bvio7','biio7']
        ]

        self.compare_numerals(test_sevenths, test_keys, expected_out)

    def test_seventh_numerals_minor(self, get_test_chords):
        """Test case to check the numerals of seventh chords relative to a few minor keys."""

        test_sevenths = get_test_chords(type='seventh')
        test_keys = ['f','b','d#']

        expected_out = [
            ['VIIM7','IM6/5','V4/3','#VI4/2','#vii7','iv4/3','#vø6/5','#iiø4/2','#iiio7','#vio7'],
            ['bIVM7','bVM6/5','bII4/3','III4/2','iv7','bi4/3','iiø6/5','#viø4/2','viio7','iiio7'],
            ['bbIIM7','bIIIM6/5','bVII4/3','bI4/2','bii7','bvi4/3','viiø6/5','ivø4/2','bvo7','bio7'],
        ]

        self.compare_numerals(test_sevenths, test_keys, expected_out)

    def test_seventh_properties(self, get_test_chords):
        """Test case to check the properties of seventh chords of different qualities and inversions."""

        test_sevenths = get_test_chords(type='seventh')
        
        expected_out = [
            {'name': 'Ebmaj7', 'bass_index': 0, 'position': 0},
            {'name': 'Fmaj7', 'bass_index': 3, 'position': 1},
            {'name': 'C7', 'bass_index': 3, 'position': 2},
            {'name': 'D7', 'bass_index': 1, 'position': 3},
            {'name': 'Emin7', 'bass_index': 0, 'position': 0},
            {'name': 'Bbmin7', 'bass_index': 3, 'position': 2},
            {'name': 'C#ø', 'bass_index': 2, 'position': 1},
            {'name': 'G#ø', 'bass_index': 3, 'position': 3},
            {'name': 'Ao7', 'bass_index': 0, 'position': 0},
            {'name': 'Do7', 'bass_index': 0, 'position': 0},
        ]

        self.compare_properties(test_sevenths, expected_out)
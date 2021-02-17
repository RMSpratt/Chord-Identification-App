import pytest

from chord import Chord, ChordFactory

class TestChords:

    def compare_properties(self, chords, expected_out):
        
        for i, chord in enumerate(chords):
            assert chord.name == expected_out[i]['name']
            assert chord.bass_index == expected_out[i]['bass_index']
            assert chord.position == expected_out[i]['position']

    def test_triad_properties(self):
        """Test case to check the properties of triad chords of different qualities and inversions."""

        test_factory = ChordFactory()

        maj_chord_root = test_factory.create_chord('C3, E3, G3')
        maj_chord_fv = test_factory.create_chord('F#0, D1, A0')
        maj_chord_sv = test_factory.create_chord('E5, A5, C#6, E6')

        min_chord_root = test_factory.create_chord('C1, Eb1, G1, Eb2')
        min_chord_fv = test_factory.create_chord('D4, B4, F#5, B5')
        min_chord_sv = test_factory.create_chord('D0, Bb0, G1')

        expected_out = [
            {'name': 'C', 'bass_index': 0, 'position': 0},
            {'name': 'D', 'bass_index': 2, 'position': 1},
            {'name': 'A', 'bass_index': 1, 'position': 2},
            {'name': 'Cm', 'bass_index': 0, 'position': 0},
            {'name': 'Bm', 'bass_index': 1, 'position': 1},
            {'name': 'Gm', 'bass_index': 2, 'position': 2},
        ]
        
        test_triads = [maj_chord_root, maj_chord_fv, maj_chord_sv, min_chord_root, min_chord_fv, min_chord_sv]

        self.compare_properties(test_triads, expected_out)

    def test_seventh_properties(self):
        """Test case to check the properties of seventh chords of different qualities and inversions."""

        test_factory = ChordFactory()

        maj_seventh_root = test_factory.create_chord('Eb2,G2,Bb2,D3')
        maj_seventh_first = test_factory.create_chord('A1,C2,E2,F2')
        dom_seventh_second = test_factory.create_chord('G5,E6,Bb6,C7')
        dom_seventh_third = test_factory.create_chord('C3,F#3,A3,D3')
        min_seventh_root = test_factory.create_chord('E0,B0,D1,G1')
        min_seventh_second = test_factory.create_chord('F4,Ab4,Bb5,Db5')
        halfdim_seventh_first = test_factory.create_chord('B2,E2,G3,C#3')
        halfdim_seventh_third = test_factory.create_chord('F#1,B1,D2,G#2')
        fulldim_seventh_one = test_factory.create_chord('A6,C7,Eb7,Gb7')
        fulldim_seventh_two = test_factory.create_chord('F5,D5,Ab5,Cb6')

        expected_out = [
            {'name': 'Ebmaj7', 'bass_index': 0, 'position': 0},
            {'name': 'Fmaj7', 'bass_index': 3, 'position': 1},
            {'name': 'C7', 'bass_index': 3, 'position': 2},
            {'name': 'D7', 'bass_index': 1, 'position': 3},
            {'name': 'Emin7', 'bass_index': 0, 'position': 0},
            {'name': 'Bbmin7', 'bass_index': 3, 'position': 2},
            {'name': 'C#ø', 'bass_index': 2, 'position': 1},
            {'name': 'G#ø', 'bass_index': 3, 'position': 3},
            {'name': 'Ao7', 'bass_index': 0, 'position': -1},
            {'name': 'Do7', 'bass_index': 0, 'position': -1},
        ]

        test_sevenths = [
            maj_seventh_root, maj_seventh_first, dom_seventh_second, dom_seventh_third, 
            min_seventh_root, min_seventh_second, halfdim_seventh_first, halfdim_seventh_third, 
            fulldim_seventh_one, fulldim_seventh_two
        ]

        self.compare_properties(test_sevenths, expected_out)
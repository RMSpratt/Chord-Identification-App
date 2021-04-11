import csv
import musicInfo as music_info

from collections import defaultdict


class ChordIdentifier:

    #Dictionary holding all of the recognized interval strings comprising a chord
    chord_interval_strings = defaultdict(lambda: {'bass_index': 'unknown', 'quality': 'unknown', 'position': -1})

    def __init__(self):
        self.load_chord_interval_strings()

    def identify_chord(self, interval_string):
        """Returns an object identifying a chord by the passed string of its intervals."""

        return self.chord_interval_strings[interval_string]

    def load_chord_interval_strings(self):
        """This function reads in every valid combination of note intervals forming a chord defined in the chordIntervals.csv file."""
        
        try:

            with open('chordIntervals.csv', 'r') as chord_file:
                
                chord_reader = csv.reader(chord_file)
                next(chord_reader, None)

                for row in chord_reader:

                    #Rows with less than four fields should be ignored
                    if len(row) < 4:
                        continue

                    else:
                        chord_type = ''

                        #If the chord's ID and/or bass_index aren't numerical, the chord is invalid
                        if row[0].isdigit() == False or row[1].isdigit() == False:
                            continue

                        try: 

                            #If the chord's type is valid, get its string representation
                             chord_type = music_info.ChordTypes[row[3]].value

                        except KeyError:
                            continue

                        #Save the chord to the class's list of possible chords
                        self.chord_interval_strings[row[0]] = {'bass_index': int(row[1]), 'quality': chord_type, 'position': int(row[2])}

        except FileNotFoundError:
            print('Error: The chordIntervals.csv file is missing.')


chord_id = ChordIdentifier()

with open('dict.txt', 'w') as fp:

    for key,value in chord_id.chord_interval_strings.items():     
        print(f"\'{key}\': {value},", file=fp)
        # print("\n",file=fp)
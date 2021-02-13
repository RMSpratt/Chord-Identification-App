import collections
import csv

from collections import defaultdict
from chord import Chord

    
def run_main_menu():
    
    user_input = ''

    while user_input != 'q':
        print('Please enter the chord to identify or q to quit.')
        user_input = str(input('Enter each note below separated by a comma.\n\n> '))
        print('')

        if user_input == 'q':
            print('Goodbye!')
            
        else:
            test_chord = Chord(user_input)

            print("-----Chord Information-----")
            test_chord.print_chord_info()
            test_chord.identify_numeral_by_key('F')
            print("")


# run_main_menu()

# music_info.identify_chord_numeral_for_key('F', 'C', 1)
# music_info.identify_chord_numeral_for_key('Bbm', 'Cm', 1)
# music_info.identify_chord_numeral_for_key('C', 'Eb', 2, True)
# music_info.identify_chord_numeral_for_key('Cm', 'Cm', 2)


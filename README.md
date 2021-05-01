# Chord-Identification-App

## Description

This web-hosted Python project provides functionality for identifying chords and analyzing chord progressions using a series of notes entered by the user. Currently the project is being hosted at: https://rmspratt.pythonanywhere.com

The primary features offered the app are listed and described below.

### Identifying Chords
Chords entered by the user are identified to provide its name and numeral relative to a selected key. Major and minor keys are supported, but theoretical keys, i.e. G#+ are excluded for selection.

Currently all of the following chord types are supported for identification:

- Major and minor triads
- Augmented and diminished triads
- Suspended chords (sus2 and sus4)
- Add5 and b5 triads
- Major and minor seventh chords
- Dominant seventh chords
- Half-diminished and fully-diminished seventh chords
- 7b5 chords

Some special cases for chords are checked for by the application and may alter the name or numeral returned for a chord. These are:

- The Neopolitan chord
- The augmented sixth chords
- Applied/Secondary dominants
- Leading tone fully-diminished seventh chords (including inversions)


### Analyzing Chord Progressions 
All of the chords entered by the user are combined into a progression for a selected key so that the progression can be analyzed according to SATB four-part harmony writing rules. Analysis is optional, and any violations to the rules supported by the application are returned for view with appropriate chord and voice indices.

Currently all of the following SATB rules are checked for:
- Voices exceeding their typical note range
- Intervals between voices being too large
- Unresolved leading tones and chordal sevenths
- Doubled leading tones and chordal sevenths
- Parallel 5th and 8ve movement
- Chords unknown to the key

**Note:** I tried to avoid tackling more subjective or less agreed upon rules for progressions such as which chord tones to double depending on chord quality, and the having too many leaps in inner voices or in consecutive chords.

### Rendering Chord Progressions
All of the chords entered by the user are displayed on a musical staff or on multiple staves rendered by the VexFlow library. More information on VexFlow can be found here: https://www.vexflow.com.

An example of a rendered chord progression is below:
![image](https://user-images.githubusercontent.com/10410051/116791560-47656180-aa89-11eb-94d4-dc9128e88b21.png)


## Build and Running Instructions

If you would like to download this app and run it on your local device, please see the steps below. Take note that the application was built using Python 3.8 and may not be compatible with earlier versions of Python.

**Build the application:**
1. Navigate to the Flask sub-folder.
2. Configure a virtual environment with the command:
3. Install the build requirements with the command: pip install -r requirements.txt

**Run the application:**
1. Activate the virtual environment, '. venv/bin/activate' on MAC OS devices.
2. Enter the command 'flask run' from within the Flask sub-directory.
3. Navigate to the localhost link generated.


## Possible Future Updates

While I don't have plans to implement more features to this app at this time, all of the following features could appear if I return to the project:

- Web settings for chord notation when rendered i.e. not using slash chord names, configuring middle-C
- More SATB rule checks including: voice crossing, hidden 5ths and 8ves, parallel unisons
- The ability to read in CSV files of chords for rendering and analysis
- Support for chords with extensions, i.e. 9ths, 11ths, and 13ths

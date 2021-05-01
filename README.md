# Chord-Identification-App

## Description

This web-hosted Python project provides functionality for identifying chords and analyzing chord progressions using a series of notes entered by the user. Currently the project is being hosted at: https://rmspratt.pythonanywhere.com

The primary features offered the app are listed and described below.

**Identifying Chords:** Chords entered by the user are identified to provide its name and numeral relative to a selected key. Major and minor keys are supported, but theoretical keys, i.e. G#+ are excluded for selection.

**Identifying Chords:** All of the chords entered by the user are combined into a progression for a selected key so that the progression can be analyzed according to SATB four-part harmony writing rules. Analysis is optional, and any violations to the rules supported by the application are returned for view with appropriate chord and voice indices.

**Rendering Chord Progressions:** All of the chords entered by the user are displayed on a musical staff or on multiple staves rendered by the VexFlow library. More information on VexFlow can be found here: https://www.vexflow.com.


## Build and Running Instructions

If you would like to download this app and run it on your local device, please see the steps below. Take note that the application was built using Python 3.8 and may not be compatible with earlier versions of Python.

**Build the application:**
1. Navigate to the Flask sub-folder.
2. Configure a virtual environment with the command: 'python3 -m venv venv' or 'py -3 -m venv venv' on Windows.
3. Install the build requirements with the command: pip install -r requirements.txt

**Run the application:**
1. Activate the virtual environment, '. venv/bin/activate' or 'venv\Scripts\activate' on Windows. 
2. Enter the command 'flask run' from within the Flask sub-directory.
3. Navigate to the localhost link generated.

**Note:** If using VS Code, check that you have the correct Python Interpreter selected if you have trouble running the application. I have found that restarting VS Code and re-doing the run steps has also helped in the past when the improper interpreter isn't being used.


## Potential Future Updates

While I don't have plans to implement more features to this app at this time, all of the following features could appear if I return to the project:

- Web settings for chord notation when rendered i.e. not using slash chord names, configuring middle-C
- More clear errors for the client when entering chords to the web form.
- More SATB rule checks including: voice crossing, hidden 5ths and 8ves, parallel unisons
- The ability to read in CSV files of chords for rendering and analysis
- Support for chords with extensions, i.e. 9ths, 11ths, and 13ths


## More Information

More information pertaining to the specifics of the features offered including running instructions can be found in the web app's 'How to Use' and 'SATB Information' pages, or in the Wiki pages in this repository.

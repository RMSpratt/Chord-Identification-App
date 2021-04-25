let VF = Vex.Flow;

function buildStave(key, chords, time, drawMode = 'SATB') {

    //The div to put the music stave svg inside
    let staffDiv = document.getElementById('stave-svg');
    staffDiv.innerHTML = '';

    let noteFormatter = new VF.Formatter();

    let staveInfo;
    let voices;
    let ghostNotes;

    if (drawMode === 'piano') {
        staveInfo = getPianoVoices(chords, time);
        voices = staveInfo[0];
        ghostNotes = staveInfo[1];

        //Format each voice's notes and set their beam direction
        for (let i = 0; i < voices[0].length; i++) {
            for (let j = 0; j < voices.length; j++) {
                noteFormatter
                    .joinVoices([voices[j][i]])
                    .format([voices[j][i]], 375);
                VF.Beam.generateBeams(voices[j][i].tickables);
            }
        }

        drawFullSVG(voices, time, key, 'piano', staffDiv);

    } else {
        staveInfo = getSATBVoices(chords, time);
        voices = staveInfo[0];
        ghostNotes = staveInfo[1];

        //Format each voice's notes and set their beam direction
        for (let i = 0; i < voices[0].length; i++) {
            for (let j = 0; j < voices.length; j++) {
                noteFormatter
                    .joinVoices([voices[j][i]])
                    .format([voices[j][i]], 375);

                if (j === 0 || j === 2) {
                    VF.Beam.generateBeams(voices[j][i].tickables, {
                        stem_direction: -1,
                    });
                } else {
                    VF.Beam.generateBeams(voices[j][i].tickables, {
                        stem_direction: 1,
                    });
                }
            }
        }

        drawFullSVG(voices, time, key, 'SATB', staffDiv);
    }

    //Iterate through the score's ghost notes and hide them
    for (let note_id of ghostNotes) {
        note_id = 'vf-' + note_id;

        let ghostNote = document.getElementById(note_id).childNodes[0];
        ghostNote.setAttribute('class', 'ghost-note');
    }

    let modifierElements = document.getElementsByTagName('text');

    //Set the vertical position of the chord numerals and chord names
    for (let modifier of modifierElements) {
        let modifierText = modifier.innerHTML.toLowerCase();

        if (modifierText.includes('i') || modifierText.includes('v') || modifierText.includes('+') || modifierText.includes('n')) {
            modifier.setAttribute('y', 250);
        } else {
            modifier.setAttribute(
                'y',
                staffDiv.offsetHeight - (staffDiv.offsetHeight - 30)
            );
        }
    }
}

function drawFullSVG(voices, time, key, chordMode, staveSvg) {

    let LEAD_BAR_WIDTH = 450;
    let BAR_WIDTH = 400;

    let barXOffset = 15;
    let trebleYOffset = 25;
    let bassYOffset = 125;

    //Create the svg renderer
    let renderer = new VF.Renderer(staveSvg, VF.Renderer.Backends.SVG);
    let context;

    let numBars = voices[0].length;
    let lineBarCount = 0;

    renderer.resize(1275, 300 + (300 * (Math.floor(numBars / 3))));
    context = renderer.getContext();

    for (let i = 0; i < numBars; i++) {
        let trebleStave;
        let bassStave;
        let ornamentations = [];

        //The first bar of each line draws the key signature and clef
        if (i % 3 === 0) {

            //If this isn't the first line, increment the y offsets and reset the x offset
            if (i > 0) {
                barXOffset = 15;
                trebleYOffset += 300;
                bassYOffset += 300;
            }

            trebleStave = new VF.Stave(barXOffset, trebleYOffset, LEAD_BAR_WIDTH);
            bassStave = new VF.Stave(barXOffset, bassYOffset, LEAD_BAR_WIDTH);

            ornamentations.push(
                new Vex.Flow.StaveConnector(trebleStave, bassStave).setType(3)
            );
            ornamentations.push(
                new Vex.Flow.StaveConnector(trebleStave, bassStave).setType(1)
            );

            trebleStave.addClef('treble').addKeySignature(key);
            bassStave.addClef('bass').addKeySignature(key);

            //The very first bar has the time signature
            if (i == 0) {
                trebleStave.addTimeSignature(time);
                bassStave.addTimeSignature(time);
            }
            barXOffset += 450
        }

        else {
            trebleStave = new VF.Stave(barXOffset, trebleYOffset, BAR_WIDTH);
            bassStave = new VF.Stave(barXOffset, bassYOffset, BAR_WIDTH);
            barXOffset += 400;
        }

        //Add the end barline to the last bar in the progression
        if (i == numBars - 1) {
            ornamentations.push(
                new Vex.Flow.StaveConnector(trebleStave, bassStave).setType(6)
            );
        }

        //Draw both staves and any ornamentations
        trebleStave.setContext(context).draw();
        bassStave.setContext(context).draw();

        for (let ornamentation of ornamentations) {
            ornamentation.setContext(context).draw();
        }

        //Draw the voices according to SATB notation rules
        if (chordMode === 'SATB') {
            voices[0][i].draw(context, bassStave);
            voices[1][i].draw(context, bassStave);
            voices[2][i].draw(context, trebleStave);
            voices[3][i].draw(context, trebleStave);
        }

        //Draw the treble and bass parts for the piano chord voicings
        else {
            voices[0][i].draw(context, trebleStave);
            voices[1][i].draw(context, bassStave);
        }
    }
}

/* Function: getPianoVoices
* Description: This function separates notes in each chord to place them within the treble or bass clef.
*/
function getPianoVoices(chords, timeSignature) {

    //The array of voices in the treble and bass staves to be returned
    let voices = [[], []];

    //All of the notes to be drawn in the treble stave
    let trebleVoiceNotes = [];

    //All of the notes to be drawn in the bass stave
    let bassVoiceNotes = [];

    //All of the ghost notes in the progression
    let ghostNotes = [];

    //The number of bars in the progression
    let barIndex = 0;

    //The number of beats for the current bar
    let barBeatCount = 1;

    //The number of beats maximum allowed in a bar
    let beatsPerBar =
        timeSignature.split('/')[0] * (4 / timeSignature.split('/')[1]);

    //Initialize the trebleVoiceNotes and bassVoiceNotes arrays of arrays
    trebleVoiceNotes.push([]);
    bassVoiceNotes.push([]);

    //Iterate through each chord of the progression
    for (let chord of chords) {
        let accidentals = chord.accidentals;

        let trebleNotes = [];
        let trebleAccidentals = [];
        let bassNotes = [];
        let bassAccidentals = [];

        let newTrebleChord;
        let newBassChord;

        let chordName = new VF.ChordSymbol()
            .addText(chord.name)
            .setVertical('top')
            .setHorizontal('center');

        let chordNumeral = new VF.ChordSymbol()
            .addText(chord.numeral)
            .setVertical('bottom')
            .setHorizontal('center');

        //If the number of beats has exceed the number allowed for the bar, create a new array to hold notes for the next bar
        if (barBeatCount > beatsPerBar) {
            barIndex += 1;
            barBeatCount = 1;
            trebleVoiceNotes.push([]);
            bassVoiceNotes.push([]);
        }

        //1) Separate each chord's notes into the appropriate stave
        chord.notes.forEach(function (note, i) {
            
            //Notes C4 or higher
            if (note.charAt(note.length - 1) >= 4) {
                trebleNotes.push(note);
                trebleAccidentals.push(accidentals[i]);
            }

            //Notes B3 or lower
            else {
                bassNotes.push(note);
                bassAccidentals.push(accidentals[i]);
            }
        });

        //2) Build the Treble clef StaveNote
        if (trebleNotes.length > 0) {
            newTrebleChord = new VF.StaveNote({
                clef: 'treble',
                keys: trebleNotes,
                duration: 'q',
            });
        } else {
            newTrebleChord = new VF.StaveNote({
                clef: 'treble',
                keys: ['b/4'],
                duration: 'q',
            });
            ghostNotes.push(newTrebleChord.attrs.id);
        }

        //3) Build the Bass clef StaveNote
        if (bassNotes.length > 0) {
            newBassChord = new VF.StaveNote({
                clef: 'bass',
                keys: bassNotes,
                duration: 'q',
            });
        } else {
            newBassChord = new VF.StaveNote({
                clef: 'bass',
                keys: ['d/3'],
                duration: 'q',
            });
            ghostNotes.push(newBassChord.attrs.id);
        }

        //4) Add the accidentals for the chord
        trebleAccidentals.forEach((accidental, i) => {
            if (accidental !== '') {
                newTrebleChord.addAccidental(i, new VF.Accidental(accidental));
            }
        });

        bassAccidentals.forEach((accidental, i) => {
            if (accidental !== '') {
                newBassChord.addAccidental(i, new VF.Accidental(accidental));
            }
        });

        //5) Add the chord name and numeral modifiers to the chords created
        newTrebleChord.addModifier(0, chordName);
        newBassChord.addModifier(0, chordNumeral);

        //6) Add the chord to the list of StaveNotes for the current bar
        trebleVoiceNotes[barIndex].push(newTrebleChord);
        bassVoiceNotes[barIndex].push(newBassChord);

        barBeatCount++;
    }

    //Build the arrays of voices to display
    for (let i = 0; i < barIndex + 1; i++) {
        voices[0].push(
            new VF.Voice({ num_beats: 4, beat_value: 4 })
                .setStrict(false)
                .addTickables(trebleVoiceNotes[i])
        );

        voices[1].push(
            new VF.Voice({ num_beats: 4, beat_value: 4 })
                .setStrict(false)
                .addTickables(bassVoiceNotes[i])
        );
    }

    return [voices, ghostNotes];
}

/* Function: getSATBVoices
* Description: This function separates notes in each chord to match SATB voicing rules.
*/
function getSATBVoices(chords, timeSignature) {

    //The array of soprano, alto, tenor, and bass voices to be returned
    let voices = [[], [], [], []];

    let bassNotes = [[]];
    let tenorNotes = [[]];
    let altoNotes = [[]];
    let sopranoNotes = [[]];

    let ghostNotes = [];

    let barIndex = 0;

    let barBeatCount = 1;

    let beatsPerBar =
        timeSignature.split('/')[0] * (4 / timeSignature.split('/')[1]);

    for (let chord of chords) {
        let notes = [];
        let accidentals = chord.accidentals;

        let chordName = new VF.ChordSymbol()
            .addText(chord.name)
            .setVertical('top')
            .setHorizontal('center');

        let chordNumeral = new VF.ChordSymbol()
            .addText(chord.numeral)
            .setVertical('bottom')
            .setHorizontal('center');

        //If the number of beats has exceed the number allowed for the bar, create a new array to hold notes for the next bar
        if (barBeatCount > beatsPerBar) {
            barIndex += 1;
            barBeatCount = 1;
            sopranoNotes.push([]);
            altoNotes.push([]);
            tenorNotes.push([]);
            bassNotes.push([]);
        }

        notes.push(
            new VF.StaveNote({
                clef: 'bass',
                keys: [chord.notes[0]],
                duration: 'q',
            }),
            new VF.StaveNote({
                clef: 'bass',
                keys: [chord.notes[1]],
                duration: 'q',
            }),
            new VF.StaveNote({
                clef: 'treble',
                keys: [chord.notes[2]],
                duration: 'q',
            }),
        );

        //Catch chords with a missing voice
        if (chord.notes.length >= 4) {
            notes.push(
                new VF.StaveNote({
                    clef: 'treble',
                    keys: [chord.notes[3]],
                    duration: 'q',
                })
            )
        }

        else {
            let ghostNote = new VF.StaveNote({
                clef: 'bass',
                keys: ['d/3'],
                duration: 'q',
            });

            notes.push(ghostNote);
            ghostNotes.push(ghostNote.attrs.id);
        }

        accidentals.forEach((accidental, i) => {
            
            if (accidental !== '') {
                notes[i].addAccidental(0, new VF.Accidental(accidental));
            }
        });

        //Add the name and numeral to the notes of the chord
        notes[3].addModifier(0, chordName);
        notes[0].addModifier(0, chordNumeral);

        //Save each note to the appropriate voice
        bassNotes[barIndex].push(notes[0]);
        tenorNotes[barIndex].push(notes[1]);
        altoNotes[barIndex].push(notes[2]);
        sopranoNotes[barIndex].push(notes[3]);

        barBeatCount++;
    }

    //Build the voice line for each bar of the progression
    for (let i = 0; i < barIndex + 1; i++) {
        voices[0].push(
            new VF.Voice({ num_beats: 4, beat_value: 4 })
                .setStrict(false)
                .addTickables(bassNotes[i])
        );

        voices[1].push(
            new VF.Voice({ num_beats: 4, beat_value: 4 })
                .setStrict(false)
                .addTickables(tenorNotes[i])
        );

        voices[2].push(
            new VF.Voice({ num_beats: 4, beat_value: 4 })
                .setStrict(false)
                .addTickables(altoNotes[i])
        );

        voices[3].push(
            new VF.Voice({ num_beats: 4, beat_value: 4 })
                .setStrict(false)
                .addTickables(sopranoNotes[i])
        );
    }
    return [voices, ghostNotes];
}


$('#chord-form-submit').click(function(e) {
    e.preventDefault();

    let formData = new FormData(document.getElementById('chord-builder-form'));

    $.ajax({
        url: '/analysis',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,

        success: function(data) {
            
            if (!data.chords.error) {
                buildStave(data.key, data.chords.chords, data.time, data.displayForm);
            }
        }
    });   
});
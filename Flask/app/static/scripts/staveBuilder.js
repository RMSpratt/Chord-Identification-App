let VF = Vex.Flow;

/* Function: buildStave
 * Description: This function is responsible for gathering the information for VexFlow to draw the musical stvae
 * with the chords provided by the user. 
 *
 * Parameters:
 *     key - The key that the chord progression is written in
 *     chords - The array of chords for the progression
 *     time - The time signature the chord progression is written for
 *     drawMode - Controls how the notes of each chord will appear on the stvae
*/ 
function buildStave(key, chords, time, drawMode) {

    //The div to put the music stave svg inside
    let staffDiv = document.getElementById('stave-svg');
    staffDiv.innerHTML = '';

    let noteFormatter = new VF.Formatter();

    //Information for drawing the stave
    let staveInfo;
    let voices;
    let ghostNotes;
    let beatsPerLine = time.split('/')[0] * 3;

    //Draw the progression with chords following typical piano score notation
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

    } 
    
    //Draw the progression with chords following typical four-part (SATB) harmony notation
    else {
        staveInfo = getSATBVoices(chords, time);
        voices = staveInfo[0];
        ghostNotes = staveInfo[1];

        for (let i = 0; i < voices[0].length; i++) {
            for (let j = 0; j < voices.length; j++) {
                noteFormatter
                    .joinVoices([voices[j][i]])
                    .format([voices[j][i]], 375);

                //Bass and alto voices have stems facing downwards
                if (j % 2 === 0) {
                    VF.Beam.generateBeams(voices[j][i].tickables, {
                        stem_direction: -1,
                    });
                } 
                
                //Tenor and soprano voices have stems facing upwards
                else {
                    VF.Beam.generateBeams(voices[j][i].tickables, {
                        stem_direction: 1,
                    });
                }
            }
        }

        drawFullSVG(voices, time, key, 'SATB', staffDiv);
    }

    //Iterate through the score's ghost notes and set their class so they can be hidden
    for (let note_id of ghostNotes) {
        note_id = 'vf-' + note_id;

        let ghostNote = document.getElementById(note_id).childNodes[0];
        ghostNote.setAttribute('class', 'ghost-note');
    }

    let modifierCount = 0;

    //Adjust the y-position of the chord names and numerals so they appear consistently
    for (let modifier of document.getElementsByTagName('text')) {
        let modifierText = modifier.innerHTML.toLowerCase();

        //Each new barline uses an additional offset amount for the height of the stave
        let barLineOffset = drawMode === 'piano' ? 300 : 325;
        let yOffset = Math.floor(modifierCount / (beatsPerLine * 2));

        let chordNameY = 35 + (yOffset * barLineOffset);    
        let chordNumeralY = drawMode === 'piano' ? 250 : 275;
        chordNumeralY +=  yOffset * barLineOffset;

        //Chord symbols appear below a stave
        if (modifierText.includes('i') || modifierText.includes('v') || modifierText.includes('+') || modifierText.includes('n')) {
            modifier.setAttribute('y', chordNumeralY);
        } 
        
        //Chord names appear above a stave
        else {
            modifier.setAttribute('y', chordNameY);
        }
        modifierCount++;
    }
}


function displaySATBErrors(errors) {
    console.log(errors);

    let satbErrorPanel = document.getElementById('satb-error-panel');
    satbErrorPanel.innerHTML = '';

    let satbErrorHeader = document.createElement('h2');
    satbErrorHeader.innerText = 'SATB Voice Leading Errors'
    
    satbErrorPanel.appendChild(satbErrorHeader);

    for (let error of errors) {
        let errorMsg = document.createElement('p');
        errorMsg.innerText = error;

        satbErrorPanel.appendChild(errorMsg);
    }

    document.getElementsByTagName('main')[0].append(satbErrorPanel);
}


/* Function: drawFullSVG
 * Description: This function draws the full stave SVG using the Vexflow and music notation 
 * information provided. 
 *
 * Parameters:
 *     voices - The array of voices containing a line of notes to draw for each chord
 *     time - The time signature of the progression
 *     key - The key signature of the progression
 *     chordMode - The format for chords in the progression (piano or SATB)
 *     staveSVG - The musical stave (svg) to populate with notes
*/ 
function drawFullSVG(voices, time, key, chordMode, staveSvg) {

    //Values defining the alignment and sizing of bars in the full stave
    let leadBarWidth = 450;
    let barHeight = chordMode === 'piano' ? 300 : 325;
    let barWidth = 400;

    let barXOffset = 15;
    let trebleYOffset = 25;
    let bassYOffset = chordMode === 'piano' ? 125 : 150;

    //The number of bars is determined by the length of the voice arrays (all same length)
    let numBars = voices[0].length;

    //Create the VexFlow svg renderer
    let renderer = new VF.Renderer(staveSvg, VF.Renderer.Backends.SVG);
    let context;

    renderer.resize(1275, barHeight + (barHeight * (Math.floor(numBars / 3))));
    context = renderer.getContext();

    for (let i = 0; i < numBars; i++) {
        let trebleStave;
        let bassStave;
        let ornamentations = [];

        //The first bar of each line draws the key signature and clef
        if (i % 3 === 0) {

            //If this isn't the first line of bars, increment the y offsets and reset the x offset
            if (i > 0) {
                barXOffset = 15;
                trebleYOffset += barHeight;
                bassYOffset += barHeight;
            }

            trebleStave = new VF.Stave(barXOffset, trebleYOffset, leadBarWidth);
            bassStave = new VF.Stave(barXOffset, bassYOffset, leadBarWidth);

            //Add the connecting barline decorators and clef and key signatures
            ornamentations.push(
                new Vex.Flow.StaveConnector(trebleStave, bassStave).setType(3)
            );
            ornamentations.push(
                new Vex.Flow.StaveConnector(trebleStave, bassStave).setType(1)
            );

            trebleStave.addClef('treble').addKeySignature(key);
            bassStave.addClef('bass').addKeySignature(key);

            //Add the time signature to the very first bar
            if (i == 0) {
                trebleStave.addTimeSignature(time);
                bassStave.addTimeSignature(time);
            }
            barXOffset += 450
        }

        //Draw a new middle or end bar in a line
        else {
            trebleStave = new VF.Stave(barXOffset, trebleYOffset, barWidth);
            bassStave = new VF.Stave(barXOffset, bassYOffset, barWidth);
            barXOffset += 400;
        }

        //Add the ending barline to the last bar in the progression
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
* Description: This function separates notes in each chord to place them according to
* typical piano voice notation. 
* 
* Notes of value C4 or less will be drawn relative to the bass stave.
* Notes of value C#4 or greater will be drawn relative to the treble stave.
*/
function getPianoVoices(chords, timeSignature) {

    //The array of voices in the treble and bass staves to be returned
    let voices = [[], []];

    //All of the notes to be drawn in the treble and bass staves respectively
    let trebleVoiceNotes = [];
    let bassVoiceNotes = [];

    //All of the ghost notes in the progression (used for proper formatting)
    let ghostNotes = [];

    //The number of bars in the progression
    let barCount = 0;

    //The number of beats for the current bar
    let barBeatCount = 1;

    //The number of beats maximum allowed in a bar
    let beatsPerBar =
        timeSignature.split('/')[0] * (4 / timeSignature.split('/')[1]);

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
            barCount += 1;
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

        //2) Build the Treble clef StaveNote or GhostNote if no notes are >= C4
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

        //3) Build the Bass clef StaveNote or GhostNote if no notes are < C4
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
        trebleVoiceNotes[barCount].push(newTrebleChord);
        bassVoiceNotes[barCount].push(newBassChord);

        barBeatCount++;
    }

    //7) Build the arrays of voices to display
    for (let i = 0; i < barCount + 1; i++) {
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

    //Each voice's set of notes
    let bassNotes = [[]];
    let tenorNotes = [[]];
    let altoNotes = [[]];
    let sopranoNotes = [[]];

    //All of the ghost notes in the progression (used for proper formatting)
    let ghostNotes = [];

    //The number of bars in the progression
    let barCount = 0;

    //The number of beats for the current bar
    let barBeatCount = 1;

    //The number of beats maximum allowed in a bar
    let beatsPerBar =
        timeSignature.split('/')[0] * (4 / timeSignature.split('/')[1]);

    //1) Create a set of StaveNotes for every chord
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

        //If the number of beats in a bar exceeds the maximum, create new bar arrays
        if (barBeatCount > beatsPerBar) {
            barCount += 1;
            barBeatCount = 1;
            sopranoNotes.push([]);
            altoNotes.push([]);
            tenorNotes.push([]);
            bassNotes.push([]);
        }

        //2) Create a StaveNote for every voice
        for (let i = 0; i < 4; i++) {
    
            if (i < chord.notes.length) {

                //Bass and Tenor voices are drawn in the bass stave
                if (i < 2) {
                    notes.push(
                        new VF.StaveNote({
                            clef: 'bass',
                            keys: [chord.notes[i]],
                            duration: 'q',
                        })
                    ) 
                }

                //Alto and Soprano voices are drawn in the treble stave
                else {
                    notes.push(
                        new VF.StaveNote({
                            clef: 'treble',
                            keys: [chord.notes[i]],
                            duration: 'q',
                        })
                    )
                }
            }

            //If less than four voices were provided, create 'ghost' notes for those missing
            else {
                let ghostNote = new VF.StaveNote({
                    clef: 'treble',
                    keys: ['b/4'],
                    duration: 'q',
                });

                notes.push(ghostNote);
                ghostNotes.push(ghostNote.attrs.id);
            }
        }

        //3) Add accidentals to notes
        accidentals.forEach((accidental, i) => {
            
            if (accidental !== '') {
                notes[i].addAccidental(0, new VF.Accidental(accidental));
            }
        });

        //4) Add the name and numeral to the notes of the chord
        notes[3].addModifier(0, chordName);
        notes[0].addModifier(0, chordNumeral);

        //5) Save each StaveNote to the appropriate voice
        bassNotes[barCount].push(notes[0]);
        tenorNotes[barCount].push(notes[1]);
        altoNotes[barCount].push(notes[2]);
        sopranoNotes[barCount].push(notes[3]);

        barBeatCount++;
    }

    //6) Build the voice line for each bar of the progression
    for (let i = 0; i < barCount + 1; i++) {
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


//Callback function to respond to the user submitting a chord progression for analysis
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
            
            //If the chord progression information was returned successfully, build the Stave svg
            if (!data.chords.error) {
                buildStave(data.key, data.chords.chords, data.time, data.displayForm);
                
                
                if (data.chords.satb_errors) {
                    displaySATBErrors(data.chords.satb_errors);
                }
            }
        }
    });   
});
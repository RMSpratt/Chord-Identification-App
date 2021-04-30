from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FieldList, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError

class ProgressionBuilderForm(FlaskForm):

    #Key signature select
    key = SelectField('Key:', choices=
    [
        ('C','C Major'),('G','G Major'),('D','D Major'),('A','A Major'),('E','E Major'),
        ('B','B Major'),('F#','F# Major'),('C#','C# Major'),('F','F Major'),('Bb','Bb Major'),
        ('Eb','Eb Major'),('Ab','Ab Major'),('Db','Db Major'),('Gb','Gb Major'),('Cb','Cb Major'),
        ('a','A minor'),('E','E minor'),('b','B minor'),('F#','F# minor'),('C#','C# minor'),
        ('G#','G# minor'),('D#','D# minor'),('A#','A# minor'),('D','D minor'),('G','G minor'),
        ('C','C minor'),('F','F minor'),('Bb','Bb minor'),('Eb','Eb minor'),('Ab','Ab minor'),
    ], id='key-options')

    #Time signature select
    time = SelectField('Time:', choices=[('4/4','4/4'),('3/4','3/4'),('5/4','5/4')], id='time-options')

    #Field list for chord inputs
    chords = FieldList(StringField('Chord:'), min_entries=8, max_entries=24)

    #Chord organisation display options
    display_options = RadioField('Chord Display Format:', choices=[('piano','Piano'),('SATB','SATB')], default='piano')

    analyze_satb = BooleanField('Analyze voice leading for SATB rules')

    #Generate Progression, submit option
    submit = SubmitField('Draw Progression', id='form-submit')

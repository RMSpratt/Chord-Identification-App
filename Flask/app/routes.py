from app import app
from flask import render_template, request, Response, redirect, url_for
from api import musicFuncs 
from .forms import ProgressionBuilderForm
#Note: Routes must precede the function they are related to
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])

def index():
    form = ProgressionBuilderForm()
    return render_template('index.html', form=form)

@app.route('/analysis', methods=['POST',])
def analysis():

    form = ProgressionBuilderForm(request.form)
    chords = form.chords.data
    key_signature = form.key.data
    time_signature = form.time.data
    display_format = form.display_options.data or 'piano'
    analyze_satb = form.analyze_satb.data

    progression_info = musicFuncs.analyze_progression(chords, key_signature, analyze_satb)

    return {'chords': progression_info, 'time': time_signature, 'key': key_signature, 'displayForm': display_format}


@app.route('/how_to')
def how_to():
    return render_template('howTo.html')
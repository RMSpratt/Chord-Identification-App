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
    key = form.key.data
    time = form.time.data
    display_format = form.display_options.data or 'piano'

    progression_info = musicFuncs.analyze_progression(chords, key)

    return {'chords': progression_info, 'time': time, 'key': key, 'displayForm': display_format}


@app.route('/how_to')
def how_to():
    return render_template('howTo.html')
from app import app
from flask import render_template, request, Response, redirect, url_for
from api import musicFuncs 

#Note: Routes must precede the function they are related to
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])

def index():

    return render_template('index.html')

@app.route('/analysis', methods=["POST",])
def analysis():

    chords = request.form.get('chords')
    key = request.form.get('key')
    time = request.form.get('time')

    chords = chords.split('|')
    
    progression_info = musicFuncs.analyze_progression(chords, key)

    return {'chords': progression_info, 'time': time, 'key': key}
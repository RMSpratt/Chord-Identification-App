from app import app
from flask import render_template, request, Response, redirect, url_for
from api import musicFuncs 

#Note: Routes must precede the function they are related to
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])

def index():

    chords = request.form.getlist('chord')
    key = request.form.get('key')
    time = request.form.get('time')

    print(f'Key: {key} and chords: {chords}')

    progression_info = musicFuncs.analyze_progression(chords, key)

    return render_template('index.html', data={'chords': progression_info, 'key': key, 'time': time})


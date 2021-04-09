from app import app
from flask import render_template, request, Response
from api import musicFuncs 

#Note: Routes must precede the function they are related to
@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/analysis', methods=['GET'])
def analysis():

    notes = request.args.get('notes')

    try: 
        chord_name = musicFuncs.analyze_chord(notes) 

    except:
        chord_name = 'Invalid'

    return render_template('analysis.html', data={"notes": chord_name})


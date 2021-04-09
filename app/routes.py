from app import app
from flask import render_template, request, Response
from api import requests 

#Note: Routes must precede the function they are related to
@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/analysis', methods=['GET'])
def analysis():

    notes = request.args.get('notes')

    return render_template('analysis.html', data={"notes": 'C3'})
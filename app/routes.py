from flask import render_template, request
import requests
import json
from app import app
from app.forms import SearchSpotifyform

@app.route('/', methods=['GET', 'POST'])
def index():

    Spotifyform=SearchSpotifyform()


    if request.method == 'GET':
        return render_template('index.html',
                               Spotifyform=Spotifyform)
    elif request.method == 'POST':

        if Spotifyform.validate():
            return render_template('result.html',
                                   )


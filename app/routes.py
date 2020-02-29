from flask import render_template, request
import requests
import json
import configparser
from app import app
from app.forms import SearchSpotifyform

@app.route('/', methods=['GET', 'POST'])
def index():

    Spotifyform=SearchSpotifyform()


    if request.method == 'GET':
        return render_template('index.html',
                               Spotifyform=Spotifyform)
    elif request.method == 'POST':

        return render_template('result.html')


from flask import render_template, request
import requests
import json
from app import app
from app.forms import SearchSpotifyform
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

def trackInfoBasic(tracks):
    names = [trackName['track']['name'] for trackName in tracks['items']]
    uris = [trackURI['track']['id'] for trackURI in tracks['items']]

    return {'names': names, 'uris': uris}

def get_sp_client():

    client = 'f4d25f2bdfee4094a7d93f0ec7e4f264'
    secret = '520f13ab9f7747919d705f2ccc5dcd2b'
    username = 'jup118'

    client_credentials_manager = SpotifyClientCredentials(client_id=client, client_secret=secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return sp


def getFeatures(sp, songData):
    playlistURI = songData['uris']
    songNames = songData['names']
    audioFeaturesRaw = sp.audio_features(playlistURI)

    danceability = []
    energy = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    duration_ms = []
    time_signature = []
    uris = []

    for track in audioFeaturesRaw:
        #         print(track)
        danceability.append(track['danceability'])
        energy.append(track['energy'])
        key.append(track['key'])
        loudness.append(track['loudness'])
        mode.append(track['mode'])
        speechiness.append(track['speechiness'])
        instrumentalness.append(track['instrumentalness'])
        liveness.append(track['liveness'])
        valence.append(track['valence'])
        tempo.append(track['tempo'])
        duration_ms.append(track['duration_ms'])
        time_signature.append(track['time_signature'])
        uris.append(track['uri'])

    playlistFeatures = {
        'danceability': danceability,
        'energy': energy,
        'key': key,
        'loudness': loudness,
        'mode': mode,
        'speechiness': speechiness,
        'liveness': liveness,
        'valence': valence,
        'tempo': tempo,
        'duration_ms': duration_ms,
        'time_signature': time_signature,
        'uris': uris,
        'playlistURI': playlistURI,
        'songNames': songNames
    }

    return playlistFeatures


@app.route('/', methods=['GET', 'POST'])
def index():

    Spotifyform=SearchSpotifyform()

    # Hardcoded
    user = 'jup118'
    playlistId = '0iGABH7qHUQpHsz0yaUxTV'
    startingTrackNum = 4

    sp = get_sp_client()
    playlistTracks = sp.user_playlist_tracks(user, playlistId)

    # 1. Get Playlist Data
    trackData = trackInfoBasic(playlistTracks)

    #2. Get features
    trackFeaturesDict = getFeatures(sp, trackData)
    print(trackFeaturesDict)

    #


    if request.method == 'GET':

        return render_template('index.html',
                               Spotifyform=Spotifyform)
    elif request.method == 'POST':

        if Spotifyform.validate():
            return render_template('result.html',
                                   )


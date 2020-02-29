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

def getOneFeature(sp, songURI):
    audioFeaturesRaw = sp.audio_features(songURI)[0]

    return audioFeaturesRaw

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

    trackList = []

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

        trackList.append(track)

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

    return trackList, playlistFeatures

def getRecommendations(sp, seedURI, val):
    print(seedURI)
    print(val)

    recommendations = sp.recommendations(seed_tracks=[seedURI], target_danceability=val)
    print(recommendations)
    # print(recommendations['tracks'][0]['name'])

    return

@app.route('/', methods=['GET', 'POST'])
def index():

    Spotifyform=SearchSpotifyform()

    # Hardcoded
    user = 'jup118'
    playlistId = '0iGABH7qHUQpHsz0yaUxTV'
    startingTrackNum = 4
    seedSongId = '7tSCXqS0evaolLl3jIuodQ'

    sp = get_sp_client()
    playlistTracks = sp.user_playlist_tracks(user, playlistId)

    # 1. Get Playlist Data
    trackData = trackInfoBasic(playlistTracks)

    #2. Get features
    trackList, trackFeaturesDict = getFeatures(sp, trackData)

    # print(trackList[startingTrackNum])
    #3. Get features for seed Song
    seedSongData = getOneFeature(sp, seedSongId)
    print(seedSongData['id'])
    newSongs = []

    for i in range(startingTrackNum-1, len(trackList)-1):

        benchmarkDance = trackList[i]['danceability']
        nextDance = trackList[i+1]['danceability']
        danceDiff = round(benchmarkDance-nextDance, 3)

        targetVal = seedSongData['danceability']+danceDiff

        recSong = getRecommendations(sp, seedSongData['id'], targetVal)
        newSongs.append(recSong)
        break






    # Get difference from

    #3.


    if request.method == 'GET':

        return render_template('index.html',
                               Spotifyform=Spotifyform)
    elif request.method == 'POST':

        if Spotifyform.validate():
            return render_template('result.html',
                                   )


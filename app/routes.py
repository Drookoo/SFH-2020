from flask import render_template, request
import requests
import json
from app import app
from app.forms import SearchSpotifyform
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from dotenv import load_dotenv
import os

load_dotenv()

# SPOT_TOKEN = os.getenv("SPOTIFY_TOKEN")
SPOT_TOKEN = 'BQCOMAVr2bcb2sbjtISSniYCdr1e7OqfArfrTPn74czcApyYyiNaSrU-if4b0b-NfyEfbSqlHju8Lw7SfdtHBn6tGdS2kV54LVRmvFhWSNnlLr4vOouqJX6SXa4BIBxt_NdPSv3gxmY3Fc4D0UnXV5RA-iU9hBoFd3P-nKIai-H1fye76ffsbVnONA3dlohu3LvSn-QZxZfQIlXPhRs105ojD7mjLpDBNgN9B8fzStbmlOq2'


def trackInfoBasic(tracks):
    names = [trackName['track']['name'] for trackName in tracks['items']]
    uris = [trackURI['track']['id'] for trackURI in tracks['items']]

    return {'names': names, 'uris': uris}

def get_sp_client():

    client = 'f4d25f2bdfee4094a7d93f0ec7e4f264'
    secret = '520f13ab9f7747919d705f2ccc5dcd2b'
    username = 'jup118'
    scope = 'playlist-read-private playlist-modify-public playlist-read-private playlist-modify-private'

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
    # print(seedURI)
    # print(val)

    recommendations = sp.recommendations(seed_tracks=[seedURI], target_danceability=val)
    # print(recommendations)
    # print(recommendations['tracks'][0]['id'])

    return recommendations['tracks'][0]['id']

def createPlaylist(sp):


    headers = {
        'Authorization': 'Bearer ' + SPOT_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'

    }

    data = '{"name":"API_TEST_playlist", "public":true, "description":"A playlist for sunflower hack"}'

    response = requests.post('https://api.spotify.com/v1/users/jup118/playlists',
                             headers=headers, data=data)
    playlistId = response.json()['id']
    return playlistId

def addSongstoPlaylist(songURIs, playlistId):

    sp = spotipy.Spotify(auth=SPOT_TOKEN)

    sp.user_playlist_add_tracks('jup118', playlistId, songURIs)


@app.route('/home', methods=['GET', 'POST'])
def home():
    Spotifyform=SearchSpotifyform()
    print("IN HOME")
    if request.method == 'GET':

        return render_template('index.html',
                               Spotifyform=Spotifyform)
    elif request.method == 'POST':

        if Spotifyform.validate():
            return render_template('result.html',
                                   )

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
    pointToEnd = []
    beginToPoint = []

    seedSongURI = seedSongId
    for i in range(startingTrackNum-1, len(trackList)-1):

        seedSongData = getOneFeature(sp, seedSongURI)

        benchmarkDance = trackList[i]['danceability']
        nextDance = trackList[i+1]['danceability']
        danceDiff = round(benchmarkDance-nextDance, 3)

        targetVal = seedSongData['danceability']+danceDiff

        recSong = getRecommendations(sp, seedSongData['id'], targetVal)
        pointToEnd.append(recSong)

    for i in range(startingTrackNum-1, 0, -1):
        seedSongData = getOneFeature(sp, seedSongId)

        benchmarkDance = trackList[i]['danceability']
        nextDance = trackList[i+1]['danceability']
        danceDiff = round(benchmarkDance-nextDance, 3)

        targetVal = seedSongData['danceability'] + danceDiff

        recSong = getRecommendations(sp, seedSongData['id'], targetVal)
        beginToPoint.insert(0, recSong)

    finalPlaylistSongs = beginToPoint + [seedSongId] + pointToEnd

    newPlaylistId = createPlaylist(sp)

    addSongstoPlaylist(finalPlaylistSongs, newPlaylistId)



    if request.method == 'GET':

        return render_template('index.html',
                               Spotifyform=Spotifyform)
    elif request.method == 'POST':

        if Spotifyform.validate():
            return render_template('result.html',
                                   )


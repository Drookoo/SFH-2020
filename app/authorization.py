import spotipy
import spotipy.util as util
import requests
import os

from dotenv import load_dotenv

token = 'BQDVjpa-SH4tDkOpJpTwTNzBTPSFzfF0yCe3KRkoP4GAw4B1QilbiG92uY51zhYnd-6w_bn0VdmerjXJ297ENoCPJtkdAvB6SJF8G9PjcBium4xfpJSBLsIWSAX6hV3jDCv4AHXOlg-gC60bxKvfBFeoTGKey7ENWsrhyviRqhtBAtijFqs2bw_k8Wi179v9T5AvLEX9PpyhenZfHSls'

client = 'f4d25f2bdfee4094a7d93f0ec7e4f264'
secret = '520f13ab9f7747919d705f2ccc5dcd2b'
username = 'jup118'
scope = 'playlist-read-private playlist-modify-public playlist-read-private playlist-modify-private'

token = util.prompt_for_user_token(username, scope, client_id=client, client_secret=secret, redirect_uri='http://localhost/')

os.environ['SPOTIFY_TOKEN'] = token
print(token)
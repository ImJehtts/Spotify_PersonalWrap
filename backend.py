#backend
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
from datetime import datetime
import sys 

client_id = 'HIDDEN'
client_secert = 'HIDDEN'
redirect_uri = 'HIDDEN'

scope = 'user-top-read'

spotify_auth = SpotifyOAuth(client_id, client_secert, redirect_uri, scope=scope)

auth_url = spotify_auth.get_authorize_url()

webbrowser.open(auth_url)

redirect_url = input("Please paste redirect url: ")

if redirect_url.split('=')[1] == "access_denied":
   print("Access was denied ")
   sys.exit()

authorization_code = spotify_auth.parse_response_code(redirect_url)

tokens = spotify_auth.get_access_token(authorization_code)

def search(tokens,range):
    if tokens:
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        expires_at = datetime.now().timestamp() + tokens['expires_in']

        spotify = spotipy.Spotify(auth=access_token)

        results = spotify.current_user_top_tracks(limit=25, time_range=range)

        top_songs_dictionary = {}

        for index, item in enumerate(results['items']):
            track_name = item['name']
            album_cover_image = item['album']['images'][0]['url']
            artists = ""
            for artist in item['artists']:
                artists += artist['name'] + ', '
            artists = artists[:-2]
            song_information = [track_name, artists, album_cover_image]

            top_songs_dictionary[str(index + 1)] = song_information

        if datetime.now().timestamp() > expires_at - 300:
            tokens = spotify_auth.refresh_access_token(refresh_token)
            access_token = tokens['access_token']
            expires_at = datetime.now().timestamp() + tokens['expires_in']
            spotify = spotipy.Spotify(auth=access_token)
            print("access token refreshed")

    else:
        print("Authorization did not work.")

    return top_songs_dictionary


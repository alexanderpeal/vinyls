import base64
import requests
from django.conf import settings
from urllib.parse import urlencode

class SpotifyAuth:
    AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    @staticmethod
    def get_auth_url():
        params = {
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'scope': 'user-library-read playlist-read-private user-read-private user-read-email',
        }
        auth_url = f"{SpotifyAuth.AUTHORIZE_URL}?{urlencode(params)}"
        print(f"Generated Auth URL: {auth_url}")  # Debug print
        print(f"Redirect URI: {settings.SPOTIFY_REDIRECT_URI}")  # Debug print
        return auth_url
    
    @staticmethod
    def get_token(code):
        auth_header = base64.b64encode(
            f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
            .encode('ascii')).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        }

        response = requests.post(SpotifyAuth.TOKEN_URL, headers=headers, data=data)
        return response.json()

    @staticmethod
    def get_user_profile(access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        return response.json()
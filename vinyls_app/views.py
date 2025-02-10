from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .spotify_auth import SpotifyAuth

def spotify_login(request):
    auth_url = SpotifyAuth.get_auth_url()
    return redirect(auth_url)

def spotify_callback(request):
    error = request.GET.get('error')
    if error:
        print(f"Spotify Error: {error}")
        return HttpResponse(f"Error: {error}")
        
    code = request.GET.get('code')
    if code:
        token_info = SpotifyAuth.get_token(code)
        if 'error' in token_info:
            print(f"Token Error: {token_info}")
            return HttpResponse(f"Token Error: {token_info['error']}")

        request.session['spotify_token'] = token_info
        return redirect('/')  # Redirect to root URL instead of using named URL
    
    return HttpResponse("No code received from Spotify")

# Create your views here.
def home(request):
    token_info = request.session.get('spotify_token')
    
    if token_info and 'access_token' in token_info:
        # Get user profile if authenticated
        user_profile = SpotifyAuth.get_user_profile(token_info['access_token'])
        return render(request, 'home.html', {
            'is_authenticated': True,
            'username': user_profile.get('display_name', 'Unknown User')
        })
    
    return render(request, 'home.html', {'is_authenticated': False})
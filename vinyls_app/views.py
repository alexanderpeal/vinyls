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

# --- Views for app below ---

def home(request):
    token_info = request.session.get('spotify_token')
    
    # If authenticated, render home.html
    if token_info and 'access_token' in token_info:
        user_profile = SpotifyAuth.get_user_profile(token_info['access_token'])
        
        profile_image_url = None
        if user_profile.get('images'):
            profile_image_url = user_profile['images'][0]['url']
        
        context = {
            'username': user_profile.get('display_name', 'Unknown User'),
            'profile_image_url': profile_image_url
        }
        
        return render(request, 'home.html', context)
    
    # Otherwise, render landing.html
    return render(request, 'landing.html')

def logout_view(request):
    if 'spotify_token' in request.session:
        del request.session['spotify_token']
    
    return redirect('/')
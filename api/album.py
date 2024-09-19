import requests
from typing import List, Tuple
from secrets import CLIENT_ID, CLIENT_SECRET


# Get access token to use Spotify API
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
ACCESS_TOKEN = response.json()["access_token"]


def getListOfSongs(id: str, endpoint: str="https://api.spotify.com/v1/playlists/") -> Tuple[List[str], List[str]]:
    """Function used for generating lists of track names and artist names using Spotify API.

    Args:
        id (str): ID required by the Spotify endpoint. In default case playlist ID.
        endpoint (_type_, optional): Endpoint link. Defaults to "https://api.spotify.com/v1/playlists/".

    Returns:
        Tuple[List[str], List[str]]: list of track names and list of artist names
    """
    # Get response from Spotify API
    url = endpoint + id
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    # Get artists and tracks from response
    tracks = []
    artists = []
    for track in response.json()["tracks"]["items"]:
        
        track_artists = []
        for artist in track["track"]["artists"]:
            track_artists.append(artist['name'])

        tracks.append((track["track"]["name"]))
        artists.append(", ".join(track_artists))

    return tracks, artists


tracks, artists = getListOfSongs("37i9dQZEVXbN6itCcaL3Tt") # Top 50 - Poland

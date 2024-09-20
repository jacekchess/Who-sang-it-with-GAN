import requests
import lyricsgenius
from typing import List, Tuple
from secrets import CLIENT_ID_SPOTIFY, CLIENT_SECRET_SPOTIFY, ACCESS_TOKEN_GENIUS


# Get access token to use Spotify API
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = f"grant_type=client_credentials&client_id={CLIENT_ID_SPOTIFY}&client_secret={CLIENT_SECRET_SPOTIFY}"
response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
ACCESS_TOKEN_SPOTIFY = response.json()["access_token"]


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
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN_SPOTIFY}"}
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


def writeSongLyrics(tracks: List[str], artists: List[str], directory: str="data/raw/") -> None:
    """Function used for writing lyrics of the songs to the destined directory

    Args:
        tracks (List[str]): List of song titles (provided by getListOfSongs)
        artists (List[str]): List of artists (provided by getListOfSongs)
        directory (str, optional): Path to the place where lyrics will be saved. Defaults to "data/raw/".
    """
    # Access Genius API with dedicated library
    genius = lyricsgenius.Genius(ACCESS_TOKEN_GENIUS)

    for track, artist in zip(tracks, artists):
        try:
            song = genius.search_song(track, artist)
            if song:
                lyrics = song.lyrics
                with open(f"{directory}{track}.txt", "w+", encoding="utf-8") as f:
                    f.write(f"{track} - {artist}\n{lyrics}")
                
        except Exception as e:
            print(f"Exception {e} for song {track}.")


# tracks, artists = getListOfSongs("37i9dQZEVXbN6itCcaL3Tt") # Top 50 - Poland
# writeSongLyrics(tracks, artists)

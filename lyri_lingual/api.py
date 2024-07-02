"""Fetch track data and translations from API."""

from pathlib import Path

import requests
import toml
import deepl

from lyri_lingual.structures import TrackData

BASE_URL = "https://api.musixmatch.com/ws/1.1/"
MUSIX_API_KEY = None  # still initialized when imported
DEEPL_API_KEY = None

def _init_api_key(file_path: Path) -> None:
    """
    Parses a TOML file to retrieve the value of the specified API key.

    :param file_path: Path to the config TOML file.
    :return: The API key as a string if found, otherwise None.
    """
    with open(file_path, "r") as file:
        config = toml.load(file)
        global MUSICX_API_KEY
        global DEEPL_API_KEY
        MUSICX_API_KEY = config.get("musixmatch_api_key")
        DEEPL_API_KEY = config.get("deepl_api_key")

def _query_api(endpoint: str, params: dict) -> dict:
    """
    Function to get data from the Musixmatch API.

    :param endpoint: The API endpoint to query.
    :param params: Dictionary of query parameters to include in the request.
    :return: The JSON response from the API.
    """
    params["apikey"] = MUSICX_API_KEY

    response = requests.get(BASE_URL + endpoint, params=params)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def get_tracks_from_lyrics(lyrics: str, track_count: int) -> list[TrackData]:
    """
    Get track data given lyrics.

    :param lyrics: The lyric string to search for.
    :param track_count: The number of tracks to return.
    :return: List of TrackMetadata instances.
    """

    endpoint = "track.search"
    params = {
        "q_lyrics": lyrics,
        "f_lyrics_language": "es",
        "page_size": track_count,
        "page": 1,
        "s_track_rating": "desc",
    }
    response = _query_api(endpoint, params)
    tracks = []
    try:
        for i in range(track_count):
            response_track = response["message"]["body"]["track_list"][i]["track"]

            track_id = response_track["commontrack_id"]
            title = response_track["track_name"]
            artist = response_track["artist_name"]
            album = response_track["album_name"]
            genre = response_track["primary_genres"]["music_genre_list"][0][
                "music_genre"
            ]["music_genre_name"]
            track_obj = TrackData(track_id, title, artist, album, genre)
            tracks.append(track_obj)
    except IndexError:  # No or not enough tracks found
        pass

    return tracks


def get_track_from_id(track_id: int) -> TrackData:
    """
    Get track lyrics from track ID.

    :param track_id: The track ID.
    :return: Track lyrics.
    """
    endpoint = "track.get"
    params = {
        "commontrack_id": track_id,
    }
    response = _query_api(endpoint, params)
    response_track = response["message"]["body"]["track"]

    track_id = response_track["commontrack_id"]
    title = response_track["track_name"]
    artist = response_track["artist_name"]
    album = response_track["album_name"]
    genre = response_track["primary_genres"]["music_genre_list"][0]["music_genre"][
        "music_genre_name"
    ]
    track_obj = TrackData(track_id, title, artist, album, genre)
    return track_obj


def get_lyrics_from_id(track_id: int) -> str:
    """
    Get track lyrics from track ID.

    :param track_id: The track ID.
    :return: Track lyrics.
    """
    endpoint = "track.lyrics.get"
    params = {
        "commontrack_id": track_id,
    }
    response = _query_api(endpoint, params)

    lyrics = response["message"]["body"]["lyrics"]["lyrics_body"]
    return lyrics

def translate_text(lang: str, text: str) -> str:
    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(text, target_lang=lang)
    return result.text


_init_api_key(Path(__file__).parent.parent / "config.toml")

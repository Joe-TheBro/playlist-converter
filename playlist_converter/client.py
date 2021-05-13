from typing import List, Tuple, Dict, Union, Any
import requests


SEARCH_URL = "https://api.spotify.com/v1/search"
CONTAINS_URL = "https://api.spotify.com/v1/me/tracks/contains"

class SpotifyClient:
    """Client makes requests to the Spotify API to create a playlist."""

    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id

    def find_track_ids(self, track: str, artist: str) -> List[str]:
        query = "{} artist:{}".format(track, artist)
        request_args = {
            "url": SEARCH_URL,
            "headers": {"Authorization": "Bearer " + self.access_token},
            "params": {"q": query, "type": "track", "limit": 20}
        }
        response_json = send_request("GET", request_args)
        tracks_found = response_json["tracks"]["items"]
        return [result["id"] for result in tracks_found]

    def find_saved_track(self, track_ids: List[str]) -> Union[str, None]:
        request_args = {
            "url": CONTAINS_URL,
            "headers": {"Authorization": "Bearer " + self.access_token},
            "params": {"ids": track_ids}
        }
        response_json = send_request("GET", request_args)
        return first_saved(list(zip(track_ids, response_json)))

    def get_track_id(self, track: str, artist: str) -> Union[str, None]:
        track_results = self.find_track_ids(track, artist)
        if not track_results:
            return None
        saved_track = self.find_saved_track(track_results)
        if not saved_track:
            return track_results[0]
        return saved_track


def send_request(method: str, request_args: Dict) -> Any:
    response = requests.request(method, **request_args)
    response.raise_for_status()
    return response.json()

def first_saved(tracks_saved: List[Tuple[str, bool]]) -> Union[str, None]:
    for tid, saved in tracks_saved:
        if saved:
            return tid
    return None


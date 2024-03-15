import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

MUSICKIT_IDENTIFIER = os.getenv("MUSICKIT_IDENTIFIER")
MUSICKIT_SECRET = os.getenv("MUSICKIT_SECRET")
ALBUM_URL = "https://api.music.apple.com/v1/me/library/albums"

def build_token() -> str:
    """
    Builds the token for the Apple Music API
    param: None
    return: list
    
    Build a JWT object and return it as a list
    """
    #TODO: Implement this function
    pass

def get_tracks() -> list:
    """
    Get the tracks from the Apple Music API
    param: None
    return: list
    
    Get the tracks from the Apple Music API and return them as a list
    """
    dev_token = build_token()
    tracks = []
    resp = requests.get(ALBUM_URL, headers={"Authorization": "Bearer " + dev_token})
    if resp.status_code == 200:
        resp = json.loads(resp.text)
        while("data" in resp):
            for album in resp["data"]:
                tracks.append([f"{album["attributes"]["artistName"]}", f"{album["attributes"]["name"]}"])
            if "next" in resp:
                resp = requests.get(resp["next"], headers={"Authorization": "Bearer " + dev_token})
                if resp.status_code == 200:
                    resp = json.loads(resp.text)
                else:
                    raise Exception(f"Error: {resp.status_code}")
            else:
                break
        return tracks
    else:
        raise Exception(f"Error: {resp.status_code}")

def main():
    tracks = get_tracks()
    with open("playlist.txt", "w") as file:
        for track in tracks:
            file.write(f"{track[1]}---{track[0]}\n")
    print("Playlist created")

if __name__ == "__main__":
    main()
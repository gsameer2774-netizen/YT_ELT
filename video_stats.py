import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = 'tseries'


def get_playlist_id(API_KEY, CHANNEL_HANDLE):
    try:
        URL = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(URL)

        if response.status_code == 200:
            print("Success! Status Code: 200")
        else:
            print(f"Failed! Status Code: {response.status_code}")
            # This will print the exact reason (e.g., 'API Key Not Enabled')
            print(response.text)

        data = response.json()
        #json_output = json.dumps(data, indent=4)
        #print(json_output)


        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']

        #print(f"Channel Playlist ID: {channel_playlist_id}")
        return channel_playlist_id

    except Exception as e:
        return e


if __name__ == "__main__":
    playlist_id = get_playlist_id(API_KEY, CHANNEL_HANDLE)
    print(f"playlist_id is:{playlist_id}")
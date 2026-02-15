import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = 'tseries'
maxResults = 50



def get_playlist_id():
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
    

def get_video_ids(playlist_id,limit = 500):

    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"
    try:
        while True:
            params = {
                'part': 'contentDetails',
                'maxResults': maxResults,
                'playlistId': playlist_id,
                'key': API_KEY,
                'pageToken': pageToken
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
                if len(video_ids) >= limit:
                    return video_ids
            pageToken = data.get('nextPageToken')

            if not pageToken:
                break

        return video_ids
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return video_ids

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    print(f"playlist_id is:{playlist_id}")
    print(f"Video ids are: {get_video_ids(playlist_id)}")
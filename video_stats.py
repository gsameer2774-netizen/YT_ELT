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
    


def extract_video_data(video_ids):
    video_data = []

    def batch_list(video_id_lst,batch_size):
        for video_id in range(0,len(video_id_lst),batch_size):
            yield video_id_lst[video_id:video_id+batch_size]

    try:
        for batch in batch_list(video_ids,maxResults):
            video_ids_str = ','.join(batch)

            url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
            
                video_item = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount', 0),
                    "likeCount": statistics.get('likeCount',0),
                    "commentCount": statistics.get('commentCount',0)    
                }
                video_data.append(video_item)
        return video_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return video_data

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    print(video_data)
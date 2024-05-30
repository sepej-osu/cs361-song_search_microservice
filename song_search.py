from flask import Flask
from ytmusicapi import YTMusic
import json

ytmusic = YTMusic("oauth.json")

app = Flask(__name__)

# search route
@app.route("/search/<string:query>")
def search(query):
    search_results = ytmusic.search(query)

    songs = []

    # filter json results to only the information needed
    for item in search_results:
        if item.get('category') == 'Songs' or (item.get('category') == 'Top result' and item.get('resultType') == 'song'):
            filtered_item = {
                'title': item.get('title'),
                'album': item.get('album', {}).get('name'),
                'artist': item.get('artists')[0]['name'],
                'videoId': item.get('videoId'),
                'yturl': 'https://www.youtube.com/watch?v=' + item.get('videoId'),
                'duration': item.get('duration'),
                'duration_seconds': item.get('duration_seconds'),
                'thumbnail': next((thumbnail.get('url') for thumbnail in item.get('thumbnails', []) if thumbnail.get('width') == 120 and thumbnail.get('height') == 120), None)
            }
            songs.append(filtered_item)

    songs_json = json.dumps(songs, indent=4)

    return songs_json

# get song info route
@app.route("/song_info/<string:videoId>")
def song_info(videoId):
    song = ytmusic.get_song(videoId)

    # create a new dictionary with only certain values
    song_info = {'title': song['videoDetails']['title'],
                 'artist': song['videoDetails']['author'],
                 'duration_seconds': song['videoDetails']['lengthSeconds'],
                 'thumbnail': song['videoDetails']['thumbnail']['thumbnails'][3]['url']}

    song_json = json.dumps(song_info, indent=4)

    return song_json

if __name__ == '__main__':
    app.run(debug=True)
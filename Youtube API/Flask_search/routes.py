import requests
from isodate import parse_duration

from flask import Blueprint, render_template, current_app, request, redirect

main = Blueprint('main', __name__)

@main.route('/search', methods=['GET', 'POST'])
def index():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    if request.method == 'POST':
        search_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'q' : request.form.get('query'),
            'part' : 'snippet',
            'maxResults' : 100,
            'type' : 'video',
            'regionCode': 'IN'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.form.get('submit') == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            'maxResults' : 100,
            'regionCode': 'IN'
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title' : result['snippet']['title'],
            }
            videos.append(video_data)
        
    return render_template('index.html', videos=videos)

@main.route('/', methods=['GET'])
def popular_yt_videos():
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    # Define parameters for the YouTube API request
    video_params = {
        'key': current_app.config['YOUTUBE_API_KEY'],
        'chart': 'mostPopular',  # Specify to retrieve most popular videos
        'part': 'snippet,contentDetails',
        'maxResults': 100,
        'regionCode': 'IN'
    }

    # Make a request to the YouTube API to fetch popular videos
    r = requests.get(video_url, params=video_params)
    
    # Check if the request was successful
    if r.status_code == 200:
        results = r.json()['items']
        for result in results:
            video_data = {
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
                'title': result['snippet']['title'],
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            }
            videos.append(video_data)

    # Render the template with the retrieved videos
    return render_template('popular_yt_videos.html', videos=videos)



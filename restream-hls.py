from flask import Flask, Response, request
import requests

app = Flask(__name__)

# Replace with the URL of the original HLS stream's playlist
SOURCE_HLS_URL = 'https://example.com/path/to/your/hls/playlist.m3u8'

@app.route('/stream/<path:filename>')
def stream(filename):
    # Modify the filename to form the full URL for a segment request
    segment_url = f"{SOURCE_HLS_URL.rsplit('/', 1)[0]}/{filename}"
    response = requests.get(segment_url, stream=True)
    
    # Forward the response as a stream with the appropriate content type
    return Response(response.iter_content(chunk_size=4096), content_type=response.headers.get('Content-Type'))

@app.route('/playlist.m3u8')
def playlist():
    # Fetch the original playlist
    response = requests.get(SOURCE_HLS_URL)
    content = response.text

    # Modify the playlist file to point segments to this proxy server
    # Change each segment line to point to our /stream endpoint
    proxy_playlist = content.replace('index', request.host_url + 'stream/index')
    
    return Response(proxy_playlist, content_type='application/vnd.apple.mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

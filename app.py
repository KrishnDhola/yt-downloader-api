from flask import Flask, jsonify, request

try:
    import yt_dlp
except ImportError:
    import os
    os.system("pip install yt-dlp")
    import yt_dlp

app = Flask(__name__)

def get_video_details(video_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])

            # Get audio link (prefer m4a or best audio)
            audio_link = next((f['url'] for f in formats if f['ext'] == 'm4a'), None)

            # Get video links by resolution
            video_links = {
                f['format_note']: f['url']
                for f in formats
                if f['ext'] == 'mp4' and f.get('format_note')
            }

            return {
                "Created": "By Krishn Dhola 😃",
                "Title": info_dict.get('title', ''),
                "Description": info_dict.get('description', ''),
                "Download Links 👇": {
                    "Audio": audio_link,
                    "Video": video_links
                }
            }

    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET'])
@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    video_details = get_video_details(video_url)
    return jsonify(video_details)
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    video_details = get_video_details(video_url)
    return jsonify(video_details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


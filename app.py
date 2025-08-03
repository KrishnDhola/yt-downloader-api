from flask import Flask, jsonify, request
import os

try:
    import yt_dlp
except ImportError:
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

            # Extract audio link (prefer m4a)
            audio_link = next((f['url'] for f in formats if f['ext'] == 'm4a'), None)

            # Extract video links by resolution
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

@app.route('/')
@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    video_details = get_video_details(video_url)
    return jsonify(video_details)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render uses this PORT env variable
    app.run(host='0.0.0.0', port=port)

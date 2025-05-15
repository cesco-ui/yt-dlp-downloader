from flask import Flask, request, send_file
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return {"error": "No URL provided"}, 400

    filename = f"/tmp/{uuid.uuid4()}.mp4"
    try:
        # yt-dlp command to download raw video (no watermark if possible)
        result = subprocess.run(
            ["yt-dlp", "-f", "mp4", "-o", filename, url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return send_file(filename, as_attachment=True, download_name="video.mp4")
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr.decode()}, 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route("/tts")
def serve_tts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_path = os.path.join(base_dir, "../static/sample.mp3")
    return send_file(mp3_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(port=5000)

from flask import Flask, send_file, request, jsonify
import os
from io import BytesIO
import requests

app = Flask(__name__)

@app.route("/tts")
def serve_tts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_path = os.path.join(base_dir, "../static/sample.mp3")
    return send_file(mp3_path, mimetype="audio/mpeg")


# Environment variables for ElevenLabs API integration
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
# Default demo voice ID provided by ElevenLabs
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")


@app.route("/generate-tts", methods=["POST"])
def generate_tts():
    """Generate TTS audio from provided text using the ElevenLabs API."""
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text'"}), 400

    if not ELEVENLABS_API_KEY:
        return jsonify({"error": "ELEVENLABS_API_KEY not set"}), 500

    text = data["text"]

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream"
        headers = {
            "accept": "audio/mpeg",
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {"text": text}
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()

        audio_io = BytesIO(resp.content)
        return send_file(audio_io, mimetype="audio/mpeg", download_name="tts.mp3")
    except requests.RequestException as exc:
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    app.run(port=5000)

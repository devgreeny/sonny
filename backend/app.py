from flask import Flask, send_file, request, jsonify
import os
from io import BytesIO
import base64
import requests

# Load API keys from a .env file if present
from config import (
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    OPENAI_API_KEY,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)

import requests


app = Flask(__name__)

@app.route("/tts")
def serve_tts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_path = os.path.join(base_dir, "../static/sample.mp3")
    return send_file(mp3_path, mimetype="audio/mpeg")






def create_tts_audio(text: str) -> bytes:
    """Helper to call ElevenLabs and return raw MP3 bytes."""
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not set")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream"
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"text": text}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.content

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

        audio_bytes = create_tts_audio(text)
        audio_io = BytesIO(audio_bytes)
        return send_file(audio_io, mimetype="audio/mpeg", download_name="tts.mp3")
    except requests.RequestException as exc:
        return jsonify({"error": str(exc)}), 500


def get_spotify_token() -> str:
    """Return an access token using the Client Credentials flow."""
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise RuntimeError("Spotify credentials not set")

    auth = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth}"}
    data = {"grant_type": "client_credentials"}
    resp = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]


@app.route("/spotify-token")
def spotify_token():
    """Return a Spotify access token (for testing)."""
    try:
        token = get_spotify_token()
        return jsonify({"access_token": token})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/reddit-tts")
def reddit_tts():
    """Summarize top r/bostonceltics post and return TTS audio."""
    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY not set"}), 500

    try:
        reddit_resp = requests.get(
            "https://www.reddit.com/r/bostonceltics/top.json?limit=1",
            headers={"User-Agent": "sonny-app"},
        )
        reddit_resp.raise_for_status()
        post = reddit_resp.json()["data"]["children"][0]["data"]
        text = post.get("selftext") or post.get("title")
    except Exception as exc:
        return jsonify({"error": f"Failed to fetch reddit: {exc}"}), 500

    try:
        openai_headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f"Summarize this text in one paragraph: {text}",
                }
            ],
        }
        ai_resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=openai_headers,
            json=payload,
        )
        ai_resp.raise_for_status()
        summary = ai_resp.json()["choices"][0]["message"]["content"]
    except Exception as exc:
        return jsonify({"error": f"OpenAI failed: {exc}"}), 500

    try:
        audio_bytes = create_tts_audio(summary)
        audio_io = BytesIO(audio_bytes)
        return send_file(audio_io, mimetype="audio/mpeg", download_name="reddit.mp3")
    except Exception as exc:
        return jsonify({"error": f"ElevenLabs failed: {exc}"}), 500
      
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

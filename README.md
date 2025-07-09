# Sonny Beta

A small prototype that plays music and pauses for short spoken segments.

## Setup

Install dependencies (Flask and requests) and run both servers:

```bash
pip install Flask requests
python run_sonny.py
```

## New TTS Endpoint

`POST /generate-tts` with JSON like `{"text": "Hello world"}`. The route
calls the ElevenLabs API to create audio and returns an MP3 stream.

Set the environment variable `ELEVENLABS_API_KEY` with your ElevenLabs key.
Optionally override `ELEVENLABS_VOICE_ID` to choose a different voice.

## Reddit + Spotify Test

Set the following environment variables for extra features:

- `OPENAI_API_KEY` for summarizing Reddit posts
- `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` for retrieving a Spotify token

Endpoints:

- `GET /reddit-tts` - fetches the top post from r/bostonceltics, summarizes it via OpenAI, and returns TTS audio.
- `GET /spotify-token` - returns a Spotify access token using the client credentials flow (for testing the API connection).

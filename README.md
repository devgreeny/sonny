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

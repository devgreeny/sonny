# Sonny Beta

A minimal script that fetches the top post from **r/bostonceltics** and converts it to speech using the ElevenLabs API.

## Setup

1. Install the required Python packages:

```bash
pip install praw requests
```

2. Copy `.env.example` to `.env` and fill in your API keys:

- `ELEVENLABS_API_KEY` and optional `ELEVENLABS_VOICE_ID`
- `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT`

3. Run the script:

```bash
python sonny.py
```

The generated audio will be saved as `output.mp3` in the project directory.

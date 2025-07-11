import os
import requests
import praw


def load_env(env_path=".env"):
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                os.environ.setdefault(key, value)


load_env()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "sonny-app")


def fetch_reddit_text():
    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET]):
        raise RuntimeError("Reddit credentials not configured")
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )
    submission = next(reddit.subreddit("bostonceltics").top(limit=1))
    return submission.selftext or submission.title


def generate_tts(text: str) -> str:
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not configured")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream"
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json={"text": text}, headers=headers)
    resp.raise_for_status()
    out_path = "output.mp3"
    with open(out_path, "wb") as f:
        f.write(resp.content)
    return out_path


def main():
    text = fetch_reddit_text()
    print("Fetched Reddit post:\n")
    print(text)
    path = generate_tts(text)
    print(f"\nAudio saved to {path}")


if __name__ == "__main__":
    main()

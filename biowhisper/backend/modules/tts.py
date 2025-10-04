import os
from typing import Optional
import requests
from pathlib import Path

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def elevenlabs_tts(text: str, voice: str = "alloy") -> Optional[str]:
    if not text:
        return None

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {"text": text}

    try:
        resp = requests.post(API_URL.format(voice_id=voice), json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            out_dir = Path(__file__).resolve().parents[2] / "uploads"
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / "tts_output.mp3"
            with open(out_path, "wb") as f:
                f.write(resp.content)
            return str(out_path)
        else:
            return None
    except Exception:
        return None

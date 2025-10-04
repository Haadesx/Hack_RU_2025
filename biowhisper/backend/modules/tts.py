from __future__ import annotations
import os
from pathlib import Path
from typing import Optional
import requests

from pydub.generators import Sine
from pydub import AudioSegment

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def _fallback_generate_audio(text: str, outfile: Path) -> str:
    # Generate a short 3-second tone so the UI has something to play
    tone = Sine(440).to_audio_segment(duration=2000).fade_in(100).fade_out(300)
    quieter = tone - 12
    AudioSegment.silent(duration=250).append(quieter, crossfade=50).export(outfile, format="mp3")
    return f"/uploads/{outfile.name}"


def elevenlabs_tts(text: str, voice: str = "alloy") -> Optional[str]:
    outfile = UPLOAD_DIR / "tts_output.mp3"

    if not ELEVEN_API_KEY:
        return _fallback_generate_audio(text, outfile)

    headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text}

    try:
        url = ELEVEN_BASE_URL.format(voice_id=voice)
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200 and resp.content:
            with outfile.open("wb") as f:
                f.write(resp.content)
            return f"/uploads/{outfile.name}"
        return _fallback_generate_audio(text, outfile)
    except Exception:
        return _fallback_generate_audio(text, outfile)

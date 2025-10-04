import numpy as np
import librosa
from typing import Dict, Any


def analyze_audio(path: str, sr: int = 22050) -> Dict[str, Any]:
    y, _ = librosa.load(path, sr=sr, mono=True, duration=12)
    if y.size == 0:
        return {"ok": False, "reason": "empty_audio"}

    rms = float(librosa.feature.rms(y=y).mean())
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_vals = pitches[magnitudes > 0]
    pitch_mean = float(np.mean(pitch_vals)) if pitch_vals.size > 0 else 0.0
    pitch_var = float(np.var(pitch_vals)) if pitch_vals.size > 0 else 0.0
    energy = float(np.mean(np.abs(y)))

    stress_score = min(1.0, (energy * 5 + tempo / 200 + pitch_var * 10) / 3)

    return {
        "ok": True,
        "rms": rms,
        "tempo": float(tempo),
        "pitch_mean": pitch_mean,
        "pitch_var": pitch_var,
        "energy": energy,
        "stress_score": stress_score,
    }

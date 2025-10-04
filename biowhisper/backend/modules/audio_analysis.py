from __future__ import annotations
import numpy as np
from typing import Dict, Any

# Optional heavy imports guarded for hackathon robustness
try:
    import librosa  # type: ignore
except Exception:  # pragma: no cover
    librosa = None  # type: ignore


def _safe_float(value: float | int | np.ndarray, default: float = 0.0) -> float:
    try:
        if isinstance(value, np.ndarray):
            if value.size == 0:
                return default
            return float(np.mean(value))
        return float(value)
    except Exception:
        return default


def analyze_audio(path: str, sr: int = 22050) -> Dict[str, Any]:
    """
    Lightweight audio feature extraction with safe fallbacks.
    Returns a dict with energy, rms, tempo, pitch_mean, pitch_var, stress_score.
    """
    features: Dict[str, Any] = {
        "rms": 0.0,
        "tempo": 0.0,
        "pitch_mean": 0.0,
        "pitch_var": 0.0,
        "energy": 0.0,
        "stress_score": 0.0,
        "engine": "fallback",
    }

    if librosa is None:
        return features

    try:
        y, _ = librosa.load(path, sr=sr, mono=True, duration=12)
        if y is None or len(y) == 0:
            return features

        rms = _safe_float(librosa.feature.rms(y=y).mean())
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        voiced = pitches[magnitudes > 0]
        pitch_mean = _safe_float(voiced.mean() if voiced.size else 0.0)
        pitch_var = _safe_float(np.var(voiced) if voiced.size else 0.0)
        energy = _safe_float(np.mean(np.abs(y)))

        stress_score = float(min(1.0, (energy * 5.0 + (tempo / 200.0) + pitch_var * 10.0) / 3.0))

        features.update(
            {
                "rms": float(rms),
                "tempo": float(tempo),
                "pitch_mean": float(pitch_mean),
                "pitch_var": float(pitch_var),
                "energy": float(energy),
                "stress_score": float(stress_score),
                "engine": "librosa",
            }
        )
        return features
    except Exception:
        return features

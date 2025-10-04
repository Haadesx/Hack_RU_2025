# modules/audio_analysis.py
import numpy as np
import librosa
import soundfile as sf
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

def analyze_audio(path, sr=22050):
    """
    Analyze audio file for stress indicators and voice characteristics
    Returns comprehensive audio features for wellness assessment
    """
    try:
        # Load audio file
        y, sr = librosa.load(path, sr=sr, mono=True, duration=12)
        
        # Basic audio features
        rms = librosa.feature.rms(y=y).mean()
        energy = float(np.mean(np.abs(y)))
        
        # Tempo analysis
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Pitch analysis
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_vals = pitches[magnitudes > 0]
        pitch_mean = float(np.mean(pitch_vals)) if len(pitch_vals) > 0 else 0.0
        pitch_var = float(np.var(pitch_vals)) if len(pitch_vals) > 0 else 0.0
        pitch_std = float(np.std(pitch_vals)) if len(pitch_vals) > 0 else 0.0
        
        # Spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y).mean()
        
        # MFCC features (mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfccs, axis=1)
        
        # Voice Activity Detection (simple energy-based)
        frame_length = int(0.025 * sr)  # 25ms frames
        hop_length = int(0.010 * sr)    # 10ms hop
        energy_frames = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        voice_activity = np.mean(energy_frames > np.percentile(energy_frames, 30))
        
        # Speaking rate estimation (rough)
        speaking_rate = len(energy_frames[energy_frames > np.percentile(energy_frames, 50)]) / (len(y) / sr)
        
        # Stress score calculation (composite heuristic)
        # Higher energy + higher tempo + higher pitch variance + higher spectral centroid = more stress
        stress_components = [
            min(1.0, energy * 5),                    # Energy component
            min(1.0, tempo / 200),                    # Tempo component  
            min(1.0, pitch_var * 10),                 # Pitch variance component
            min(1.0, spectral_centroid / 3000),       # Spectral centroid component
            min(1.0, zero_crossing_rate * 2)          # Zero crossing rate component
        ]
        
        stress_score = float(np.mean(stress_components))
        
        # Emotional tone indicators (simplified)
        tone_indicators = {
            "calm": max(0, 1 - stress_score),
            "energetic": min(1.0, energy * 3),
            "focused": min(1.0, speaking_rate / 3),
            "relaxed": max(0, 1 - (pitch_var * 5))
        }
        
        return {
            "rms": float(rms),
            "energy": energy,
            "tempo": float(tempo),
            "pitch_mean": pitch_mean,
            "pitch_var": pitch_var,
            "pitch_std": pitch_std,
            "spectral_centroid": float(spectral_centroid),
            "spectral_rolloff": float(spectral_rolloff),
            "zero_crossing_rate": float(zero_crossing_rate),
            "voice_activity": float(voice_activity),
            "speaking_rate": float(speaking_rate),
            "stress_score": stress_score,
            "tone_indicators": tone_indicators,
            "mfcc_features": mfcc_mean.tolist(),
            "audio_length": len(y) / sr
        }
        
    except Exception as e:
        print(f"Audio analysis error: {e}")
        # Return default values if analysis fails
        return {
            "rms": 0.0,
            "energy": 0.0,
            "tempo": 0.0,
            "pitch_mean": 0.0,
            "pitch_var": 0.0,
            "pitch_std": 0.0,
            "spectral_centroid": 0.0,
            "spectral_rolloff": 0.0,
            "zero_crossing_rate": 0.0,
            "voice_activity": 0.0,
            "speaking_rate": 0.0,
            "stress_score": 0.5,
            "tone_indicators": {"calm": 0.5, "energetic": 0.5, "focused": 0.5, "relaxed": 0.5},
            "mfcc_features": [0.0] * 13,
            "audio_length": 0.0
        }
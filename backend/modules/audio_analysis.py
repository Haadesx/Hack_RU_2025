# modules/audio_analysis.py
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def analyze_audio(file_path: str, sr: int = 22050) -> dict:
    """
    Analyze audio file for emotional and stress indicators
    Returns features including energy, pitch, tempo, and stress score
    """
    try:
        # Load audio file
        y, _ = librosa.load(file_path, sr=sr, mono=True, duration=12)
        
        if len(y) == 0:
            return {"error": "Empty audio file", "stress_score": 0.5}
        
        # Basic audio features
        rms = librosa.feature.rms(y=y)[0]
        rms_mean = float(np.mean(rms))
        rms_var = float(np.var(rms))
        
        # Tempo and rhythm
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(tempo)
        
        # Pitch analysis
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr, threshold=0.1)
        pitch_values = pitches[magnitudes > np.max(magnitudes) * 0.1]
        
        if len(pitch_values) > 0:
            pitch_mean = float(np.mean(pitch_values[pitch_values > 0]))
            pitch_var = float(np.var(pitch_values[pitch_values > 0]))
            pitch_range = float(np.max(pitch_values) - np.min(pitch_values[pitch_values > 0]))
        else:
            pitch_mean = 0.0
            pitch_var = 0.0
            pitch_range = 0.0
        
        # Speaking rate estimation (zero crossing rate as proxy)
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        speaking_rate = float(np.mean(zcr))
        
        # Energy distribution
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        
        energy = float(np.mean(np.abs(y)))
        spectral_energy = float(np.mean(spectral_centroid))
        
        # MFCC features for voice quality
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = [float(np.mean(mfcc)) for mfcc in mfccs]
        
        # Voice activity detection (simple energy threshold)
        voice_activity = np.mean(rms > np.mean(rms) * 0.1)
        
        # Stress score calculation (0-1 scale)
        # Higher energy, pitch variance, tempo, and speaking rate suggest stress
        stress_indicators = [
            min(1.0, energy * 10),  # Energy component
            min(1.0, pitch_var / 1000),  # Pitch variability
            min(1.0, (tempo - 60) / 100) if tempo > 60 else 0,  # Fast tempo
            min(1.0, speaking_rate * 20),  # Speaking rate
            min(1.0, rms_var * 50)  # RMS variability
        ]
        
        stress_score = float(np.mean(stress_indicators))
        stress_score = max(0.0, min(1.0, stress_score))  # Clamp to 0-1
        
        # Emotional valence estimation (simplified)
        # Lower pitch + higher energy might indicate excitement
        # Higher pitch + lower energy might indicate anxiety
        if pitch_mean > 200 and energy < 0.01:
            emotional_state = "anxious"
            confidence = 0.6
        elif pitch_mean < 150 and energy > 0.02:
            emotional_state = "energetic"
            confidence = 0.7
        elif energy < 0.005:
            emotional_state = "tired"
            confidence = 0.5
        else:
            emotional_state = "neutral"
            confidence = 0.4
        
        return {
            "rms_mean": rms_mean,
            "rms_var": rms_var,
            "tempo": tempo,
            "pitch_mean": pitch_mean,
            "pitch_var": pitch_var,
            "pitch_range": pitch_range,
            "energy": energy,
            "speaking_rate": speaking_rate,
            "spectral_energy": spectral_energy,
            "voice_activity": float(voice_activity),
            "stress_score": stress_score,
            "emotional_state": emotional_state,
            "emotional_confidence": confidence,
            "mfcc_features": mfcc_mean[:5],  # First 5 MFCC coefficients
            "duration_seconds": float(len(y) / sr),
            "analysis_quality": "good" if voice_activity > 0.3 else "low"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing audio {file_path}: {str(e)}")
        return {
            "error": str(e),
            "stress_score": 0.5,
            "emotional_state": "unknown",
            "analysis_quality": "failed"
        }

def create_breathing_exercise_audio(duration_minutes: int = 3, output_path: str = None) -> str:
    """
    Generate a simple breathing exercise tone pattern
    """
    if output_path is None:
        output_path = "uploads/tts/breathing_exercise.wav"
    
    sr = 22050
    duration_seconds = duration_minutes * 60
    
    # Create breathing pattern: 4 seconds in, 2 seconds hold, 6 seconds out
    cycle_duration = 12  # seconds per cycle
    num_cycles = duration_seconds // cycle_duration
    
    # Generate tone pattern
    t = np.linspace(0, duration_seconds, int(sr * duration_seconds))
    frequency = 220  # A3 note
    
    # Create breathing cue tones
    audio = np.zeros_like(t)
    
    for cycle in range(num_cycles):
        cycle_start = cycle * cycle_duration
        
        # Inhale cue (rising tone)
        inhale_start = int((cycle_start) * sr)
        inhale_end = int((cycle_start + 4) * sr)
        inhale_t = np.linspace(0, 4, inhale_end - inhale_start)
        audio[inhale_start:inhale_end] += 0.1 * np.sin(2 * np.pi * frequency * inhale_t) * np.linspace(0, 1, len(inhale_t))
        
        # Exhale cue (falling tone)
        exhale_start = int((cycle_start + 6) * sr)
        exhale_end = int((cycle_start + 12) * sr)
        exhale_t = np.linspace(0, 6, exhale_end - exhale_start)
        audio[exhale_start:exhale_end] += 0.1 * np.sin(2 * np.pi * frequency * 0.7 * exhale_t) * np.linspace(1, 0, len(exhale_t))
    
    # Save audio file
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_path, audio, sr)
    
    return output_path
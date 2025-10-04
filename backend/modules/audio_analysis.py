# modules/audio_analysis.py - Voice and stress analysis
import numpy as np
import librosa
import warnings
warnings.filterwarnings('ignore')

def analyze_audio(path, sr=22050, duration=12):
    """
    Analyze audio file for emotion, stress, and vocal characteristics
    
    Returns:
        dict: Audio features including stress score, energy, tempo, pitch
    """
    try:
        # Load audio file
        y, loaded_sr = librosa.load(path, sr=sr, mono=True, duration=duration)
        
        # 1) RMS Energy (loudness/intensity)
        rms = librosa.feature.rms(y=y).mean()
        
        # 2) Tempo (speaking rate indicator)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # 3) Pitch analysis (using piptrack for fundamental frequency)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr, fmin=75, fmax=400)
        
        # Extract valid pitches (where magnitude > 0)
        pitch_vals = pitches[magnitudes > np.median(magnitudes)]
        
        if len(pitch_vals) > 0:
            pitch_mean = float(np.mean(pitch_vals))
            pitch_var = float(np.var(pitch_vals))
            pitch_std = float(np.std(pitch_vals))
        else:
            pitch_mean = 0.0
            pitch_var = 0.0
            pitch_std = 0.0
        
        # 4) Zero-crossing rate (roughness/breathiness indicator)
        zcr = librosa.feature.zero_crossing_rate(y).mean()
        
        # 5) Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
        
        # 6) MFCC (tone quality indicators)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfccs, axis=1).tolist()
        
        # 7) Energy (amplitude-based)
        energy = float(np.mean(np.abs(y)))
        
        # 8) Calculate stress score (heuristic based on multiple features)
        # High stress indicators: high energy, high pitch variance, high tempo, high ZCR
        stress_indicators = [
            min(1.0, energy * 8),  # Normalize energy
            min(1.0, tempo / 180),  # Normalize tempo (speaking rate)
            min(1.0, pitch_var / 1000),  # High pitch variance = stress
            min(1.0, zcr * 5)  # High zero-crossing = breathiness/tension
        ]
        
        stress_score = float(np.mean(stress_indicators))
        
        # 9) Emotional tone estimate (simplified)
        # Low pitch + low energy = sadness/fatigue
        # High pitch + high energy = anxiety/excitement
        # Mid-range = neutral/calm
        
        if pitch_mean > 200 and energy > 0.05:
            emotional_tone = "anxious/energetic"
            confidence = 0.7
        elif pitch_mean < 150 and energy < 0.03:
            emotional_tone = "low-energy/subdued"
            confidence = 0.6
        elif stress_score > 0.6:
            emotional_tone = "stressed/tense"
            confidence = 0.65
        else:
            emotional_tone = "neutral/calm"
            confidence = 0.5
        
        # 10) Speaking duration estimate (remove silence)
        non_silent_intervals = librosa.effects.split(y, top_db=20)
        speaking_duration = sum([(end - start) / sr for start, end in non_silent_intervals])
        
        return {
            "rms": float(rms),
            "tempo": float(tempo),
            "pitch_mean": pitch_mean,
            "pitch_variance": pitch_var,
            "pitch_std": pitch_std,
            "zero_crossing_rate": float(zcr),
            "spectral_centroid": float(spectral_centroids),
            "spectral_rolloff": float(spectral_rolloff),
            "energy": energy,
            "stress_score": stress_score,
            "emotional_tone": emotional_tone,
            "emotional_confidence": confidence,
            "speaking_duration_seconds": float(speaking_duration),
            "mfcc_mean": mfcc_mean[:5],  # First 5 MFCCs for brevity
            "analysis_status": "success"
        }
        
    except Exception as e:
        print(f"Audio analysis error: {str(e)}")
        return {
            "error": str(e),
            "stress_score": 0.5,  # Default neutral
            "emotional_tone": "unknown",
            "analysis_status": "failed"
        }

def format_audio_insights(features):
    """
    Convert technical features into human-readable insights
    """
    insights = []
    
    if features.get("stress_score", 0) > 0.65:
        insights.append("Voice shows signs of tension or stress")
    elif features.get("stress_score", 0) < 0.35:
        insights.append("Voice sounds calm and relaxed")
    
    if features.get("energy", 0) < 0.02:
        insights.append("Low vocal energy - may indicate fatigue")
    
    if features.get("speaking_duration_seconds", 0) < 5:
        insights.append("Brief response - consider if comfortable sharing")
    
    return insights

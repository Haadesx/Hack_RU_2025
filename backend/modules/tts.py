# modules/tts.py - Text-to-Speech using ElevenLabs
import os
import requests
from pathlib import Path
from typing import Optional

# ElevenLabs API configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Default voice IDs (you can customize these)
# Get voice IDs from: https://api.elevenlabs.io/v1/voices
VOICE_IDS = {
    "alloy": "21m00Tcm4TlvDq8ikWAM",  # Rachel - calm female
    "echo": "pNInz6obpgDQGcFmaJgB",   # Adam - deep male  
    "calm": "EXAVITQu4vr4xnSDxMaL",   # Bella - soothing female
    "professional": "ErXwobaYiN019PkySvjV"  # Antoni - professional male
}

UPLOAD_DIR = Path("uploads")

def elevenlabs_tts(
    text: str,
    voice: str = "alloy",
    output_filename: Optional[str] = None,
    model_id: str = "eleven_monolingual_v1"
) -> Optional[str]:
    """
    Generate speech audio from text using ElevenLabs API
    
    Args:
        text: Text to convert to speech
        voice: Voice name (alloy, echo, calm, professional)
        output_filename: Output filename (default: auto-generated)
        model_id: ElevenLabs model ID
        
    Returns:
        str: Path to generated audio file, or None if failed
    """
    
    # Check if API key is configured
    if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "":
        print("⚠️  ELEVENLABS_API_KEY not configured - using fallback TTS")
        return _fallback_tts(text, output_filename)
    
    # Get voice ID
    voice_id = VOICE_IDS.get(voice, VOICE_IDS["alloy"])
    
    # Prepare output path
    if not output_filename:
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        output_filename = f"tts_{text_hash}.mp3"
    
    output_path = UPLOAD_DIR / output_filename
    
    try:
        # Prepare API request
        url = f"{ELEVENLABS_API_URL}/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
        
        # Make API request
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Save audio file
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS audio generated: {output_filename}")
            return str(output_path)
        else:
            print(f"❌ ElevenLabs API error ({response.status_code}): {response.text}")
            return _fallback_tts(text, output_filename)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ TTS request error: {str(e)}")
        return _fallback_tts(text, output_filename)
    
    except Exception as e:
        print(f"❌ TTS unexpected error: {str(e)}")
        return _fallback_tts(text, output_filename)

def _fallback_tts(text: str, output_filename: Optional[str] = None) -> Optional[str]:
    """
    Fallback TTS using system TTS (pyttsx3) or gTTS when ElevenLabs unavailable
    """
    if not output_filename:
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        output_filename = f"tts_fallback_{text_hash}.mp3"
    
    output_path = UPLOAD_DIR / output_filename
    
    try:
        # Try gTTS first (Google Text-to-Speech - free, no API key needed)
        from gtts import gTTS
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(str(output_path))
        
        print(f"✅ Fallback TTS (gTTS) generated: {output_filename}")
        return str(output_path)
        
    except ImportError:
        print("⚠️  gTTS not installed. Install with: pip install gTTS")
        
        # Try pyttsx3 as second fallback (offline TTS)
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)  # Speaking rate
            engine.setProperty('volume', 0.9)
            
            # Convert to WAV first, then can convert to MP3 if needed
            wav_path = str(output_path).replace('.mp3', '.wav')
            engine.save_to_file(text, wav_path)
            engine.runAndWait()
            
            # Try to convert WAV to MP3 using pydub
            try:
                from pydub import AudioSegment
                audio = AudioSegment.from_wav(wav_path)
                audio.export(str(output_path), format="mp3")
                os.remove(wav_path)  # Clean up WAV file
                
                print(f"✅ Fallback TTS (pyttsx3) generated: {output_filename}")
                return str(output_path)
                
            except ImportError:
                # If pydub not available, return WAV file
                print(f"✅ Fallback TTS (pyttsx3) generated WAV: {wav_path}")
                return wav_path
                
        except Exception as e:
            print(f"❌ Fallback TTS also failed: {str(e)}")
            return None
    
    except Exception as e:
        print(f"❌ Fallback TTS error: {str(e)}")
        return None

def generate_breathing_exercise_audio(
    duration_minutes: int = 3,
    pattern: str = "4-4-6",
    output_filename: Optional[str] = None
) -> Optional[str]:
    """
    Generate guided breathing exercise audio
    
    Args:
        duration_minutes: Length of exercise
        pattern: Breathing pattern (e.g., "4-4-6" = inhale 4, hold 4, exhale 6)
        output_filename: Output filename
        
    Returns:
        str: Path to generated audio file
    """
    
    # Parse breathing pattern
    try:
        parts = pattern.split('-')
        inhale_count = int(parts[0])
        hold_count = int(parts[1]) if len(parts) > 1 else 0
        exhale_count = int(parts[2]) if len(parts) > 2 else inhale_count + 2
    except:
        inhale_count, hold_count, exhale_count = 4, 4, 6
    
    # Generate script
    intro = f"""Let's begin a {duration_minutes}-minute breathing exercise. 
    Find a comfortable position. You can close your eyes if you'd like.
    
    We'll use a {inhale_count}-{hold_count}-{exhale_count} breathing pattern. 
    Breathe in for {inhale_count} counts, hold for {hold_count}, and breathe out for {exhale_count}.
    
    Let's start."""
    
    # Generate multiple cycles
    cycles = []
    for i in range(min(5, duration_minutes * 2)):  # Approximately 30s per cycle
        cycle = f"""
        Breathe in slowly through your nose: {', '.join([str(x) for x in range(1, inhale_count + 1)])}.
        Hold: {', '.join([str(x) for x in range(1, hold_count + 1)])}.
        Breathe out slowly through your mouth: {', '.join([str(x) for x in range(1, exhale_count + 1)])}.
        {"And rest." if i % 2 == 1 else ""}
        """
        cycles.append(cycle)
    
    outro = """
    Well done. Take a moment to notice how you feel.
    You can return to this breathing pattern anytime you need to find calm.
    When you're ready, gently open your eyes.
    """
    
    full_script = intro + " ".join(cycles) + outro
    
    # Generate TTS
    if not output_filename:
        output_filename = f"breathing_exercise_{pattern}_{duration_minutes}min.mp3"
    
    return elevenlabs_tts(full_script, voice="calm", output_filename=output_filename)

def list_available_voices() -> dict:
    """
    Fetch available voices from ElevenLabs API
    """
    if not ELEVENLABS_API_KEY:
        return {"error": "API key not configured"}
    
    try:
        response = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers={"xi-api-key": ELEVENLABS_API_KEY},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}

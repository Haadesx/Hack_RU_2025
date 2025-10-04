# modules/tts.py
import os
import requests
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

def elevenlabs_tts(text: str, voice: str = "alloy", output_name: Optional[str] = None) -> Optional[str]:
    """
    Convert text to speech using ElevenLabs API
    Returns path to generated audio file
    """
    try:
        if not ELEVEN_API_KEY:
            print("ELEVENLABS_API_KEY not found, using mock TTS")
            return create_mock_audio_file(text, output_name)
        
        # ElevenLabs API endpoint
        voice_id = get_voice_id(voice)
        url = f"{ELEVEN_API_URL}/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save audio file
            if not output_name:
                output_name = f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            output_path = Path("uploads") / f"{output_name}.mp3"
            output_path.parent.mkdir(exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"TTS audio saved to: {output_path}")
            return str(output_path)
            
        else:
            print(f"ElevenLabs API error: {response.status_code} - {response.text}")
            return create_mock_audio_file(text, output_name)
            
    except Exception as e:
        print(f"TTS generation failed: {e}")
        return create_mock_audio_file(text, output_name)

def get_voice_id(voice_name: str) -> str:
    """Get ElevenLabs voice ID from voice name"""
    voice_mapping = {
        "alloy": "pNInz6obpgDQGcFmaJgB",  # Default voice
        "echo": "MF3mGyEYCl7XYWbV9V6O",
        "fable": "pqHfZKP75CvOlQylNhV4",
        "onyx": "2EiwWnXFnvU5JabPnv8n",
        "nova": "pMsXgVXv3BLzUgSXRplM",
        "shimmer": "cgS3voqU2WVX3UxsqZQ4"
    }
    return voice_mapping.get(voice_name, voice_mapping["alloy"])

def create_mock_audio_file(text: str, output_name: Optional[str] = None) -> str:
    """Create a mock audio file for demo purposes"""
    try:
        if not output_name:
            output_name = f"mock_tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        output_path = Path("uploads") / f"{output_name}.txt"
        output_path.parent.mkdir(exist_ok=True)
        
        # Create a text file with the content (for demo purposes)
        with open(output_path, "w") as f:
            f.write(f"TTS Content:\n{text}\n\n")
            f.write(f"Generated at: {datetime.now().isoformat()}\n")
            f.write("Note: This is a mock TTS file. In production, this would be actual audio.\n")
        
        print(f"Mock TTS file created: {output_path}")
        return str(output_path)
        
    except Exception as e:
        print(f"Mock TTS creation failed: {e}")
        return None

def generate_breathing_audio(duration_minutes: int = 3) -> Optional[str]:
    """Generate a guided breathing exercise audio"""
    breathing_script = f"""
    Welcome to your {duration_minutes}-minute breathing exercise. 
    Find a comfortable position and let's begin.
    
    Breathe in slowly for four counts... hold for four counts... 
    and exhale slowly for eight counts.
    
    Continue this pattern. With each breath, feel yourself becoming more relaxed.
    Your mind is clearing, your body is releasing tension.
    
    You're doing beautifully. Stay with this rhythm.
    In... hold... out. In... hold... out.
    
    Feel the peace flowing through your body.
    You are calm, centered, and at peace.
    
    Take one final deep breath... and when you're ready, 
    gently return your attention to the present moment.
    """
    
    return elevenlabs_tts(breathing_script, voice="alloy", output_name=f"breathing_{duration_minutes}min")

def generate_sleep_hypnosis_audio(script: str) -> Optional[str]:
    """Generate sleep hypnosis audio from script"""
    return elevenlabs_tts(script, voice="alloy", output_name="sleep_hypnosis")

# Demo function to test TTS
def test_tts():
    """Test TTS functionality"""
    test_text = "Hello, this is a test of the text-to-speech system. How are you feeling today?"
    result = elevenlabs_tts(test_text, voice="alloy")
    print(f"TTS test result: {result}")
    return result

if __name__ == "__main__":
    test_tts()
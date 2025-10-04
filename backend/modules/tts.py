# modules/tts.py
import os
import requests
import asyncio
import aiohttp
from pathlib import Path
import uuid
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# ElevenLabs configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"

# Voice IDs for different types of content
VOICE_IDS = {
    "narrative": "21m00Tcm4TlvDq8ikWAM",  # Rachel - warm, conversational
    "breathing": "AZnzlk1XvdvUeBnXmlld",  # Domi - calm, soothing
    "hypnosis": "EXAVITQu4vr4xnSDxMaL",  # Bella - soft, meditative
    "long_hypnosis": "EXAVITQu4vr4xnSDxMaL",  # Bella - soft, meditative
    "default": "21m00Tcm4TlvDq8ikWAM"
}

# Alternative free TTS options
USE_ELEVENLABS = bool(ELEVENLABS_API_KEY)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Output directory
TTS_OUTPUT_DIR = Path("uploads/tts")
TTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def elevenlabs_tts(text: str, voice_type: str = "default") -> Optional[str]:
    """
    Generate TTS audio using ElevenLabs API
    Returns path to generated audio file or None if failed
    """
    try:
        if not ELEVENLABS_API_KEY:
            logger.warning("ElevenLabs API key not available, using fallback TTS")
            return generate_fallback_tts(text, voice_type)
        
        voice_id = VOICE_IDS.get(voice_type, VOICE_IDS["default"])
        
        # Prepare request
        url = f"{ELEVENLABS_BASE_URL}/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        # Configure voice settings based on type
        voice_settings = get_voice_settings(voice_type)
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": voice_settings
        }
        
        # Make request
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Generate unique filename
            filename = f"tts_{voice_type}_{uuid.uuid4().hex[:8]}.mp3"
            file_path = TTS_OUTPUT_DIR / filename
            
            # Save audio file
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            logger.info(f"TTS generated successfully: {filename}")
            return str(file_path)
        else:
            logger.error(f"ElevenLabs API error {response.status_code}: {response.text}")
            return generate_fallback_tts(text, voice_type)
            
    except requests.Timeout:
        logger.error("ElevenLabs API timeout")
        return generate_fallback_tts(text, voice_type)
    except Exception as e:
        logger.error(f"ElevenLabs TTS failed: {str(e)}")
        return generate_fallback_tts(text, voice_type)

async def elevenlabs_tts_async(text: str, voice_type: str = "default") -> Optional[str]:
    """Async version of ElevenLabs TTS"""
    try:
        if not ELEVENLABS_API_KEY:
            return await generate_fallback_tts_async(text, voice_type)
        
        voice_id = VOICE_IDS.get(voice_type, VOICE_IDS["default"])
        url = f"{ELEVENLABS_BASE_URL}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json", 
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        voice_settings = get_voice_settings(voice_type)
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1", 
            "voice_settings": voice_settings
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, timeout=30) as response:
                if response.status == 200:
                    filename = f"tts_{voice_type}_{uuid.uuid4().hex[:8]}.mp3"
                    file_path = TTS_OUTPUT_DIR / filename
                    
                    audio_data = await response.read()
                    with open(file_path, "wb") as f:
                        f.write(audio_data)
                    
                    return str(file_path)
                else:
                    error_text = await response.text()
                    logger.error(f"ElevenLabs API error {response.status}: {error_text}")
                    return await generate_fallback_tts_async(text, voice_type)
                    
    except asyncio.TimeoutError:
        logger.error("ElevenLabs API timeout")
        return await generate_fallback_tts_async(text, voice_type)
    except Exception as e:
        logger.error(f"ElevenLabs async TTS failed: {str(e)}")
        return await generate_fallback_tts_async(text, voice_type)

def get_voice_settings(voice_type: str) -> dict:
    """Get voice settings optimized for different content types"""
    base_settings = {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    
    if voice_type == "breathing":
        return {
            **base_settings,
            "stability": 0.7,  # More stable for meditation
            "similarity_boost": 0.3
        }
    elif voice_type in ["hypnosis", "long_hypnosis"]:
        return {
            **base_settings,
            "stability": 0.8,  # Very stable for sleep content
            "similarity_boost": 0.2
        }
    elif voice_type == "narrative":
        return {
            **base_settings,
            "stability": 0.4,  # More expressive for storytelling
            "similarity_boost": 0.6
        }
    else:
        return base_settings

def generate_fallback_tts(text: str, voice_type: str) -> Optional[str]:
    """
    Fallback TTS using OpenAI or system TTS
    """
    try:
        # Try OpenAI TTS if available
        if OPENAI_API_KEY:
            return openai_tts(text, voice_type)
        
        # Try system TTS (espeak, say, etc.)
        return system_tts(text, voice_type)
        
    except Exception as e:
        logger.error(f"Fallback TTS failed: {str(e)}")
        return create_placeholder_audio(text, voice_type)

async def generate_fallback_tts_async(text: str, voice_type: str) -> Optional[str]:
    """Async fallback TTS"""
    try:
        if OPENAI_API_KEY:
            return await openai_tts_async(text, voice_type)
        return await asyncio.get_event_loop().run_in_executor(None, system_tts, text, voice_type)
    except Exception as e:
        logger.error(f"Async fallback TTS failed: {str(e)}")
        return create_placeholder_audio(text, voice_type)

def openai_tts(text: str, voice_type: str) -> Optional[str]:
    """Generate TTS using OpenAI API"""
    try:
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Map voice types to OpenAI voices
        voice_map = {
            "narrative": "alloy",
            "breathing": "nova", 
            "hypnosis": "shimmer",
            "long_hypnosis": "shimmer",
            "default": "alloy"
        }
        
        voice = voice_map.get(voice_type, "alloy")
        
        data = {
            "model": "tts-1",
            "input": text,
            "voice": voice,
            "response_format": "mp3"
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            filename = f"tts_openai_{voice_type}_{uuid.uuid4().hex[:8]}.mp3"
            file_path = TTS_OUTPUT_DIR / filename
            
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            logger.info(f"OpenAI TTS generated: {filename}")
            return str(file_path)
        else:
            logger.error(f"OpenAI TTS error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"OpenAI TTS failed: {str(e)}")
        return None

async def openai_tts_async(text: str, voice_type: str) -> Optional[str]:
    """Async OpenAI TTS"""
    try:
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        voice_map = {
            "narrative": "alloy",
            "breathing": "nova",
            "hypnosis": "shimmer", 
            "long_hypnosis": "shimmer",
            "default": "alloy"
        }
        
        data = {
            "model": "tts-1",
            "input": text,
            "voice": voice_map.get(voice_type, "alloy"),
            "response_format": "mp3"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, timeout=30) as response:
                if response.status == 200:
                    filename = f"tts_openai_{voice_type}_{uuid.uuid4().hex[:8]}.mp3"
                    file_path = TTS_OUTPUT_DIR / filename
                    
                    audio_data = await response.read()
                    with open(file_path, "wb") as f:
                        f.write(audio_data)
                    
                    return str(file_path)
                else:
                    error_text = await response.text()
                    logger.error(f"OpenAI async TTS error {response.status}: {error_text}")
                    return None
                    
    except Exception as e:
        logger.error(f"OpenAI async TTS failed: {str(e)}")
        return None

def system_tts(text: str, voice_type: str) -> Optional[str]:
    """Use system TTS as last resort"""
    try:
        import subprocess
        import platform
        
        filename = f"tts_system_{voice_type}_{uuid.uuid4().hex[:8]}.wav"
        file_path = TTS_OUTPUT_DIR / filename
        
        system = platform.system().lower()
        
        if system == "darwin":  # macOS
            subprocess.run([
                "say", "-o", str(file_path), "-r", "150", text
            ], check=True)
        elif system == "linux":
            # Try espeak
            subprocess.run([
                "espeak", "-w", str(file_path), "-s", "140", text
            ], check=True)
        else:
            logger.error(f"System TTS not supported on {system}")
            return None
        
        if file_path.exists():
            logger.info(f"System TTS generated: {filename}")
            return str(file_path)
        
        return None
        
    except subprocess.CalledProcessError as e:
        logger.error(f"System TTS command failed: {str(e)}")
        return None
    except FileNotFoundError:
        logger.error("System TTS command not found")
        return None
    except Exception as e:
        logger.error(f"System TTS failed: {str(e)}")
        return None

def create_placeholder_audio(text: str, voice_type: str) -> str:
    """Create a simple placeholder audio file with tone"""
    try:
        import numpy as np
        import soundfile as sf
        
        # Generate simple tone pattern based on text length
        duration = min(max(len(text) * 0.1, 3), 30)  # 3-30 seconds based on text
        sr = 22050
        
        # Create a simple tone pattern
        t = np.linspace(0, duration, int(sr * duration))
        
        # Different tones for different voice types
        if voice_type == "breathing":
            # Gentle breathing rhythm
            freq = 220  # A3
            audio = 0.1 * np.sin(2 * np.pi * freq * t) * np.sin(2 * np.pi * 0.2 * t)
        elif voice_type in ["hypnosis", "long_hypnosis"]:
            # Low, calming tone
            freq = 110  # A2
            audio = 0.05 * np.sin(2 * np.pi * freq * t) * np.exp(-0.1 * t)
        else:
            # Neutral tone for narrative
            freq = 330  # E4
            audio = 0.08 * np.sin(2 * np.pi * freq * t) * (1 - 0.5 * t / duration)
        
        # Save placeholder audio
        filename = f"tts_placeholder_{voice_type}_{uuid.uuid4().hex[:8]}.wav"
        file_path = TTS_OUTPUT_DIR / filename
        
        sf.write(file_path, audio, sr)
        
        logger.info(f"Placeholder audio created: {filename}")
        return str(file_path)
        
    except Exception as e:
        logger.error(f"Failed to create placeholder audio: {str(e)}")
        return None

# Utility functions
def get_supported_voices() -> dict:
    """Get list of supported voices"""
    return {
        "elevenlabs": list(VOICE_IDS.keys()) if ELEVENLABS_API_KEY else [],
        "openai": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"] if OPENAI_API_KEY else [],
        "system": ["default"] if has_system_tts() else []
    }

def has_system_tts() -> bool:
    """Check if system TTS is available"""
    try:
        import subprocess
        import platform
        
        system = platform.system().lower()
        if system == "darwin":
            subprocess.run(["which", "say"], check=True, capture_output=True)
            return True
        elif system == "linux":
            subprocess.run(["which", "espeak"], check=True, capture_output=True)
            return True
        return False
    except:
        return False

def clean_old_files(max_age_hours: int = 24):
    """Clean up old TTS files"""
    try:
        import time
        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)
        
        for file_path in TTS_OUTPUT_DIR.iterdir():
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
                logger.info(f"Cleaned up old TTS file: {file_path.name}")
    except Exception as e:
        logger.error(f"Error cleaning old TTS files: {str(e)}")
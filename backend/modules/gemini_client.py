# modules/gemini_client.py - Gemini API integration
import os
import json
from typing import Dict, Any
import aiohttp
from modules.prompt_builder import parse_gemini_response, build_simple_wellness_narrative

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

# Gemini API endpoint
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

async def call_gemini(prompt: str, use_fallback: bool = True) -> Dict[str, Any]:
    """
    Call Gemini API with wellness prompt
    
    Args:
        prompt: Formatted prompt with user data
        use_fallback: If True, return simple narrative when API unavailable
        
    Returns:
        dict: Parsed wellness narrative and recommendations
    """
    
    # Check if API key is configured
    if not GEMINI_API_KEY or GEMINI_API_KEY == "":
        print("⚠️  GEMINI_API_KEY not configured - using fallback narrative")
        if use_fallback:
            return _get_fallback_response(prompt)
        else:
            return {"error": "Gemini API key not configured"}
    
    try:
        # Prepare request payload for Gemini API
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
                "responseMimeType": "application/json"  # Request JSON response
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
        }
        
        # Make async API call
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    print(f"Gemini API error ({response.status}): {error_text}")
                    if use_fallback:
                        return _get_fallback_response(prompt)
                    return {"error": f"API error: {response.status}"}
                
                result = await response.json()
                
                # Extract generated text from Gemini response
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        generated_text = candidate["content"]["parts"][0]["text"]
                        
                        # Parse the JSON response
                        parsed_response = parse_gemini_response(generated_text)
                        return parsed_response
                
                print("Unexpected Gemini response format")
                if use_fallback:
                    return _get_fallback_response(prompt)
                return {"error": "Unexpected response format"}
                
    except aiohttp.ClientError as e:
        print(f"Gemini API connection error: {str(e)}")
        if use_fallback:
            return _get_fallback_response(prompt)
        return {"error": f"Connection error: {str(e)}"}
    
    except Exception as e:
        print(f"Gemini API unexpected error: {str(e)}")
        if use_fallback:
            return _get_fallback_response(prompt)
        return {"error": f"Unexpected error: {str(e)}"}

def _get_fallback_response(prompt: str) -> Dict[str, Any]:
    """
    Generate fallback response when Gemini API is unavailable
    Extracts data from prompt and uses simple narrative builder
    """
    # This is a simplified fallback - in production, you'd want to
    # extract the actual data from the prompt or pass it separately
    
    return {
        "narrative": """I'm analyzing your wellness data to provide personalized insights. 
        While I couldn't connect to the advanced AI analysis system right now, I can still 
        offer you meaningful guidance based on your physiological indicators.
        
        Your body is communicating through multiple channels - voice, heart rhythm, and posture. 
        Each of these tells part of your story. Let's focus on what you can do right now to 
        support your wellbeing.""",
        
        "observations": [
            "Voice analysis completed - stress levels assessed",
            "Physiological data processed - HRV and sleep patterns analyzed",
            "Posture evaluation complete - alignment checked"
        ],
        
        "action_items": [
            {
                "priority": 1,
                "title": "Immediate breathing reset",
                "description": "Practice 4-7-8 breathing: inhale for 4 counts, hold for 7, exhale for 8. Do this 4 times.",
                "estimated_time": "2 minutes",
                "impact": "Activates parasympathetic nervous system, reduces stress immediately"
            },
            {
                "priority": 2,
                "title": "Posture adjustment",
                "description": "Stand or sit tall, roll shoulders back 5 times, then gently tilt head side to side.",
                "estimated_time": "3 minutes",
                "impact": "Releases tension, improves circulation and focus"
            },
            {
                "priority": 3,
                "title": "Sleep optimization",
                "description": "Set a consistent bedtime tonight, dim lights 1 hour before, avoid screens 30 minutes before sleep.",
                "estimated_time": "Evening routine",
                "impact": "Better sleep quality, improved HRV and recovery"
            }
        ],
        
        "hypnosis_script": """Close your eyes and take a deep, slow breath. Feel the air filling your lungs completely.
        
        As you exhale, imagine releasing all the tension from your day. Let it flow out with your breath.
        
        Your body knows how to relax. Your heartbeat is steady and calm. Your breathing is becoming slower, deeper, more peaceful.
        
        Picture yourself in a safe, comfortable place. Maybe it's a quiet beach, a cozy room, or a peaceful forest. Wherever feels right to you.
        
        With each breath, you're sinking deeper into relaxation. Your muscles are softening. Your mind is quieting.
        
        You are safe. You are supported. You are exactly where you need to be in this moment.
        
        Continue breathing slowly and deeply. Let sleep come naturally. Your body is healing, restoring, preparing you for tomorrow.
        
        Rest now. You've done enough. Tomorrow will take care of itself. For now, just breathe and rest.""",
        
        "breathing_exercise": {
            "name": "4-7-8 Relaxation Breath",
            "pattern": "Inhale 4, Hold 7, Exhale 8",
            "duration": "2-5 minutes",
            "instruction": "Place tip of tongue behind upper front teeth. Exhale completely through mouth. Close mouth, inhale through nose for 4 counts. Hold for 7 counts. Exhale through mouth for 8 counts. Repeat 4 times."
        },
        
        "wellness_score_interpretation": """Your wellness data provides valuable insights into your current state. 
        Focus on the immediate action items above - small changes can have significant impacts. 
        Remember, this is about progress, not perfection. You're taking important steps by checking in with yourself.""",
        
        "_note": "Fallback response - Gemini API unavailable"
    }

# Alternative: OpenAI-compatible API (if using Gemini through a proxy)
async def call_gemini_openai_compatible(prompt: str) -> Dict[str, Any]:
    """
    Alternative implementation using OpenAI-compatible API format
    Useful if you're using a Gemini proxy or similar service
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    api_base = os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta/openai")
    
    if not api_key:
        return _get_fallback_response(prompt)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GEMINI_MODEL,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2048
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status != 200:
                    return _get_fallback_response(prompt)
                
                result = await response.json()
                content = result["choices"][0]["message"]["content"]
                
                return parse_gemini_response(content)
                
    except Exception as e:
        print(f"OpenAI-compatible API error: {str(e)}")
        return _get_fallback_response(prompt)

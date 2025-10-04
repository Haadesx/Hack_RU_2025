# modules/gemini_client.py
import os
import json
import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Fallback to OpenAI-compatible API if preferred
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

async def call_gemini(prompt: str, model: str = None) -> Dict[str, Any]:
    """
    Call Gemini API with the given prompt
    Returns parsed JSON response with narrative, observations, action_items, etc.
    """
    try:
        # Use specified model or default
        model_name = model or GEMINI_MODEL
        
        # Try Gemini API first if API key is available
        if GEMINI_API_KEY:
            result = await call_gemini_api(prompt, model_name)
            if result and not result.get('error'):
                return result
        
        # Fallback to OpenAI-compatible API
        if OPENAI_API_KEY:
            result = await call_openai_api(prompt)
            if result and not result.get('error'):
                return result
        
        # Ultimate fallback: return structured mock response
        logger.warning("No API keys available, returning mock response")
        return generate_mock_response(prompt)
        
    except Exception as e:
        logger.error(f"Error calling LLM API: {str(e)}")
        return generate_mock_response(prompt, error=str(e))

async def call_gemini_api(prompt: str, model: str) -> Dict[str, Any]:
    """Call Google's Gemini API"""
    try:
        url = GEMINI_API_URL.format(model=model)
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract text from Gemini response format
                    if 'candidates' in data and len(data['candidates']) > 0:
                        text_content = data['candidates'][0]['content']['parts'][0]['text']
                        return parse_llm_response(text_content)
                    else:
                        logger.error(f"Unexpected Gemini response format: {data}")
                        return {"error": "Unexpected response format"}
                else:
                    error_text = await response.text()
                    logger.error(f"Gemini API error {response.status}: {error_text}")
                    return {"error": f"API error: {response.status}"}
                    
    except asyncio.TimeoutError:
        logger.error("Gemini API timeout")
        return {"error": "API timeout"}
    except Exception as e:
        logger.error(f"Gemini API call failed: {str(e)}")
        return {"error": str(e)}

async def call_openai_api(prompt: str) -> Dict[str, Any]:
    """Call OpenAI-compatible API as fallback"""
    try:
        url = f"{OPENAI_BASE_URL}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Format prompt for chat completion
        messages = [
            {"role": "system", "content": "You are a compassionate wellness assistant. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if 'choices' in data and len(data['choices']) > 0:
                        text_content = data['choices'][0]['message']['content']
                        return parse_llm_response(text_content)
                    else:
                        return {"error": "Unexpected response format"}
                else:
                    error_text = await response.text()
                    logger.error(f"OpenAI API error {response.status}: {error_text}")
                    return {"error": f"API error: {response.status}"}
                    
    except Exception as e:
        logger.error(f"OpenAI API call failed: {str(e)}")
        return {"error": str(e)}

def parse_llm_response(text_content: str) -> Dict[str, Any]:
    """Parse LLM response text into structured JSON"""
    try:
        # Clean up the response text
        text_content = text_content.strip()
        
        # Try to extract JSON from the response
        if text_content.startswith('```json'):
            # Remove markdown code blocks
            text_content = text_content.replace('```json', '').replace('```', '').strip()
        elif text_content.startswith('```'):
            text_content = text_content.replace('```', '').strip()
        
        # Try to parse as JSON
        parsed = json.loads(text_content)
        
        # Validate required fields
        required_fields = ['narrative', 'observations', 'action_items']
        for field in required_fields:
            if field not in parsed:
                logger.warning(f"Missing required field: {field}")
                parsed[field] = f"Unable to generate {field}"
        
        # Ensure observations and action_items are lists
        if not isinstance(parsed['observations'], list):
            parsed['observations'] = [str(parsed['observations'])]
        
        if not isinstance(parsed['action_items'], list):
            parsed['action_items'] = [str(parsed['action_items'])]
        
        return parsed
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM response: {str(e)}")
        logger.error(f"Response text: {text_content}")
        
        # Try to extract useful information even if JSON is malformed
        return extract_fallback_response(text_content)

def extract_fallback_response(text: str) -> Dict[str, Any]:
    """Extract useful information from malformed responses"""
    lines = text.split('\n')
    
    narrative = ""
    observations = []
    action_items = []
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Look for section headers
        if 'narrative' in line.lower():
            current_section = 'narrative'
        elif 'observation' in line.lower():
            current_section = 'observations'
        elif 'action' in line.lower() or 'recommendation' in line.lower():
            current_section = 'action_items'
        elif line.startswith('-') or line.startswith('•'):
            # Bullet point
            item = line.lstrip('- •').strip()
            if current_section == 'observations':
                observations.append(item)
            elif current_section == 'action_items':
                action_items.append(item)
        else:
            # Regular text
            if current_section == 'narrative':
                narrative += line + " "
    
    return {
        'narrative': narrative.strip() if narrative else "I'm here to support your wellness journey based on your check-in data.",
        'observations': observations if observations else ["Your check-in data has been analyzed"],
        'action_items': action_items if action_items else ["Take a few deep breaths", "Stay hydrated", "Check in with yourself regularly"],
        'hypnosis_script': ""
    }

def generate_mock_response(prompt: str, error: str = None) -> Dict[str, Any]:
    """Generate a structured mock response for testing/fallback"""
    
    # Analyze prompt for context clues
    stress_level = "moderate"
    if "stress_score" in prompt:
        # Try to extract stress level from prompt
        if "stress_score: 0." in prompt:
            score_part = prompt.split("stress_score: 0.")[1][:1]
            try:
                score = float(f"0.{score_part}")
                if score < 0.3:
                    stress_level = "low"
                elif score > 0.7:
                    stress_level = "high"
            except:
                pass
    
    # Generate contextual response based on stress level
    if stress_level == "high":
        narrative = """I can sense that you're experiencing some stress right now, and I want you to know that what you're feeling is completely valid. Your body and mind are working hard, and it's important to acknowledge that. The data from your check-in shows elevated stress indicators, which tells me you might benefit from some focused attention on nervous system regulation.

This is actually valuable information - your awareness of your stress levels is the first step toward managing them effectively. Let's focus on some immediate strategies that can help bring your system back into balance."""
        
        observations = [
            "Elevated stress indicators detected in voice analysis",
            "Your nervous system may be in a heightened state of activation",
            "Body may benefit from intentional relaxation techniques",
            "Current stress levels suggest need for immediate self-care"
        ]
        
        action_items = [
            "Take 5 deep breaths right now using 4-7-8 technique (inhale 4, hold 7, exhale 8)",
            "Step away from stressful tasks for 10 minutes if possible",
            "Drink a glass of water and do gentle neck rolls",
            "Consider a brief walk or stretching break within the next hour"
        ]
        
    elif stress_level == "low":
        narrative = """Your check-in data suggests you're in a relatively calm and balanced state right now, which is wonderful to see. Your stress indicators are low, and this presents a great opportunity to maintain and build upon this positive state. When we're feeling more centered, it's an ideal time to engage in activities that support our overall wellness.

Use this stable energy to reinforce healthy habits and perhaps tackle tasks that require focus. Your body seems to be in a good place for both productivity and restoration."""
        
        observations = [
            "Low stress indicators suggest a calm, balanced state",
            "Good opportunity for focused activities or deeper relaxation",
            "Nervous system appears well-regulated",
            "Current state is conducive to building positive habits"
        ]
        
        action_items = [
            "Maintain this balanced state with mindful breathing",
            "Consider engaging in a fulfilling activity you enjoy",
            "Use this calm energy for tasks requiring focus",
            "Practice gratitude for this peaceful moment"
        ]
        
    else:  # moderate stress
        narrative = """Your check-in shows a moderate level of stress, which is quite common and manageable. You're in a space where you're experiencing some activation but haven't moved into overwhelming territory. This is actually a good place to work from - you have energy available while still maintaining the capacity to make thoughtful choices about your wellbeing.

Your body is communicating its needs clearly, and with some gentle attention, you can guide yourself toward greater ease and effectiveness."""
        
        observations = [
            "Moderate stress levels indicate manageable activation",
            "Good balance between energy and calm",
            "Optimal state for gentle wellness interventions",
            "Body is responsive to stress management techniques"
        ]
        
        action_items = [
            "Take 3 conscious breaths to center yourself",
            "Check in with your posture and adjust if needed",
            "Stay hydrated and consider a healthy snack",
            "Plan a brief relaxing activity for later today"
        ]
    
    hypnosis_script = """Close your eyes if you feel comfortable, or simply soften your gaze. Begin to notice your breathing, without trying to change it, just observing the natural rhythm of air moving in and out of your body.

With each exhale, allow your shoulders to drop just a little more. Feel your feet on the ground, connecting you to the earth beneath you. You are safe, you are supported, and you are exactly where you need to be right now.

Imagine a warm, golden light beginning to glow in your chest, right at your heart center. This light is peaceful and healing. With each breath, this light grows slightly brighter and warmer, spreading slowly through your body. It moves through your arms, down through your torso, and into your legs, carrying with it a deep sense of calm and restoration.

As this light fills your entire being, notice how your body begins to feel heavy and relaxed, sinking comfortably into rest. Your mind becomes quiet and still, like a calm lake on a peaceful morning. You are ready for deep, healing sleep that will restore and rejuvenate every cell in your body."""
    
    response = {
        'narrative': narrative,
        'observations': observations,
        'action_items': action_items,
        'hypnosis_script': hypnosis_script
    }
    
    if error:
        response['_error'] = f"Mock response due to: {error}"
        response['_note'] = "This is a fallback response for demonstration purposes"
    
    return response

# Utility functions for specific use cases
async def quick_mood_assessment(audio_features: Dict[str, Any]) -> Dict[str, Any]:
    """Quick mood assessment from voice features alone"""
    try:
        prompt = f"""Based on voice analysis data, provide a brief mood assessment in JSON format:

Voice Analysis:
- Stress score: {audio_features.get('stress_score', 0.5)}
- Emotional state: {audio_features.get('emotional_state', 'neutral')}
- Energy level: {audio_features.get('energy', 0.0)}

Response format:
{{
    "mood": "description",
    "energy": "low/moderate/high", 
    "stress": "low/moderate/high",
    "suggestions": ["immediate suggestion 1", "immediate suggestion 2"]
}}"""

        result = await call_gemini(prompt)
        return result if result and not result.get('error') else {
            "mood": "neutral",
            "energy": "moderate",
            "stress": "moderate", 
            "suggestions": ["Take a deep breath", "Stay present"]
        }
        
    except Exception as e:
        logger.error(f"Quick mood assessment failed: {str(e)}")
        return {"mood": "unknown", "error": str(e)}
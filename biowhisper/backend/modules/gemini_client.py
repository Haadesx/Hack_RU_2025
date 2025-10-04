from typing import Dict, Any
import os
import json

# This is a stubbed async client compatible with FastAPI usage.
# Replace with actual Gemini API calls during integration.

async def call_gemini(prompt: str) -> Dict[str, Any]:
    # In hackathon mode, return a realistic mock. Replace when API key available.
    mock = {
        "narrative": (
            "I hear some elevated pace and energy in your voice, which can happen on busy days. "
            "It also sounds like you're pushing through with focus. Let's make space for a quick reset so your body and mind can sync."
        ),
        "observations": [
            "Slightly increased tempo and energy suggesting activation",
            "No posture or wearable data provided yet",
        ],
        "action_items": [
            "Take a 3-minute box-breathing break now: inhale 4, hold 4, exhale 4, hold 4, repeat",
            "Drink a glass of water and set a 60-minute movement reminder",
            "Plan a 10-minute wind-down before bed: dim lights, no screens",
        ],
        "hypnosis_script": (
            "Find a comfortable position. Gently let your shoulders soften as you breathe in through the nose..."
        ),
    }
    return mock

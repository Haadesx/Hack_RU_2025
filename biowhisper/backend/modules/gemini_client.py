from __future__ import annotations
from typing import Dict, Any
import json

# Hackathon-friendly stub that returns deterministic JSON-shaped output.
# Replace with real Gemini API call later.


async def call_gemini(prompt: str) -> Dict[str, Any]:
    try:
        # A minimal heuristic based on presence of stress features
        has_stress = "stress_score" in prompt
        narrative = (
            "Thanks for checking in. From your voice sample and available signals, I'm noticing some markers of tension. "
            "Nothing here is diagnostic, but it may help to slow down and reset. "
            "Let's focus on small steps you can take today."
        )
        observations = [
            "Voice energy and tempo suggest mild activation",
            "No wearable data attached in this run (simulated)",
            "Posture scan not available (optional)",
        ]
        action_items = [
            "Try a 3-minute box-breathing: inhale 4s, hold 4s, exhale 4s, hold 4s",
            "Drink a glass of water and take a brief 5-minute walk",
            "Plan a consistent sleep window tonight (aim for 8 hours in bed)",
        ]
        hypnosis_script = (
            "Find a comfortable position. Gently close your eyes. As you breathe in, imagine a calm tide rising, and as you exhale, the tide slowly recedes. "
            "Let your shoulders drop and your jaw soften. With each breath, invite warmth across your chest and stillness behind your eyes. "
            "Notice the space between thoughts becoming wider and softer. If worries appear, acknowledge them and let them drift to the side like leaves on water. "
            "Feel your body supported. You are safe. With the next exhale, release what you no longer need. Breathe in ease. Breathe out any remaining tension. "
            "When you're ready, return gently, carrying this calm with you."
        )
        data = {
            "narrative": narrative,
            "observations": observations,
            "action_items": action_items,
            "hypnosis_script": hypnosis_script,
        }
        # Validate JSON-serializable
        json.dumps(data)
        return data
    except Exception:
        # Super-safe fallback
        return {
            "narrative": "I couldn't generate a narrative right now.",
            "observations": [],
            "action_items": ["Take 3 slow breaths"],
            "hypnosis_script": "",
        }

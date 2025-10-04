from typing import Dict, Any
import json


def build_gemini_prompt(
    audio_feats: Dict[str, Any],
    wearable_summary: Dict[str, Any],
    pose_summary: Dict[str, Any],
) -> str:
    system = (
        "You are a compassionate, clinically-informed wellness assistant. "
        "Given the user's physiological and sensor analysis below, produce a concise, empathetic narrative (2-3 short paragraphs), "
        "a bulleted set of 3 immediate action items ranked by impact, and a short sleep-hypnosis script (200-300 words) that is calming and non-medical. "
        "Output MUST be a JSON object with keys: narrative, observations, action_items (list), hypnosis_script."
    )

    user_data = {
        "voice_features": audio_feats,
        "wearable_summary": wearable_summary,
        "pose_summary": pose_summary,
        # NOTE: the caller can augment local_time if desired
    }

    return f"SYSTEM: {system}\nUSER DATA:\n{json.dumps(user_data)}\nConstraints: do NOT provide definitive medical diagnoses. Use plain language, supportive tone. Action items should be specific, time-bound, and include one quick breathing exercise the user can do immediately."

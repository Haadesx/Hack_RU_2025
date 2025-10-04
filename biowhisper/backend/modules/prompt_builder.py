from __future__ import annotations
from typing import Dict, Any


def build_gemini_prompt(
    audio_feats: Dict[str, Any],
    wearable_summary: Dict[str, Any] | None = None,
    pose_summary: Dict[str, Any] | None = None,
    local_time_iso: str | None = None,
) -> str:
    wearable_summary = wearable_summary or {}
    pose_summary = pose_summary or {}

    system = (
        "You are a compassionate, clinically-informed wellness assistant. "
        "Given the user's physiological and sensor analysis below, produce a concise, empathetic narrative (2-3 short paragraphs), "
        "a bulleted set of 3 immediate action items ranked by impact, and a short sleep-hypnosis script (200-300 words) that is calming and non-medical. "
        "Output MUST be a JSON object with keys: narrative, observations, action_items (list), hypnosis_script. "
        "Do not give medical diagnoses. Use plain, supportive language."
    )

    user_data = {
        "voice_features": audio_feats,
        "wearable_summary": wearable_summary,
        "pose_summary": pose_summary,
        "local_time": local_time_iso,
    }

    prompt = (
        f"SYSTEM: {system}\n\n"  # noqa: E501
        f"USER DATA:\n{user_data}\n\n"
        "Constraints: do NOT provide definitive medical diagnoses. Use plain language, supportive tone. "
        "Action items should be specific, time-bound, and include one quick breathing exercise the user can do immediately."
    )
    return prompt

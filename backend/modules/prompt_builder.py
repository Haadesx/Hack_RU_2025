# modules/prompt_builder.py
from datetime import datetime
from typing import Dict, Any

def build_gemini_prompt(audio_feats: Dict, wearable_summary: Dict, pose_summary: Dict) -> str:
    """
    Build a comprehensive prompt for Gemini to generate wellness insights
    """
    
    # Extract key metrics
    stress_score = audio_feats.get('stress_score', 0.5)
    energy_level = audio_feats.get('energy', 0.5)
    speaking_rate = audio_feats.get('speaking_rate', 1.0)
    tone_indicators = audio_feats.get('tone_indicators', {})
    
    # Wearable data
    avg_hr = wearable_summary.get('heart_rate', {}).get('average', 70)
    wellness_score = wearable_summary.get('wellness_score', 0.5)
    hrv_rmssd = wearable_summary.get('hrv_metrics', {}).get('rmssd', 30)
    
    # Posture data
    posture_score = pose_summary.get('overall_posture_score', 0.5)
    forward_head_angle = pose_summary.get('forward_head_angle', 0)
    tension_flags = pose_summary.get('tension_flags', {})
    
    # Current time context
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hour = datetime.now().hour
    
    # Determine time of day context
    if 5 <= hour < 12:
        time_context = "morning"
    elif 12 <= hour < 17:
        time_context = "afternoon"
    elif 17 <= hour < 21:
        time_context = "evening"
    else:
        time_context = "night"
    
    prompt = f"""
SYSTEM: You are a compassionate, clinically-informed wellness assistant named BioWhisper. Your role is to provide personalized, empathetic wellness insights based on physiological and behavioral data. You must:

1. Provide supportive, non-medical guidance
2. Use warm, encouraging language
3. Focus on actionable, time-bound recommendations
4. Never provide medical diagnoses or treatment advice
5. Always emphasize the user's agency and capability for improvement

USER DATA ANALYSIS:
Current Time: {current_time} ({time_context})

VOICE ANALYSIS:
- Stress Level: {stress_score:.2f} (0=calm, 1=stressed)
- Energy Level: {energy_level:.2f} (0=low, 1=high)
- Speaking Rate: {speaking_rate:.2f} (words per second)
- Voice Tone: {tone_indicators}

WEARABLE DATA:
- Average Heart Rate: {avg_hr:.0f} bpm
- Heart Rate Variability (RMSSD): {hrv_rmssd:.1f} ms
- Overall Wellness Score: {wellness_score:.2f} (0=poor, 1=excellent)

POSTURE ANALYSIS:
- Overall Posture Score: {posture_score:.2f} (0=poor, 1=excellent)
- Forward Head Angle: {forward_head_angle:.1f} degrees
- Tension Indicators: {tension_flags}

TASK: Generate a comprehensive wellness response with the following structure:

1. NARRATIVE: Write 2-3 empathetic paragraphs that acknowledge the user's current state, validate their experience, and provide gentle insights about what the data suggests about their wellbeing.

2. OBSERVATIONS: List 3-4 key observations about their current state, written in supportive language.

3. ACTION_ITEMS: Provide exactly 3 prioritized, specific, time-bound action items that the user can implement immediately. Include one breathing exercise they can do right now.

4. BREATHING_SCRIPT: Write a 3-minute guided breathing exercise script (200-300 words) that is calming, non-medical, and appropriate for their current stress level.

5. SLEEP_HYPNOSIS_SCRIPT: Write a short sleep hypnosis script (150-200 words) for relaxation and better sleep.

OUTPUT FORMAT: Return ONLY a valid JSON object with these exact keys:
{{
    "narrative": "Your empathetic narrative here...",
    "observations": ["Observation 1", "Observation 2", "Observation 3", "Observation 4"],
    "action_items": ["Action 1", "Action 2", "Action 3"],
    "breathing_script": "Your breathing exercise script here...",
    "sleep_hypnosis_script": "Your sleep hypnosis script here..."
}}

IMPORTANT: 
- Use "you" and "your" to make it personal
- Be encouraging and supportive
- Focus on what they can control
- Keep language simple and accessible
- Make recommendations specific and actionable
- End on a positive, empowering note
"""

    return prompt

def build_quick_breathing_prompt(stress_level: float) -> str:
    """Build a quick breathing exercise prompt based on stress level"""
    
    if stress_level > 0.7:
        breathing_type = "calming"
        duration = "5 minutes"
        technique = "4-7-8 breathing"
    elif stress_level > 0.4:
        breathing_type = "centering"
        duration = "3 minutes"
        technique = "box breathing"
    else:
        breathing_type = "energizing"
        duration = "2 minutes"
        technique = "rhythmic breathing"
    
    return f"""
Create a {duration} {breathing_type} breathing exercise using {technique}.
Make it gentle, encouraging, and easy to follow.
Include specific timing cues and calming imagery.
Keep it under 200 words and make it feel personal and supportive.
"""

def build_sleep_hypnosis_prompt(sleep_quality_score: float, current_hour: int) -> str:
    """Build a personalized sleep hypnosis prompt"""
    
    if current_hour >= 22 or current_hour <= 6:
        time_context = "bedtime"
        focus = "deep relaxation and sleep preparation"
    else:
        time_context = "relaxation"
        focus = "stress relief and mental calm"
    
    if sleep_quality_score < 0.5:
        emphasis = "deep sleep and restoration"
    else:
        emphasis = "maintaining healthy sleep patterns"
    
    return f"""
Create a {time_context} hypnosis script focused on {focus} and {emphasis}.
Make it soothing, non-medical, and personalized.
Include gentle imagery and progressive relaxation.
Keep it under 200 words and use calming, repetitive language.
"""
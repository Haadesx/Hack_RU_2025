# modules/prompt_builder.py
from typing import Dict, Any, Optional
from datetime import datetime
import json

def build_gemini_prompt(
    audio_feats: Dict[str, Any],
    wearable_summary: Dict[str, Any],
    pose_summary: Dict[str, Any],
    user_context: Optional[Dict[str, Any]] = None
) -> str:
    """
    Build a comprehensive prompt for Gemini to analyze wellness data
    Returns a formatted prompt string
    """
    
    # Current timestamp for context
    current_time = datetime.now().isoformat()
    
    # Build the system prompt
    system_prompt = """You are a compassionate, clinically-informed wellness assistant named BioWhisper. 
Your role is to analyze physiological and behavioral data to provide empathetic, actionable wellness guidance.

IMPORTANT GUIDELINES:
- Use a warm, supportive tone that acknowledges the person's experience
- Provide specific, actionable recommendations that can be implemented immediately  
- NEVER provide medical diagnoses or replace professional healthcare
- Focus on wellness optimization rather than medical treatment
- Be encouraging and highlight positive aspects when present
- Keep language accessible and non-technical for general audiences

OUTPUT FORMAT: Your response MUST be valid JSON with exactly these keys:
{
    "narrative": "A compassionate 2-3 paragraph summary that validates their experience and provides context",
    "observations": ["3-5 key observations about their current state"],
    "action_items": ["3-4 specific, time-bound actions they can take today"],
    "hypnosis_script": "A calming 200-300 word sleep/relaxation script (if appropriate)"
}"""

    # Build user data section
    user_prompt = f"""
CURRENT ANALYSIS DATA (timestamp: {current_time}):

VOICE & EMOTIONAL ANALYSIS:
{format_audio_data(audio_feats)}

BIOMETRIC DATA:
{format_wearable_data(wearable_summary)}

POSTURE & PHYSICAL STATE:
{format_posture_data(pose_summary)}

CONTEXT:
- Time of analysis: {datetime.now().strftime('%A, %B %d at %I:%M %p')}
- Analysis requested by user seeking wellness insights
{format_user_context(user_context) if user_context else ""}

Please provide a comprehensive wellness assessment following the JSON format specified above. Focus on being supportive and actionable."""

    return f"{system_prompt}\n\n{user_prompt}"

def format_audio_data(audio_feats: Dict[str, Any]) -> str:
    """Format audio analysis data for the prompt"""
    if not audio_feats or audio_feats.get('error'):
        return "- Voice analysis: Limited data available"
    
    stress_level = audio_feats.get('stress_score', 0.5)
    emotional_state = audio_feats.get('emotional_state', 'neutral')
    energy_level = audio_feats.get('energy', 0.0)
    
    # Interpret stress level
    if stress_level < 0.3:
        stress_desc = "low stress indicators"
    elif stress_level < 0.6:
        stress_desc = "moderate stress indicators"
    else:
        stress_desc = "elevated stress indicators"
    
    # Interpret energy
    if energy_level < 0.01:
        energy_desc = "low vocal energy (possibly tired)"
    elif energy_level < 0.03:
        energy_desc = "moderate vocal energy"
    else:
        energy_desc = "high vocal energy"
    
    return f"""- Stress level: {stress_level:.2f} ({stress_desc})
- Emotional tone: {emotional_state}
- Vocal energy: {energy_desc}
- Speaking characteristics: Tempo {audio_feats.get('tempo', 0):.1f} BPM, Pitch variance {audio_feats.get('pitch_var', 0):.1f}
- Voice activity quality: {audio_feats.get('analysis_quality', 'unknown')}"""

def format_wearable_data(wearable_summary: Dict[str, Any]) -> str:
    """Format wearable/HRV data for the prompt"""
    if not wearable_summary or wearable_summary.get('error'):
        return "- Biometric data: No wearable data available for this session"
    
    hrv_status = wearable_summary.get('hrv_status', 'unknown')
    recovery_score = wearable_summary.get('recovery_score', 0.5)
    sleep_quality = wearable_summary.get('sleep_quality_score', 0.5)
    sleep_debt = wearable_summary.get('sleep_debt_hours', 0)
    
    return f"""- Heart Rate Variability: {hrv_status} (RMSSD: {wearable_summary.get('hrv_rmssd', 'N/A')})
- Recovery score: {recovery_score:.2f}/1.0
- Recent sleep quality: {sleep_quality:.2f}/1.0 ({wearable_summary.get('total_sleep_time', 0):.1f} hours)
- Sleep debt: {sleep_debt:.1f} hours
- Average heart rate: {wearable_summary.get('avg_heart_rate', 'N/A')} BPM
- Circadian alignment: {wearable_summary.get('circadian_alignment', 'unknown')}"""

def format_posture_data(pose_summary: Dict[str, Any]) -> str:
    """Format posture analysis data for the prompt"""
    if not pose_summary or pose_summary.get('error'):
        return "- Posture analysis: No camera data available for this session"
    
    posture_score = pose_summary.get('posture_score', 0.5)
    risk_level = pose_summary.get('risk_level', 'unknown')
    
    return f"""- Overall posture score: {posture_score:.2f}/1.0
- Posture risk level: {risk_level}
- Head position: {pose_summary.get('head_position', 'unknown')}
- Shoulder alignment: {pose_summary.get('shoulder_status', 'unknown')}
- Spinal alignment: {pose_summary.get('spinal_status', 'unknown')}"""

def format_user_context(user_context: Dict[str, Any]) -> str:
    """Format additional user context"""
    context_items = []
    
    if user_context.get('recent_stressors'):
        context_items.append(f"- Recent stressors: {user_context['recent_stressors']}")
    
    if user_context.get('wellness_goals'):
        context_items.append(f"- Wellness goals: {user_context['wellness_goals']}")
    
    if user_context.get('current_challenges'):
        context_items.append(f"- Current challenges: {user_context['current_challenges']}")
    
    return "\n".join(context_items) if context_items else ""

def create_breathing_exercise_prompt() -> str:
    """Create a prompt specifically for breathing exercise generation"""
    return """Create a 3-minute guided breathing exercise script. Use calming, supportive language with specific timing cues. 
    
The script should:
- Start with grounding and awareness
- Use 4-7-8 breathing technique (inhale 4, hold 7, exhale 8)
- Include body awareness and relaxation cues
- End with gentle transition back to normal breathing
- Be exactly suitable for text-to-speech conversion

Format as plain text suitable for TTS, approximately 300-400 words."""

def create_sleep_hypnosis_prompt(duration_minutes: int = 10, focus_area: str = "general relaxation") -> str:
    """Create a prompt for sleep hypnosis script generation"""
    return f"""Create a {duration_minutes}-minute sleep hypnosis script focused on {focus_area}.

The script should:
- Use progressive relaxation techniques
- Include calming imagery and metaphors
- Have a slow, peaceful pace suitable for sleep induction
- Incorporate positive suggestions for restful sleep
- End with deep sleep suggestions
- Be written in second person ("you")
- Use gentle, soothing language throughout

The script should be approximately {duration_minutes * 80} words (80 words per minute for slow, meditative pace).
Format as plain text suitable for text-to-speech conversion."""

def build_mood_check_prompt(audio_features: Dict[str, Any]) -> str:
    """Build a prompt specifically for mood assessment from voice"""
    stress_score = audio_features.get('stress_score', 0.5)
    emotional_state = audio_features.get('emotional_state', 'neutral')
    energy = audio_features.get('energy', 0.0)
    
    return f"""Based on this voice analysis, provide a brief mood assessment:

Voice Data:
- Stress indicators: {stress_score:.2f}/1.0
- Emotional state: {emotional_state}
- Energy level: {energy:.3f}
- Analysis quality: {audio_features.get('analysis_quality', 'unknown')}

Provide a JSON response with:
{{
    "mood_summary": "Brief, empathetic description of detected mood",
    "confidence": 0.8,
    "suggestions": ["2-3 immediate mood support suggestions"]
}}

Be gentle and supportive in your assessment."""

# Template prompts for different scenarios
PROMPT_TEMPLATES = {
    "morning_checkin": """
You're analyzing a morning check-in. Focus on:
- Energy levels for the day ahead
- Sleep recovery assessment  
- Motivation and readiness
- Gentle activation recommendations
""",
    
    "evening_checkin": """
You're analyzing an evening check-in. Focus on:
- Stress accumulated during the day
- Relaxation and wind-down needs
- Sleep preparation recommendations
- Reflection on the day's experiences
""",
    
    "stress_response": """
The data indicates elevated stress. Focus on:
- Immediate stress relief techniques
- Nervous system regulation
- Practical coping strategies
- Validation of their experience
""",
    
    "recovery_focus": """
The data suggests recovery needs. Focus on:
- Rest and restoration recommendations
- Gentle movement or complete rest
- Nutrition and hydration
- Sleep optimization
"""
}

def get_contextual_prompt_additions(audio_feats: Dict, wearable_data: Dict, pose_data: Dict) -> str:
    """Add contextual prompt elements based on data patterns"""
    additions = []
    
    # High stress context
    if audio_feats.get('stress_score', 0) > 0.7:
        additions.append(PROMPT_TEMPLATES["stress_response"])
    
    # Recovery needs context  
    recovery_score = wearable_data.get('recovery_score', 0.5)
    if recovery_score < 0.4:
        additions.append(PROMPT_TEMPLATES["recovery_focus"])
    
    # Time-based context
    current_hour = datetime.now().hour
    if 5 <= current_hour <= 11:
        additions.append(PROMPT_TEMPLATES["morning_checkin"])
    elif 18 <= current_hour <= 23:
        additions.append(PROMPT_TEMPLATES["evening_checkin"])
    
    return "\n".join(additions)
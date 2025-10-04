# modules/prompt_builder.py - Gemini prompt engineering for wellness narratives
from datetime import datetime
from typing import Dict, Any
import json

def build_gemini_prompt(
    audio_feats: Dict[str, Any],
    wearable_summary: Dict[str, Any],
    pose_summary: Dict[str, Any]
) -> str:
    """
    Build comprehensive prompt for Gemini to generate compassionate wellness narrative
    
    Args:
        audio_feats: Voice analysis results
        wearable_summary: HRV and sleep data summary
        pose_summary: Posture analysis results
        
    Returns:
        str: Formatted prompt for Gemini API
    """
    
    # Get current time for circadian context
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_hour = datetime.now().hour
    
    # Determine time of day context
    if 5 <= current_hour < 12:
        time_context = "morning"
    elif 12 <= current_hour < 17:
        time_context = "afternoon"
    elif 17 <= current_hour < 22:
        time_context = "evening"
    else:
        time_context = "night"
    
    # Format the data sections
    audio_summary = f"""
Voice Analysis:
- Stress Score: {audio_feats.get('stress_score', 0.5):.2f} (0=calm, 1=high stress)
- Emotional Tone: {audio_feats.get('emotional_tone', 'neutral')}
- Speaking Energy: {audio_feats.get('energy', 0):.3f}
- Vocal Tension Indicators: {audio_feats.get('zero_crossing_rate', 0):.3f}
- Speaking Duration: {audio_feats.get('speaking_duration_seconds', 0):.1f} seconds
    """
    
    wearable_summary_text = f"""
Physiological Data:
- HRV (RMSSD): {wearable_summary.get('hrv_rmssd', 'N/A')} ms
- Average Heart Rate: {wearable_summary.get('avg_hr', 'N/A')} bpm
- Resting Heart Rate: {wearable_summary.get('resting_hr', 'N/A')} bpm
- Total Sleep: {wearable_summary.get('total_sleep_hours', 'N/A')} hours
- Sleep Debt: {wearable_summary.get('sleep_debt_hours', 'N/A')} hours
- Sleep Midpoint: {wearable_summary.get('sleep_midpoint', 'N/A')}
- Circadian Status: {wearable_summary.get('circadian_status', 'unknown')}
- Wellness Score: {wearable_summary.get('wellness_score', 'N/A')}/100
    """
    
    pose_summary_text = f"""
Posture Analysis:
- Alignment Score: {pose_summary.get('alignment_score', 'N/A')}
- Posture Status: {pose_summary.get('posture_status', 'not assessed')}
- Tension Indicators: {', '.join(pose_summary.get('tension_indicators', ['none detected']))}
- Recommendations: {', '.join(pose_summary.get('recommendations', ['N/A']))}
    """
    
    # Build the complete prompt
    prompt = f"""You are a compassionate, clinically-informed wellness assistant named BioWhisper. You analyze physiological data and create personalized, empathetic wellness guidance.

Given the user's current physiological and behavioral analysis below, produce a wellness report in **strict JSON format only** (no markdown, no code blocks, no extra text).

CURRENT CONTEXT:
- Time: {current_time} ({time_context})
- Assessment Type: Comprehensive wellness check-in

USER DATA:
{audio_summary}

{wearable_summary_text}

{pose_summary_text}

INSTRUCTIONS:
1. Analyze all data holistically - look for patterns between voice, physiology, and posture
2. Consider time of day and circadian alignment
3. Use warm, non-judgmental language
4. Focus on actionable insights, not just observations
5. Prioritize immediate interventions that can help right now
6. Do NOT provide medical diagnoses - frame as wellness optimization
7. Be specific with recommendations (include timing, duration, techniques)

OUTPUT REQUIREMENTS:
Return ONLY a valid JSON object with these exact keys:

{{
  "narrative": "2-3 paragraph compassionate summary that weaves together the data into a coherent story about what the user's body is communicating. Use 'you' language. Be warm and supportive.",
  
  "observations": [
    "Key finding 1 with context",
    "Key finding 2 with context",
    "Key finding 3 with context"
  ],
  
  "action_items": [
    {{
      "priority": 1,
      "title": "Immediate action (do now)",
      "description": "Specific, actionable step with timing",
      "estimated_time": "X minutes",
      "impact": "Expected benefit"
    }},
    {{
      "priority": 2,
      "title": "Today's action",
      "description": "Specific, actionable step",
      "estimated_time": "X minutes",
      "impact": "Expected benefit"
    }},
    {{
      "priority": 3,
      "title": "This week's habit",
      "description": "Sustainable practice to build",
      "estimated_time": "X minutes daily",
      "impact": "Long-term benefit"
    }}
  ],
  
  "hypnosis_script": "A 200-300 word calming script for sleep or relaxation. Use present tense, second person ('you'). Include imagery, breathing cues, and progressive relaxation. Make it soothing and non-medical.",
  
  "breathing_exercise": {{
    "name": "Specific breathing technique name",
    "pattern": "Inhale X, Hold Y, Exhale Z pattern",
    "duration": "X minutes",
    "instruction": "Step-by-step guidance"
  }},
  
  "wellness_score_interpretation": "Brief explanation of what their overall wellness indicators suggest and one encouraging insight."
}}

IMPORTANT CONSTRAINTS:
- NO medical advice or diagnoses
- Use accessible language (8th grade reading level)
- Be specific with numbers and timing
- If data is limited or simulated, acknowledge it gracefully
- Always include at least one thing the user is doing well
- Make the narrative feel personal and observed, not generic

Return ONLY the JSON object, nothing else."""

    return prompt

def parse_gemini_response(response_text: str) -> Dict[str, Any]:
    """
    Parse and validate Gemini's JSON response
    """
    try:
        # Try to extract JSON if wrapped in markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()
        
        # Parse JSON
        data = json.loads(response_text)
        
        # Validate required fields
        required_fields = ["narrative", "observations", "action_items"]
        for field in required_fields:
            if field not in data:
                print(f"Warning: Missing required field '{field}' in Gemini response")
        
        return data
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse Gemini response as JSON: {e}")
        # Return fallback structure
        return {
            "narrative": response_text[:500] if response_text else "Unable to generate narrative.",
            "observations": ["Data analysis completed"],
            "action_items": [
                {
                    "priority": 1,
                    "title": "Take a moment to breathe",
                    "description": "Try 4-4-6 breathing for 2 minutes",
                    "estimated_time": "2 minutes",
                    "impact": "Immediate calm and stress reduction"
                }
            ],
            "hypnosis_script": "Close your eyes and breathe deeply. You are safe and supported.",
            "wellness_score_interpretation": "Your wellness data has been analyzed."
        }

def build_simple_wellness_narrative(
    audio_feats: Dict[str, Any],
    wearable_summary: Dict[str, Any],
    pose_summary: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Fallback: Generate simple wellness narrative without Gemini API
    Useful for testing and when API is unavailable
    """
    
    stress_score = audio_feats.get('stress_score', 0.5)
    emotional_tone = audio_feats.get('emotional_tone', 'neutral')
    hrv = wearable_summary.get('hrv_rmssd', 45)
    sleep_hours = wearable_summary.get('total_sleep_hours', 7)
    posture_status = pose_summary.get('posture_status', 'not assessed')
    
    # Build narrative based on data
    narrative_parts = []
    
    # Stress assessment
    if stress_score > 0.65:
        narrative_parts.append("Your voice analysis suggests you're experiencing some tension right now. This is completely normal, and your body is communicating that it might need some support.")
    elif stress_score < 0.35:
        narrative_parts.append("Your voice sounds calm and relaxed, which is wonderful. Your body seems to be in a good place right now.")
    else:
        narrative_parts.append("Your voice shows a balanced emotional state - neither overly stressed nor completely relaxed.")
    
    # HRV assessment
    if hrv < 30:
        narrative_parts.append("Your heart rate variability is on the lower side, which can happen when you're stressed or tired. This is your body asking for some recovery time.")
    elif hrv > 50:
        narrative_parts.append("Your heart rate variability is excellent, indicating strong parasympathetic activity and good recovery capacity.")
    
    # Sleep assessment
    if sleep_hours < 7:
        narrative_parts.append(f"You got {sleep_hours} hours of sleep, which is below the recommended 7-9 hours. Even small amounts of sleep debt can impact how you feel.")
    
    narrative = " ".join(narrative_parts)
    
    return {
        "narrative": narrative,
        "observations": [
            f"Voice stress level: {stress_score:.2f} ({emotional_tone})",
            f"HRV (RMSSD): {hrv} ms - {('low', 'moderate', 'good', 'excellent')[min(3, int(hrv/20))]} recovery status",
            f"Sleep: {sleep_hours} hours - {('insufficient', 'borderline', 'adequate', 'optimal')[min(3, int(sleep_hours/2))]}"
        ],
        "action_items": [
            {
                "priority": 1,
                "title": "3-minute breathing reset",
                "description": "Practice 4-4-6 breathing: inhale for 4 counts, hold for 4, exhale for 6. This activates your parasympathetic nervous system.",
                "estimated_time": "3 minutes",
                "impact": "Immediate stress reduction and HRV improvement"
            },
            {
                "priority": 2,
                "title": "Posture check and stretch",
                "description": "Stand up, roll your shoulders back, and do 3 gentle neck rolls each direction.",
                "estimated_time": "2 minutes",
                "impact": "Release physical tension and improve circulation"
            },
            {
                "priority": 3,
                "title": "Sleep consistency goal",
                "description": "Aim for bed at the same time tonight, targeting 7.5-8 hours of sleep.",
                "estimated_time": "Full night",
                "impact": "Better recovery and improved HRV tomorrow"
            }
        ],
        "hypnosis_script": """Take a deep breath in, and slowly release. Feel your body settling into this moment.
        
        With each breath, you're letting go of the day. Your shoulders soften. Your jaw unclenches. 
        
        Imagine a warm, gentle wave starting at the crown of your head, slowly washing down through your body. This wave brings deep relaxation wherever it flows. Down your neck, across your shoulders, down your spine.
        
        Your heartbeat is steady and calm. Your breath is your anchor. You are safe here, in this moment.
        
        As you continue breathing slowly and deeply, notice how your body naturally knows how to relax. You don't have to force anything. Just allow. Just breathe.
        
        With each exhale, you're releasing a little more tension. With each inhale, you're inviting a little more peace.
        
        Continue this rhythm as you drift toward rest. Your body is healing. Your mind is quieting. You are exactly where you need to be.""",
        "breathing_exercise": {
            "name": "4-4-6 Calming Breath",
            "pattern": "Inhale 4, Hold 4, Exhale 6",
            "duration": "3 minutes",
            "instruction": "Breathe in through your nose for 4 counts, hold comfortably for 4 counts, then exhale slowly through your mouth for 6 counts. The extended exhale activates your relaxation response."
        },
        "wellness_score_interpretation": "Your body is communicating its needs clearly. The combination of voice, heart, and posture data gives us a complete picture of your current state. Focus on the immediate actions above for the biggest impact."
    }

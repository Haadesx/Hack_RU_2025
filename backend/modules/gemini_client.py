# modules/gemini_client.py
import os
import json
import requests
from typing import Dict, Any
import time

# For demo purposes, we'll use a mock Gemini response
# In production, replace with actual Gemini API calls

def call_gemini(prompt: str) -> Dict[str, Any]:
    """
    Call Gemini API with the wellness analysis prompt
    For demo purposes, returns a mock response
    """
    try:
        # Mock API key check
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("GEMINI_API_KEY not found, using mock response")
            return get_mock_gemini_response(prompt)
        
        # TODO: Implement actual Gemini API call here
        # For now, return mock response
        return get_mock_gemini_response(prompt)
        
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return get_fallback_response()

def get_mock_gemini_response(prompt: str) -> Dict[str, Any]:
    """Generate a realistic mock response for demo purposes"""
    
    # Extract stress level from prompt for personalization
    stress_level = 0.5
    if "Stress Level:" in prompt:
        try:
            stress_line = [line for line in prompt.split('\n') if 'Stress Level:' in line][0]
            stress_level = float(stress_line.split(':')[1].split('(')[0].strip())
        except:
            pass
    
    # Generate personalized response based on stress level
    if stress_level > 0.7:
        narrative = """I can sense that you're carrying quite a bit of stress right now, and I want you to know that it's completely understandable. Your voice shows signs of tension, and your body is working hard to manage everything on your plate. This is your body's way of protecting you, and recognizing this is the first step toward finding relief.

The good news is that stress is temporary, and you have more control over your response to it than you might realize. Your body is resilient and capable of returning to a state of calm. Small, consistent actions can make a significant difference in how you feel.

Remember, taking care of yourself isn't selfish—it's essential. When you're well-rested and centered, you're better able to handle life's challenges and be present for the people and activities that matter most to you."""
        
        observations = [
            "Your voice shows elevated stress markers, indicating your nervous system is in high alert",
            "Your speaking rate is faster than usual, suggesting mental overwhelm",
            "Your energy levels are high but potentially unsustainable",
            "Your body is showing signs of tension that could benefit from relaxation"
        ]
        
        action_items = [
            "Take 5 minutes right now for the 4-7-8 breathing exercise I'll guide you through",
            "Schedule a 10-minute walk outside within the next hour to reset your nervous system",
            "Set a phone reminder for 3 PM today to pause and check in with your body"
        ]
        
    elif stress_level > 0.4:
        narrative = """You're in a state of moderate alertness, which is actually quite normal for this time of day. Your voice shows some tension, but also resilience. This suggests you're managing your responsibilities while staying aware of your needs—that's a healthy balance.

Your body is giving you signals that it's time to pause and recharge. This isn't a sign of weakness, but rather wisdom. Your nervous system is designed to cycle between activity and rest, and honoring this natural rhythm will help you maintain your energy throughout the day.

You're doing better than you might think. The fact that you're taking time to check in with yourself shows self-awareness and care. These small moments of mindfulness are building blocks for long-term wellbeing."""
        
        observations = [
            "Your voice shows moderate stress levels with good recovery potential",
            "Your energy is balanced but could benefit from some gentle restoration",
            "Your speaking patterns suggest you're managing multiple priorities well",
            "Your body is ready for some gentle relaxation techniques"
        ]
        
        action_items = [
            "Practice the 3-minute box breathing exercise I'll guide you through now",
            "Take a 5-minute break to stretch or do gentle neck rolls within the next 30 minutes",
            "Set an intention to have one screen-free moment before your next meal"
        ]
        
    else:
        narrative = """You sound remarkably calm and centered right now. Your voice shows a beautiful balance of energy and relaxation, which suggests you're in a good place with your stress management. This is something to celebrate and build upon.

Your calm state is a testament to your self-care practices and emotional regulation skills. When you're in this balanced state, you're better able to make clear decisions, connect with others, and enjoy the present moment.

This is an ideal time to reinforce the practices that got you here. Your body and mind are aligned, and you're operating from a place of strength and clarity. Trust this feeling and remember it for times when you need to return to this centered state."""
        
        observations = [
            "Your voice shows excellent stress management and emotional regulation",
            "Your energy levels are balanced and sustainable",
            "Your speaking patterns indicate mental clarity and focus",
            "Your body appears relaxed and well-regulated"
        ]
        
        action_items = [
            "Enjoy this 2-minute energizing breathing exercise to maintain your great state",
            "Take a moment to appreciate and acknowledge your current sense of wellbeing",
            "Consider sharing your calm energy with someone else through a kind gesture today"
        ]
    
    breathing_script = """Let's begin your breathing exercise. Find a comfortable seated position or lie down if you prefer. Close your eyes gently and let your body settle into this moment.

Take a deep breath in through your nose for a count of four... hold it gently for a count of four... and now exhale slowly through your mouth for a count of eight. Feel your shoulders drop and your jaw relax as you release this breath.

Again, breathe in for four... hold for four... and exhale for eight. With each exhale, imagine releasing any tension you're carrying. Let it flow out of your body like a gentle stream.

Continue this rhythm at your own pace. In for four... hold for four... out for eight. You're doing beautifully. With each breath, you're creating space for calm and peace within yourself.

As you continue breathing, notice how your body feels lighter and more relaxed. Your mind is becoming clearer, and your heart rate is naturally slowing down. You're safe, you're supported, and you're exactly where you need to be.

Take one more deep breath... and when you're ready, gently open your eyes. Notice how you feel now compared to when we started. Carry this sense of calm with you as you continue your day."""
    
    sleep_hypnosis_script = """Welcome to your peaceful sleep preparation. Find a comfortable position and let your body relax completely. Close your eyes gently and take three deep breaths with me.

As you breathe, imagine yourself walking through a beautiful, quiet forest at twilight. The trees are tall and protective, and the path is soft beneath your feet. You can hear the gentle sounds of nature around you—the whisper of leaves, the distant call of an owl.

With each step, you feel yourself becoming more relaxed. Your muscles are releasing tension, and your mind is becoming calm and peaceful. You're walking toward a beautiful clearing where you can rest safely.

In this clearing, you find a soft bed of moss and leaves. You lie down, feeling completely supported by the earth beneath you. The stars begin to appear above you, twinkling gently in the night sky.

As you rest here, you feel your body becoming heavier and more relaxed. Your breathing slows naturally, and your thoughts become gentle and peaceful. You are drifting into a deep, restful sleep.

Sleep well, and wake refreshed."""
    
    return {
        "narrative": narrative,
        "observations": observations,
        "action_items": action_items,
        "breathing_script": breathing_script,
        "sleep_hypnosis_script": sleep_hypnosis_script
    }

def get_fallback_response() -> Dict[str, Any]:
    """Fallback response if Gemini API fails"""
    return {
        "narrative": "I'm here to support you on your wellness journey. While I'm experiencing some technical difficulties, I want you to know that taking time to check in with yourself is already a positive step. Your wellbeing matters, and small actions can make a big difference.",
        "observations": [
            "You're taking proactive steps toward better wellness",
            "Self-awareness is a key component of health",
            "Regular check-ins help maintain balance"
        ],
        "action_items": [
            "Take 5 deep breaths right now",
            "Drink a glass of water",
            "Take a 5-minute break to stretch"
        ],
        "breathing_script": "Take a deep breath in... and slowly let it out. Repeat this simple breathing pattern for a few minutes, focusing on the rhythm of your breath.",
        "sleep_hypnosis_script": "Imagine yourself in a peaceful place. Feel your body relaxing with each breath. You are safe, comfortable, and ready for restful sleep."
    }

# TODO: Implement actual Gemini API integration
def call_gemini_api_actual(prompt: str, api_key: str) -> Dict[str, Any]:
    """
    Actual Gemini API implementation (to be completed)
    """
    # This would contain the real Gemini API call
    # For now, return mock response
    pass
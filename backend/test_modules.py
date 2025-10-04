#!/usr/bin/env python3
"""
Quick test script to verify all backend modules are working
Run: python test_modules.py
"""

import sys
from pathlib import Path

print("🧪 Testing BioWhisper Backend Modules\n")
print("=" * 50)

# Test 1: Audio Analysis
print("\n1️⃣  Testing Audio Analysis Module...")
try:
    from modules.audio_analysis import analyze_audio
    print("   ✅ Audio analysis module imported successfully")
    
    # Test with dummy data would require an actual audio file
    print("   ℹ️  To test fully, provide an audio file path")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: HRV Analysis
print("\n2️⃣  Testing HRV Analysis Module...")
try:
    from modules.hrv_analysis import analyze_hrv_csv, generate_sample_wearable_csv
    print("   ✅ HRV analysis module imported successfully")
    
    # Generate sample data
    sample_file = "test_sample_data.csv"
    generate_sample_wearable_csv(sample_file)
    print(f"   ✅ Generated sample wearable data: {sample_file}")
    
    # Test analysis
    result = analyze_hrv_csv(sample_file)
    print(f"   ✅ HRV Analysis completed: {result.get('hrv_rmssd', 0):.1f} ms RMSSD")
    
    # Cleanup
    Path(sample_file).unlink(missing_ok=True)
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Pose Analysis
print("\n3️⃣  Testing Pose Analysis Module...")
try:
    from modules.pose_analysis import analyze_pose_keypoints, simulate_pose_analysis
    print("   ✅ Pose analysis module imported successfully")
    
    # Test with simulated data
    result = simulate_pose_analysis()
    print(f"   ✅ Simulated pose analysis: {result.get('posture_status', 'unknown')}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 4: Prompt Builder
print("\n4️⃣  Testing Prompt Builder Module...")
try:
    from modules.prompt_builder import build_gemini_prompt, build_simple_wellness_narrative
    print("   ✅ Prompt builder module imported successfully")
    
    # Test prompt building
    test_audio_feats = {"stress_score": 0.6, "emotional_tone": "neutral", "energy": 0.04}
    test_wearable = {"hrv_rmssd": 45, "avg_hr": 72, "total_sleep_hours": 7}
    test_pose = {"posture_status": "good", "alignment_score": 0.8}
    
    prompt = build_gemini_prompt(test_audio_feats, test_wearable, test_pose)
    print(f"   ✅ Generated prompt ({len(prompt)} chars)")
    
    # Test fallback narrative
    narrative = build_simple_wellness_narrative(test_audio_feats, test_wearable, test_pose)
    print(f"   ✅ Generated fallback narrative")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 5: Gemini Client
print("\n5️⃣  Testing Gemini Client Module...")
try:
    from modules.gemini_client import call_gemini
    print("   ✅ Gemini client module imported successfully")
    print("   ℹ️  Note: Actual API calls require GEMINI_API_KEY in .env")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 6: TTS Module
print("\n6️⃣  Testing TTS Module...")
try:
    from modules.tts import elevenlabs_tts, generate_breathing_exercise_audio
    print("   ✅ TTS module imported successfully")
    print("   ℹ️  Note: Actual TTS requires ELEVENLABS_API_KEY in .env")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 7: Environment Variables
print("\n7️⃣  Checking Environment Configuration...")
try:
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    eleven_key = os.getenv("ELEVENLABS_API_KEY", "")
    
    if gemini_key and gemini_key != "":
        print("   ✅ GEMINI_API_KEY configured")
    else:
        print("   ⚠️  GEMINI_API_KEY not configured (using fallback)")
    
    if eleven_key and eleven_key != "":
        print("   ✅ ELEVENLABS_API_KEY configured")
    else:
        print("   ⚠️  ELEVENLABS_API_KEY not configured (using fallback)")
    
except Exception as e:
    print(f"   ℹ️  python-dotenv not installed or .env not found")

# Test 8: FastAPI App
print("\n8️⃣  Testing FastAPI App...")
try:
    from app import app
    print("   ✅ FastAPI app imported successfully")
    print("   ℹ️  To run: python app.py or uvicorn app:app --reload")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("✅ All module tests passed!")
print("\n🚀 Ready to start backend:")
print("   python app.py")
print("\n📚 API docs will be available at:")
print("   http://localhost:8000/docs")
print("\n" + "=" * 50)

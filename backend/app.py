# app.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import shutil
import json
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

from modules.audio_analysis import analyze_audio
from modules.pose_analysis import analyze_pose_from_keypoints
from modules.hrv_analysis import analyze_hrv_data
from modules.prompt_builder import build_gemini_prompt
from modules.gemini_client import call_gemini
from modules.tts import elevenlabs_tts

load_dotenv()

app = FastAPI(title="BioWhisper API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Serve static files (for TTS audio output)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/")
async def root():
    return {"message": "BioWhisper API is running", "timestamp": datetime.now().isoformat()}

@app.post("/record")
async def upload_record(file: UploadFile = File(...)):
    """Upload and analyze 10-second audio recording"""
    try:
        # Save uploaded file
        dest = UPLOAD_DIR / f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Analyze audio
        features = analyze_audio(str(dest))
        
        return {
            "ok": True, 
            "filename": dest.name,
            "features": features,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {str(e)}")

@app.post("/wearable/upload")
async def upload_wearable(file: UploadFile = File(...)):
    """Upload wearable data CSV"""
    try:
        dest = UPLOAD_DIR / f"wearable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Analyze HRV data
        hrv_summary = analyze_hrv_data(str(dest))
        
        return {
            "ok": True,
            "filename": dest.name,
            "hrv_summary": hrv_summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wearable analysis failed: {str(e)}")

@app.post("/camera-scan")
async def camera_scan(pose_keypoints: dict):
    """Analyze pose keypoints from camera scan"""
    try:
        pose_summary = analyze_pose_from_keypoints(pose_keypoints)
        return {
            "ok": True,
            "pose_summary": pose_summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pose analysis failed: {str(e)}")

@app.post("/analyze")
async def analyze_all(
    audio_filename: str = Form(...),
    wearable_filename: str = Form(None),
    pose_keypoints: str = Form(None)
):
    """Comprehensive wellness analysis combining all data sources"""
    try:
        # 1) Audio analysis
        audio_path = UPLOAD_DIR / audio_filename
        if not audio_path.exists():
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        audio_feats = analyze_audio(str(audio_path))
        
        # 2) Wearable/HRV analysis (if provided)
        wearable_summary = {}
        if wearable_filename:
            wearable_path = UPLOAD_DIR / wearable_filename
            if wearable_path.exists():
                wearable_summary = analyze_hrv_data(str(wearable_path))
        
        # 3) Pose analysis (if provided)
        pose_summary = {}
        if pose_keypoints:
            pose_data = json.loads(pose_keypoints)
            pose_summary = analyze_pose_from_keypoints(pose_data)
        
        # 4) Build prompt and call Gemini
        prompt = build_gemini_prompt(
            audio_feats=audio_feats,
            wearable_summary=wearable_summary,
            pose_summary=pose_summary
        )
        
        gemini_resp = await call_gemini(prompt)
        
        # 5) Generate TTS audio
        narrative_text = gemini_resp.get("narrative", "I couldn't generate a narrative.")
        breathing_text = gemini_resp.get("breathing_script", "Take a deep breath and relax.")
        
        # Generate narration TTS
        narration_audio_path = elevenlabs_tts(
            narrative_text, 
            voice="alloy",
            output_name=f"narration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        # Generate breathing exercise TTS
        breathing_audio_path = elevenlabs_tts(
            breathing_text,
            voice="alloy", 
            output_name=f"breathing_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        return {
            "ok": True,
            "analysis": {
                "audio_features": audio_feats,
                "wearable_summary": wearable_summary,
                "pose_summary": pose_summary
            },
            "insights": gemini_resp,
            "audio_urls": {
                "narration": f"/static/{Path(narration_audio_path).name}" if narration_audio_path else None,
                "breathing": f"/static/{Path(breathing_audio_path).name}" if breathing_audio_path else None
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/generate-sleep-hypnosis")
async def generate_sleep_hypnosis(
    duration_minutes: int = Form(5),
    user_preferences: str = Form("")
):
    """Generate personalized sleep hypnosis audio"""
    try:
        # Create sleep hypnosis script
        hypnosis_script = f"""
        Welcome to your personalized sleep hypnosis session. 
        Find a comfortable position and let your body relax completely.
        Take three deep breaths with me now. In... and out. In... and out. In... and out.
        
        As you breathe, imagine yourself in a peaceful forest. The trees sway gently in the breeze.
        You can hear the soft sounds of nature around you. Feel the warmth of the sun filtering through the leaves.
        
        With each breath, you feel yourself becoming more relaxed. Your muscles are releasing tension.
        Your mind is becoming calm and peaceful. You are safe, you are comfortable, you are at peace.
        
        Now, imagine walking deeper into this peaceful forest. You come to a beautiful clearing with soft grass.
        You lie down in this clearing, feeling completely supported by the earth beneath you.
        
        As you rest here, you feel your body becoming heavier and more relaxed. Your breathing slows naturally.
        Your thoughts become gentle and peaceful. You are drifting into a deep, restful sleep.
        
        Sleep well, and wake refreshed.
        """
        
        # Generate TTS audio
        hypnosis_audio_path = elevenlabs_tts(
            hypnosis_script,
            voice="alloy",
            output_name=f"hypnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        return {
            "ok": True,
            "script": hypnosis_script,
            "audio_url": f"/static/{Path(hypnosis_audio_path).name}" if hypnosis_audio_path else None,
            "duration_minutes": duration_minutes,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hypnosis generation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
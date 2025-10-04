# app.py - FastAPI Backend for BioWhisper
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import shutil
import json
from pathlib import Path
from typing import Optional
from modules.audio_analysis import analyze_audio
from modules.prompt_builder import build_gemini_prompt
from modules.gemini_client import call_gemini
from modules.tts import elevenlabs_tts
from modules.hrv_analysis import analyze_hrv_csv
from modules.pose_analysis import analyze_pose_keypoints

app = FastAPI(title="BioWhisper API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory setup
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {"message": "BioWhisper API - Wellness Analysis Pipeline", "version": "1.0.0"}

@app.post("/record")
async def upload_record(file: UploadFile = File(...)):
    """
    Upload and analyze audio recording (10s voice check-in)
    """
    try:
        # Save uploaded file
        dest = UPLOAD_DIR / file.filename
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Analyze audio features
        features = analyze_audio(str(dest))
        
        return {
            "ok": True,
            "filename": file.filename,
            "features": features,
            "message": "Audio uploaded and analyzed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {str(e)}")

@app.post("/wearable/upload")
async def upload_wearable(file: UploadFile = File(...)):
    """
    Upload wearable data CSV (HR, HRV, sleep stages)
    """
    try:
        dest = UPLOAD_DIR / file.filename
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Analyze HRV and sleep data
        hrv_summary = analyze_hrv_csv(str(dest))
        
        return {
            "ok": True,
            "filename": file.filename,
            "hrv_summary": hrv_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wearable data analysis failed: {str(e)}")

@app.post("/camera-scan")
async def camera_scan(keypoints_json: str = Form(...)):
    """
    Analyze pose keypoints from webcam (MediaPipe or TensorFlow.js)
    """
    try:
        keypoints = json.loads(keypoints_json)
        pose_summary = analyze_pose_keypoints(keypoints)
        
        return {
            "ok": True,
            "pose_summary": pose_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pose analysis failed: {str(e)}")

@app.post("/analyze")
async def analyze_all(
    audio_filename: str = Form(...),
    wearable_filename: Optional[str] = Form(None),
    pose_keypoints_json: Optional[str] = Form(None)
):
    """
    Orchestrate full analysis: audio + wearable + pose → Gemini → TTS
    """
    try:
        # 1) Audio analysis
        audio_path = UPLOAD_DIR / audio_filename
        if not audio_path.exists():
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        audio_feats = analyze_audio(str(audio_path))
        
        # 2) Wearable / HRV analysis (simulate if not provided)
        wearable_summary = {}
        if wearable_filename:
            wearable_path = UPLOAD_DIR / wearable_filename
            if wearable_path.exists():
                wearable_summary = analyze_hrv_csv(str(wearable_path))
        else:
            # Simulate baseline data
            wearable_summary = {
                "hrv_rmssd": 45.0,
                "avg_hr": 72,
                "sleep_debt_hours": 1.5,
                "sleep_midpoint": "03:30",
                "note": "Simulated data - no wearable connected"
            }
        
        # 3) Pose analysis
        pose_summary = {}
        if pose_keypoints_json:
            keypoints = json.loads(pose_keypoints_json)
            pose_summary = analyze_pose_keypoints(keypoints)
        
        # 4) Build prompt and call Gemini
        prompt = build_gemini_prompt(
            audio_feats=audio_feats,
            wearable_summary=wearable_summary,
            pose_summary=pose_summary
        )
        
        gemini_resp = await call_gemini(prompt)
        
        # 5) Generate TTS audio for narrative
        narrative_text = gemini_resp.get("narrative", "I couldn't generate a narrative.")
        tts_filename = f"tts_narrative_{audio_filename.split('.')[0]}.mp3"
        tts_path = elevenlabs_tts(narrative_text, output_filename=tts_filename)
        
        # 6) Generate breathing exercise audio
        breathing_script = "Let's begin a calming breathing exercise. Breathe in slowly for 4 counts. Hold for 4. Breathe out for 6. And hold for 2. Let's repeat. Breathe in, 2, 3, 4. Hold, 2, 3, 4. Breathe out, 2, 3, 4, 5, 6. Hold. Again, breathe in slowly. And hold. Release. And rest."
        breathing_filename = f"breathing_{audio_filename.split('.')[0]}.mp3"
        breathing_path = elevenlabs_tts(breathing_script, output_filename=breathing_filename)
        
        return {
            "ok": True,
            "narrative": narrative_text,
            "observations": gemini_resp.get("observations", []),
            "action_items": gemini_resp.get("action_items", []),
            "hypnosis_script": gemini_resp.get("hypnosis_script", ""),
            "tts_filename": tts_filename if tts_path else None,
            "breathing_filename": breathing_filename if breathing_path else None,
            "audio_features": audio_feats,
            "wearable_summary": wearable_summary,
            "pose_summary": pose_summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline failed: {str(e)}")

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """
    Serve generated audio files
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(file_path, media_type="audio/mpeg")

@app.post("/generate-hypnosis")
async def generate_hypnosis(duration_minutes: int = Form(5)):
    """
    Generate personalized sleep hypnosis audio
    """
    try:
        # Build a longer sleep hypnosis script
        hypnosis_script = f"""
        Welcome to your personalized sleep journey. Find a comfortable position and close your eyes.
        Take a deep breath in, and slowly release. Feel your body settling into relaxation.
        
        With each breath, you're becoming more and more relaxed. Your shoulders soften.
        Your jaw unclenches. Every muscle in your body is releasing tension.
        
        Imagine a warm, gentle light starting at the top of your head, slowly moving down.
        This light brings deep relaxation wherever it goes. Down your neck, your shoulders, your arms.
        
        You are safe. You are calm. You are ready for restorative sleep.
        Let go of the day. Let go of tomorrow. This moment is yours.
        
        Continue breathing slowly and deeply as you drift into peaceful, healing sleep.
        """
        
        output_filename = f"hypnosis_{duration_minutes}min.mp3"
        tts_path = elevenlabs_tts(hypnosis_script, output_filename=output_filename)
        
        return {
            "ok": True,
            "filename": output_filename if tts_path else None,
            "duration_minutes": duration_minutes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hypnosis generation failed: {str(e)}")

if __name__ == "__main__":
    print("🎯 Starting BioWhisper API server...")
    print("📍 API docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

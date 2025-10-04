# app.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import shutil
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from modules.audio_analysis import analyze_audio
from modules.pose_analysis import analyze_pose_keypoints
from modules.hrv_analysis import analyze_hrv_data
from modules.prompt_builder import build_gemini_prompt
from modules.gemini_client import call_gemini
from modules.tts import elevenlabs_tts

app = FastAPI(title="BioWhisper API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directories
UPLOAD_DIR = Path("uploads")
AUDIO_DIR = UPLOAD_DIR / "audio"
TTS_DIR = UPLOAD_DIR / "tts"
WEARABLE_DIR = UPLOAD_DIR / "wearable"

for dir_path in [UPLOAD_DIR, AUDIO_DIR, TTS_DIR, WEARABLE_DIR]:
    dir_path.mkdir(exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/")
async def root():
    return {"message": "BioWhisper API - Your compassionate wellness assistant"}

@app.post("/record")
async def upload_audio(file: UploadFile = File(...)):
    """Upload and analyze audio recording"""
    try:
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}_{file.filename}"
        file_path = AUDIO_DIR / filename
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Analyze audio
        features = analyze_audio(str(file_path))
        
        return {
            "ok": True,
            "filename": filename,
            "features": features,
            "message": "Audio recorded and analyzed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.post("/wearable/upload")
async def upload_wearable_data(file: UploadFile = File(...)):
    """Upload wearable/HRV CSV data"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wearable_{timestamp}_{file.filename}"
        file_path = WEARABLE_DIR / filename
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Analyze HRV data
        hrv_summary = analyze_hrv_data(str(file_path))
        
        return {
            "ok": True,
            "filename": filename,
            "summary": hrv_summary,
            "message": "Wearable data analyzed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing wearable data: {str(e)}")

@app.post("/camera-scan")
async def analyze_posture(pose_keypoints: Dict[str, Any]):
    """Analyze posture from camera pose keypoints"""
    try:
        pose_summary = analyze_pose_keypoints(pose_keypoints)
        return {
            "ok": True,
            "summary": pose_summary,
            "message": "Posture analyzed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing posture: {str(e)}")

@app.post("/analyze")
async def comprehensive_analysis(
    audio_filename: str = Form(...),
    wearable_filename: Optional[str] = Form(None),
    pose_data: Optional[str] = Form(None)
):
    """Comprehensive wellness analysis with Gemini and TTS generation"""
    try:
        # 1. Get audio analysis
        audio_path = AUDIO_DIR / audio_filename
        if not audio_path.exists():
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        audio_features = analyze_audio(str(audio_path))
        
        # 2. Get wearable analysis (if provided)
        wearable_summary = {}
        if wearable_filename:
            wearable_path = WEARABLE_DIR / wearable_filename
            if wearable_path.exists():
                wearable_summary = analyze_hrv_data(str(wearable_path))
        
        # 3. Get pose analysis (if provided)
        pose_summary = {}
        if pose_data:
            pose_keypoints = json.loads(pose_data)
            pose_summary = analyze_pose_keypoints(pose_keypoints)
        
        # 4. Build prompt and call Gemini
        prompt = build_gemini_prompt(
            audio_feats=audio_features,
            wearable_summary=wearable_summary,
            pose_summary=pose_summary
        )
        
        gemini_response = await call_gemini(prompt)
        
        # 5. Generate TTS audio
        narrative_text = gemini_response.get("narrative", "I'm here to support your wellness journey.")
        breathing_script = "Let's take a moment together. Breathe in slowly for four counts... hold... and breathe out for six counts. Feel your body relax with each exhale."
        
        # Generate narrative TTS
        tts_narrative_path = elevenlabs_tts(narrative_text, "narrative")
        
        # Generate breathing exercise TTS
        tts_breathing_path = elevenlabs_tts(breathing_script, "breathing")
        
        # Generate sleep hypnosis if requested
        hypnosis_script = gemini_response.get("hypnosis_script", "")
        tts_hypnosis_path = None
        if hypnosis_script:
            tts_hypnosis_path = elevenlabs_tts(hypnosis_script, "hypnosis")
        
        return {
            "narrative": gemini_response.get("narrative"),
            "observations": gemini_response.get("observations"),
            "action_items": gemini_response.get("action_items", []),
            "audio": {
                "narrative_url": f"/static/tts/{Path(tts_narrative_path).name}" if tts_narrative_path else None,
                "breathing_url": f"/static/tts/{Path(tts_breathing_path).name}" if tts_breathing_path else None,
                "hypnosis_url": f"/static/tts/{Path(tts_hypnosis_path).name}" if tts_hypnosis_path else None,
            },
            "analysis_data": {
                "audio_features": audio_features,
                "wearable_summary": wearable_summary,
                "pose_summary": pose_summary
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in comprehensive analysis: {str(e)}")

@app.post("/generate-sleep-hypnosis")
async def generate_sleep_hypnosis(
    duration_minutes: int = Form(10),
    focus_area: str = Form("general relaxation")
):
    """Generate personalized sleep hypnosis audio"""
    try:
        # Create a longer, more detailed sleep script
        sleep_prompt = f"""Create a {duration_minutes}-minute sleep hypnosis script focused on {focus_area}. 
        Use calm, soothing language with progressive relaxation techniques. Include breathing guidance and 
        positive affirmations. The script should help the listener fall into deep, restorative sleep."""
        
        # This would call Gemini to generate the script
        hypnosis_script = f"""Close your eyes and let your body sink into comfort. With each breath, 
        feel yourself becoming more relaxed. Starting from your toes, notice how they begin to relax completely. 
        This wave of relaxation moves up through your legs, your hips, your back... 
        Each muscle group releasing tension as this peaceful feeling flows through your entire body. 
        Your breathing becomes slow and natural. You are safe, you are peaceful, and you are ready for deep, 
        healing sleep that will restore your mind and body."""
        
        # Generate TTS
        tts_path = elevenlabs_tts(hypnosis_script, "long_hypnosis")
        
        return {
            "ok": True,
            "script": hypnosis_script,
            "audio_url": f"/static/tts/{Path(tts_path).name}" if tts_path else None,
            "duration_minutes": duration_minutes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sleep hypnosis: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
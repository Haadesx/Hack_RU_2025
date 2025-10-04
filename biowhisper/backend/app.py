from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

from modules.audio_analysis import analyze_audio
from modules.prompt_builder import build_gemini_prompt
from modules.gemini_client import call_gemini
from modules.tts import elevenlabs_tts

app = FastAPI(title="BioWhisper API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"ok": True, "service": "biowhisper", "version": "0.1.0"}


@app.post("/record")
async def upload_record(file: UploadFile = File(...)) -> Dict[str, Any]:
    dest = UPLOAD_DIR / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    features = analyze_audio(str(dest))
    return {"ok": True, "features": features, "filename": file.filename}


@app.post("/analyze")
async def analyze_all(
    audio_filename: str = Form(...),
    wearable_csv: Optional[UploadFile] = None,
    pose_keypoints_json: Optional[str] = None,
) -> Dict[str, Any]:
    audio_path = UPLOAD_DIR / audio_filename
    audio_feats = analyze_audio(str(audio_path))

    wearable_summary: Dict[str, Any] = {}
    pose_summary: Dict[str, Any] = {}

    prompt = build_gemini_prompt(
        audio_feats=audio_feats,
        wearable_summary=wearable_summary,
        pose_summary=pose_summary,
    )

    gemini_resp = await call_gemini(prompt)
    narration_text = gemini_resp.get("narrative", "I couldn't generate a narrative.")

    tts_path = elevenlabs_tts(narration_text, voice="alloy")

    return {
        "narrative": narration_text,
        "analysis": {"audio": audio_feats, "wearable": wearable_summary, "pose": pose_summary},
        "tts_path": tts_path,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

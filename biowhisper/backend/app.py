from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import shutil
import json
from pathlib import Path

from modules.audio_analysis import analyze_audio
from modules.prompt_builder import build_gemini_prompt
from modules.gemini_client import call_gemini
from modules.tts import elevenlabs_tts

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="BioWhisper Backend", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], expose_headers=["*"], allow_credentials=False)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR), html=False), name="uploads")


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/record")
async def upload_record(file: UploadFile = File(...)):
    filename = file.filename or "checkin.wav"
    dest = UPLOAD_DIR / filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    features = analyze_audio(str(dest))
    return {"ok": True, "filename": filename, "features": features, "file_url": f"/uploads/{filename}"}


@app.post("/analyze")
async def analyze_all(
    audio_filename: str = Form(...),
    wearable_csv: UploadFile | None = File(None),
    pose_keypoints_json: str | None = Form(None),
):
    audio_path = UPLOAD_DIR / audio_filename
    audio_feats = analyze_audio(str(audio_path))

    wearable_summary = {}
    if wearable_csv is not None:
        wearable_summary["note"] = "Wearable parsing not implemented in MVP"

    pose_summary = {}
    if pose_keypoints_json:
        try:
            pose_summary = json.loads(pose_keypoints_json)
        except Exception:
            pose_summary["note"] = "Invalid pose JSON"

    prompt = build_gemini_prompt(audio_feats=audio_feats, wearable_summary=wearable_summary, pose_summary=pose_summary)
    gemini_resp = await call_gemini(prompt)

    narration_text = gemini_resp.get("narrative", "Narrative unavailable.")
    tts_url = elevenlabs_tts(narration_text, voice="alloy")

    return {
        "ok": True,
        "audio_features": audio_feats,
        "wearable_summary": wearable_summary,
        "pose_summary": pose_summary,
        "narrative": narration_text,
        "tts_url": tts_url,
        "gemini": gemini_resp,
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

# BioWhisper (Hackathon MVP)

A 24-hour build: record a 10s voice check‑in, run lightweight analysis, generate a compassionate narrative, and play a short TTS audio.

## Stack
- Backend: FastAPI (Python), simple audio analysis via librosa
- Frontend: React + Vite + Tailwind
- TTS: ElevenLabs (fallback tone if no key)

## Quickstart

### Backend
```bash
cd biowhisper/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend
```bash
cd biowhisper/frontend
npm i
npm run dev
```

- Set `VITE_API_BASE` in `frontend` `.env` if backend is remote.
- For ElevenLabs, export `ELEVENLABS_API_KEY` before starting the backend.

## Endpoints
- `POST /record` — multipart file `file` (WAV). Returns features and filename.
- `POST /analyze` — form fields: `audio_filename` (string). Returns narrative and `tts_url`.
- `GET /uploads/...` — static files served for playback.

## Notes
- Audio upload expects WAV. The frontend captures WebM and converts to WAV in-browser.
- Gemini is stubbed in `modules/gemini_client.py` for demo reliability.
- Tailwind is set up; adjust styles in `frontend/src/styles/tailwind.css`.

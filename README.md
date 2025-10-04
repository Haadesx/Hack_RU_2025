# 🎯 BioWhisper - Personal Wellness Analysis Pipeline

> **Real-time wellness insights through voice, physiology, and posture analysis**

BioWhisper is an AI-powered wellness assistant that combines voice stress analysis, wearable biometric data, and posture assessment to provide personalized, compassionate health insights and actionable recommendations.

Built for **HackerTron 2025** hackathon.

---

## ✨ Features

### Core Functionality (MVP)

- 🎤 **10-Second Voice Check-in**: Real-time voice recording with stress and emotional tone analysis
- 💓 **Wearable Data Integration**: Import CSV files with HR, HRV, and sleep stage data
- 📸 **Posture Assessment**: Webcam-based body alignment and tension detection (MediaPipe)
- 🤖 **AI-Powered Insights**: Gemini-generated compassionate wellness narratives
- 🔊 **Text-to-Speech Audio**: ElevenLabs-generated guided meditations and breathing exercises
- 📊 **Interactive Dashboard**: Beautiful UI showing analysis results and action items

### Stretch Features

- 🌙 Sleep hypnosis audio generation
- 🕐 Circadian rhythm analysis
- 📱 Mobile-responsive Progressive Web App

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  ← User Interface (Vite + Tailwind)
│  (Port 3000)    │
└────────┬────────┘
         │ REST API
         ↓
┌─────────────────┐
│  FastAPI Backend│  ← Python Server (Port 8000)
│  + WebSocket    │
└────────┬────────┘
         │
    ┌────┴────┬───────────┬──────────┐
    ↓         ↓           ↓          ↓
┌───────┐ ┌──────┐ ┌──────────┐ ┌───────┐
│Librosa│ │Gemini│ │MediaPipe │ │Eleven │
│Audio  │ │ AI   │ │  Pose    │ │ Labs  │
│Anlysis│ │      │ │  Detect  │ │  TTS  │
└───────┘ └──────┘ └──────────┘ └───────┘
```

---

## 🚀 Quick Start (24-Hour Hackathon Setup)

### Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **npm or yarn**
- **Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- **ElevenLabs API Key** ([Sign up here](https://elevenlabs.io/))

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd biowhisper

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_key_here
# ELEVENLABS_API_KEY=your_key_here

# Frontend setup
cd ../frontend
npm install
```

### Step 2: Run Backend

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python app.py
# Backend will start on http://localhost:8000
# API docs: http://localhost:8000/docs
```

### Step 3: Run Frontend

```bash
cd frontend
npm run dev
# Frontend will start on http://localhost:3000
```

### Step 4: Open Browser

Navigate to **http://localhost:3000** and start your wellness check-in!

---

## 📁 Project Structure

```
biowhisper/
├── backend/
│   ├── app.py                      # FastAPI main application
│   ├── modules/
│   │   ├── audio_analysis.py       # Voice/stress analysis (librosa)
│   │   ├── pose_analysis.py        # Posture detection (MediaPipe)
│   │   ├── hrv_analysis.py         # Wearable data processing
│   │   ├── prompt_builder.py       # Gemini prompt engineering
│   │   ├── gemini_client.py        # Gemini API integration
│   │   └── tts.py                  # ElevenLabs TTS wrapper
│   ├── uploads/                    # Temporary file storage
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main React app
│   │   ├── components/
│   │   │   ├── Welcome.jsx         # Landing page
│   │   │   ├── RecordingView.jsx   # Voice recording UI
│   │   │   ├── Dashboard.jsx       # Results display
│   │   │   ├── AudioPlayer.jsx     # TTS audio playback
│   │   │   ├── ActionItems.jsx     # Action plan display
│   │   │   └── WearableUpload.jsx  # CSV upload component
│   │   └── styles/
│   │       └── index.css           # Tailwind + custom styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

---

## 🔑 API Endpoints

### Backend (FastAPI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health check |
| `/record` | POST | Upload and analyze audio recording |
| `/wearable/upload` | POST | Upload wearable CSV data |
| `/camera-scan` | POST | Analyze pose keypoints |
| `/analyze` | POST | Full analysis pipeline (audio + wearable + pose → Gemini → TTS) |
| `/audio/{filename}` | GET | Stream generated audio files |
| `/generate-hypnosis` | POST | Generate sleep hypnosis audio |

**API Documentation**: http://localhost:8000/docs (Swagger UI)

---

## 🎨 UI/UX Highlights

- **Accessibility-first**: High contrast, keyboard navigation, screen reader support
- **Micro-interactions**: Smooth animations, breathing circles, waveform visualizations
- **Responsive Design**: Mobile, tablet, and desktop optimized
- **Privacy-focused**: Clear consent modals, data usage explanations

---

## 🧪 Testing

### Test Audio Analysis (Without Frontend)

```bash
cd backend
python -c "
from modules.audio_analysis import analyze_audio
result = analyze_audio('test_audio.wav')
print(result)
"
```

### Generate Sample Wearable Data

```bash
python -c "
from modules.hrv_analysis import generate_sample_wearable_csv
generate_sample_wearable_csv('sample_data.csv')
"
```

### Test Gemini Integration

Make sure `GEMINI_API_KEY` is set in `.env`, then:

```bash
curl -X POST http://localhost:8000/analyze \
  -F "audio_filename=test_recording.webm"
```

---

## 🎯 24-Hour Development Timeline

| Hours | Task | Status |
|-------|------|--------|
| 0-1 | Repo setup, dependencies | ✅ |
| 1-3 | Frontend recording + backend upload | ✅ |
| 3-5 | Audio analysis module | ✅ |
| 5-7 | Wearable ingestion + HRV | ✅ |
| 7-9 | Posture scan (MediaPipe) | ✅ |
| 9-11 | Gemini prompt engineering | ✅ |
| 11-13 | ElevenLabs TTS integration | ✅ |
| 13-15 | Dashboard UI | ✅ |
| 15-18 | UX polish, animations | ✅ |
| 18-21 | Testing, demo flow | 🔄 |
| 21-24 | Final polish, README, demo video | 🔄 |

---

## 🔧 Configuration

### Environment Variables

Create `backend/.env`:

```env
# Gemini API (Required for AI insights)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro

# ElevenLabs API (Required for TTS)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# CORS (adjust for production)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend Environment (Optional)

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

---

## 🎤 Voice Analysis Details

The audio analysis module (`audio_analysis.py`) extracts:

- **RMS Energy**: Vocal intensity/loudness
- **Tempo**: Speaking rate (words per minute proxy)
- **Pitch Statistics**: Mean, variance, standard deviation
- **Zero-Crossing Rate**: Voice roughness/breathiness indicator
- **Spectral Features**: Centroids, rolloff
- **MFCCs**: Tone quality indicators
- **Stress Score**: Composite heuristic (0-1 scale)
- **Emotional Tone**: Classification (calm, anxious, subdued, etc.)

---

## 💓 Wearable Data Format

Expected CSV structure:

```csv
timestamp,heart_rate,hrv_rmssd,sleep_stage,activity_level
2025-10-03 23:00:00,68,42.5,awake,1
2025-10-03 23:01:00,66,45.2,light,0
2025-10-03 23:02:00,62,48.1,deep,0
...
```

**Fields:**
- `timestamp`: ISO format datetime
- `heart_rate`: Beats per minute
- `hrv_rmssd`: Heart rate variability (ms)
- `sleep_stage`: awake, light, deep, rem, N1, N2, N3, REM
- `activity_level`: 0-3 scale (0=sleep, 3=high activity)

---

## 🤖 Gemini Prompt Engineering

The system uses structured prompts to generate:

1. **Compassionate Narrative** (2-3 paragraphs)
2. **Key Observations** (bulleted insights)
3. **Prioritized Action Items** (3 items with timing and impact)
4. **Sleep Hypnosis Script** (200-300 words)
5. **Breathing Exercise** (specific technique with instructions)

**Note**: Gemini is instructed to return **pure JSON** for easy parsing.

---

## 🔊 Text-to-Speech

ElevenLabs integration supports:

- Multiple voice profiles (calm, professional, etc.)
- Adjustable speech parameters (stability, similarity boost)
- Fallback to **gTTS** (Google TTS) when API unavailable
- Generated audio formats: MP3 (primary), WAV (fallback)

---

## 🔒 Privacy & Safety

- **No persistent storage**: Demo mode deletes data after session
- **Local processing first**: Audio analysis runs locally
- **Encrypted transmission**: HTTPS in production
- **No medical claims**: All disclaimers included in UI
- **Explicit consent**: Users must approve data usage

**Important**: This is **not a medical device**. For wellness optimization only.

---

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
lsof -i :8000  # Kill any process using port 8000
```

### Frontend Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Try with legacy peer deps if needed
npm install --legacy-peer-deps
```

### Audio Recording Not Working

- **Check browser permissions**: Chrome/Firefox require HTTPS or localhost
- **Microphone access**: Ensure browser has mic permissions
- **Codec support**: Some browsers don't support `audio/webm`; fallback is implemented

### Gemini API Errors

- Verify API key in `.env`
- Check quota limits at [Google AI Studio](https://makersuite.google.com/)
- Fallback narrative will be used if API unavailable

---

## 📊 Demo Script (60 Seconds)

1. **Welcome Screen** (5s): Show features grid
2. **Start Check-in** (10s): Record 10s voice sample
3. **Processing** (5s): Show loading animation
4. **Dashboard** (20s): 
   - Stress score visualization
   - HRV metrics
   - Narrative card
   - Action items
5. **Audio Playback** (15s): Play breathing exercise clip
6. **Closing** (5s): Show sleep hypnosis generation

---

## 🎓 Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Librosa**: Audio analysis library
- **MediaPipe**: Google's pose detection
- **Pandas/NumPy**: Data processing
- **Gemini API**: Google's LLM for insights
- **ElevenLabs**: Premium TTS

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **Web Audio API**: Recording

---

## 🚢 Deployment (Optional)

### Backend (Railway/Render)

```bash
# Add Procfile
echo "web: uvicorn app:app --host 0.0.0.0 --port \$PORT" > Procfile

# Push to platform
git push railway main  # or render, etc.
```

### Frontend (Vercel/Netlify)

```bash
cd frontend
npm run build
# Upload dist/ folder to platform
```

---

## 🤝 Contributing

This is a hackathon project! Feel free to:

- Report bugs in Issues
- Suggest features
- Submit pull requests
- Fork and build your own version

---

## 📝 License

MIT License - feel free to use this for your own projects!

---

## 👥 Team

Built with ❤️ for HackerTron 2025

**Contact**: [Your contact info]

---

## 🙏 Acknowledgments

- **Gemini API**: Google's powerful LLM
- **ElevenLabs**: Realistic TTS voices
- **MediaPipe**: Pose detection technology
- **Librosa**: Audio analysis library
- **Open source community**: For amazing tools

---

## 📚 Additional Resources

- [Gemini API Docs](https://ai.google.dev/docs)
- [ElevenLabs API Docs](https://elevenlabs.io/docs)
- [MediaPipe Guide](https://google.github.io/mediapipe/)
- [Librosa Documentation](https://librosa.org/doc/latest/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

**Ready to build? Let's go! 🚀**

For questions or support during the hackathon, refer to the inline code comments or the API documentation at `http://localhost:8000/docs`.

---

### Next Steps After MVP

1. **Add authentication** (Firebase/Auth0)
2. **Persistent storage** (PostgreSQL + S3)
3. **Real-time wearable sync** (Fitbit/Apple Health APIs)
4. **Social features** (Share progress, challenges)
5. **Mobile app** (React Native)
6. **Advanced ML** (Custom emotion detection models)
7. **Telehealth integration** (Share reports with practitioners)

---

**Happy Hacking! 🎉**

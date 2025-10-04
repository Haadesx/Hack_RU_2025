# BioWhisper - Compassionate Wellness Assistant

> AI-powered wellness analysis through voice, posture, and biometric data

## 🌟 Overview

BioWhisper is a compassionate wellness assistant that analyzes your voice, posture, and biometric data to provide personalized wellness insights and audio experiences. Built for hackathons and wellness enthusiasts.

## ✨ Features

- **Voice Analysis**: Stress detection, emotion recognition, energy levels
- **Biometric Integration**: HRV analysis, sleep quality, recovery scoring  
- **Posture Assessment**: Camera-based posture analysis with MediaPipe
- **AI Insights**: Personalized narratives via Gemini AI
- **Audio Experiences**: TTS narratives, breathing exercises, sleep hypnosis
- **Privacy-First**: All analysis happens locally, no permanent storage

## 🚀 Quick Start (24-Hour Hackathon Ready!)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Camera and microphone access
- Optional: API keys for Gemini and ElevenLabs

### 1. Clone and Setup Backend

```bash
cd backend
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys (optional for demo mode)

# Start the backend
python app.py
```

### 2. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Open Your Browser

Navigate to `http://localhost:3000` and start your wellness check-in!

## 🔧 Configuration

Create `backend/.env` with your API keys:

```env
# Optional: For enhanced AI responses
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here

# Optional: For high-quality TTS
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

**Note**: The app works in demo mode without API keys, using mock data and system TTS.

## 🏗️ Architecture

```
biowhisper/
├── backend/                 # FastAPI server
│   ├── app.py              # Main API server
│   ├── modules/            # Analysis modules
│   │   ├── audio_analysis.py    # Voice stress/emotion detection
│   │   ├── pose_analysis.py     # Posture assessment  
│   │   ├── hrv_analysis.py      # Biometric analysis
│   │   ├── prompt_builder.py    # AI prompt generation
│   │   ├── gemini_client.py     # Gemini AI integration
│   │   └── tts.py              # Text-to-speech
│   └── uploads/            # Temporary file storage
└── frontend/               # React app
    ├── src/
    │   ├── App.jsx         # Main app component
    │   └── components/     # UI components
    └── public/
```

## 🎯 API Endpoints

- `POST /record` - Upload and analyze voice recording
- `POST /wearable/upload` - Upload biometric CSV data
- `POST /camera-scan` - Analyze posture keypoints
- `POST /analyze` - Comprehensive wellness analysis
- `POST /generate-sleep-hypnosis` - Generate sleep audio
- `GET /health` - Health check

## 📊 Data Flow

1. **Voice Recording** → Audio analysis → Stress/emotion scores
2. **Biometric Upload** → HRV/sleep analysis → Recovery scores  
3. **Camera Capture** → Pose detection → Posture assessment
4. **AI Analysis** → Gemini prompt → Personalized insights
5. **Audio Generation** → TTS services → Wellness audio

## 🛠️ Tech Stack

**Backend**:
- FastAPI (Python web framework)
- LibROSA (audio analysis)
- MediaPipe (pose detection)
- Pandas (data processing)
- Gemini API (AI insights)
- ElevenLabs API (TTS)

**Frontend**:
- React 18 + Vite
- Tailwind CSS (styling)
- Howler.js (audio playback)
- React Query (state management)

## 📱 Usage Flow

1. **Welcome** → Start voice check-in
2. **Voice Recording** → 10-second emotional check-in
3. **Biometric Upload** → Optional CSV from wearables
4. **Camera Scan** → Optional posture assessment
5. **Analysis** → AI-powered wellness insights
6. **Results** → Personalized narrative + audio experiences

## 🎨 Demo Data

For demo purposes, the app includes:
- Mock biometric data generation
- Simulated pose keypoints
- Fallback AI responses
- System TTS backup

## 🔒 Privacy & Security

- No permanent data storage
- Local processing when possible
- Temporary files auto-cleaned
- User consent for camera/microphone
- No medical diagnostic claims

## 🚀 Deployment

### Local Development
```bash
# Backend (Terminal 1)
cd backend && python app.py

# Frontend (Terminal 2) 
cd frontend && npm run dev
```

### Production Build
```bash
# Build frontend
cd frontend && npm run build

# Serve with uvicorn
cd backend && uvicorn app:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)
```bash
docker-compose up --build
```

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest

# Frontend (if tests added)
cd frontend && npm test
```

## 🌈 Customization

- **Voice Types**: Edit `VOICE_IDS` in `tts.py`
- **Analysis Weights**: Modify scoring in analysis modules  
- **UI Themes**: Update `tailwind.config.js`
- **Prompts**: Customize templates in `prompt_builder.py`

## 🐛 Troubleshooting

**Camera not working?**
- Check browser permissions
- Try HTTPS or localhost only
- Refresh page and allow access

**Audio upload fails?**
- Check microphone permissions
- Ensure WebRTC support
- Try different browser

**No AI responses?**
- App works without API keys (demo mode)
- Check `.env` file configuration
- Verify API key validity

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- MediaPipe for pose detection
- LibROSA for audio analysis
- Gemini AI for wellness insights
- ElevenLabs for natural TTS
- Tailwind CSS for beautiful UI

---

**🌱 Built with compassion for wellness and mental health awareness.**

For questions or support, please open an issue or contact the development team.
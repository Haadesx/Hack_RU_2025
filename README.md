# BioWhisper - AI Wellness Assistant

A comprehensive wellness analysis platform that combines voice analysis, biometric data, and posture scanning to provide personalized health insights and guided relaxation experiences.

## 🌟 Features

### Core Functionality
- **Real-time Voice Analysis**: 10-second voice check-ins with stress, energy, and emotional tone detection
- **Biometric Integration**: HRV analysis, sleep pattern recognition, and circadian rhythm assessment
- **Posture Scanning**: AI-powered posture analysis using MediaPipe for tension detection
- **AI-Powered Insights**: Gemini-generated personalized wellness narratives and recommendations
- **Audio Generation**: ElevenLabs TTS for guided breathing exercises and sleep hypnosis

### Technical Highlights
- **FastAPI Backend**: High-performance Python API with real-time processing
- **React Frontend**: Modern, responsive UI with Tailwind CSS
- **Audio Processing**: Advanced librosa-based voice analysis
- **Privacy-First**: Local data processing with optional cloud integration
- **Real-time Visualization**: Live audio waveform and wellness metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Microphone access
- Webcam (optional, for posture scanning)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd biowhisper
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r ../requirements.txt
   
   # Copy environment variables
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Run the Application**
   ```bash
   # Terminal 1: Backend
   cd backend
   python app.py
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# ElevenLabs API Key (for text-to-speech)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Gemini API Key (for AI wellness insights)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Server configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### API Keys Setup

1. **ElevenLabs**: Sign up at [elevenlabs.io](https://elevenlabs.io) and get your API key
2. **Gemini**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📱 Usage Guide

### 1. Voice Check-in
- Click "Start Your Wellness Check-in"
- Allow microphone access when prompted
- Speak naturally for 10 seconds about how you're feeling
- The system will analyze your voice for stress, energy, and emotional indicators

### 2. Data Collection (Optional)
- **Wearable Data**: Upload CSV files from fitness trackers
- **Posture Scan**: Use webcam for posture analysis
- **Manual Input**: Add additional wellness metrics

### 3. Analysis & Insights
- View comprehensive wellness analysis
- Read AI-generated personalized insights
- Access actionable recommendations
- Listen to guided breathing exercises

### 4. Dashboard
- Track wellness trends over time
- View historical data and patterns
- Access personalized insights
- Manage preferences and settings

## 🏗️ Architecture

### Backend Structure
```
backend/
├── app.py                 # FastAPI main application
├── modules/
│   ├── audio_analysis.py  # Voice processing and stress detection
│   ├── pose_analysis.py   # MediaPipe posture analysis
│   ├── hrv_analysis.py   # Heart rate variability calculations
│   ├── prompt_builder.py  # Gemini prompt construction
│   ├── gemini_client.py  # AI insights generation
│   └── tts.py            # ElevenLabs text-to-speech
└── uploads/              # Temporary file storage
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/       # React components
│   ├── context/          # State management
│   └── App.jsx          # Main application
├── package.json
└── tailwind.config.js
```

## 🔬 Technical Details

### Audio Analysis
- **Stress Detection**: Composite score based on energy, tempo, pitch variance, and spectral features
- **Voice Features**: RMS, spectral centroid, zero-crossing rate, MFCC coefficients
- **Real-time Processing**: WebAudio API for browser-based recording

### Biometric Analysis
- **HRV Metrics**: RMSSD, SDNN, frequency domain analysis
- **Sleep Analysis**: Sleep stage distribution and quality scoring
- **Circadian Patterns**: Peak/trough detection and rhythm assessment

### Posture Analysis
- **MediaPipe Integration**: Real-time pose landmark detection
- **Tension Indicators**: Forward head posture, shoulder alignment, spinal deviation
- **Recommendations**: Personalized exercises and posture corrections

## 🛡️ Privacy & Security

- **Local Processing**: All sensitive data stays on your device
- **Encrypted Storage**: Secure handling of biometric data
- **Consent-Based**: Explicit permission for each data type
- **Data Retention**: Configurable data storage policies
- **No Tracking**: No personal information sent to third parties

## 🎯 Demo Flow

1. **Welcome Screen**: Introduction and feature overview
2. **Recording**: 10-second voice check-in with live visualization
3. **Analysis**: Comprehensive wellness assessment
4. **Insights**: AI-generated personalized recommendations
5. **Audio**: Guided breathing and relaxation exercises
6. **Dashboard**: Historical trends and wellness patterns

## 🚧 Development Roadmap

### MVP Features (Completed)
- ✅ Voice recording and analysis
- ✅ Basic stress detection
- ✅ AI-powered insights
- ✅ Audio generation
- ✅ Web interface

### Stretch Features
- 🔄 Sleep hypnosis generation
- 🔄 Mobile app development
- 🔄 Advanced biometric integration
- 🔄 Social features and sharing
- 🔄 Professional wellness coaching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **MediaPipe**: For pose detection capabilities
- **ElevenLabs**: For high-quality text-to-speech
- **Google Gemini**: For AI-powered insights
- **Librosa**: For audio processing and analysis
- **FastAPI**: For the robust backend framework
- **React**: For the modern frontend experience

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Check the documentation
- Review the API documentation at `/docs`

---

**BioWhisper** - Empowering wellness through AI-driven insights and personalized care.
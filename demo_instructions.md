# BioWhisper Demo Instructions

## 🎯 30-Second Demo Script

### Setup (Pre-demo)
1. Start backend: `cd backend && python app.py`  
2. Start frontend: `cd frontend && npm run dev`
3. Open `http://localhost:3000`
4. Test microphone/camera permissions

### Demo Flow (30-60 seconds)

**1. Welcome & Start (5s)**
- "Meet BioWhisper - your compassionate AI wellness assistant"
- Click "Start 10-Second Check-in"

**2. Voice Recording (15s)**  
- Record 10s: "I'm feeling pretty stressed from work today, a bit tired but trying to stay positive"
- Show waveform visualization
- Click "Continue to Biometrics"

**3. Quick Data Upload (10s)**
- Click "Skip Biometrics" (or upload sample CSV if prepared)
- Click "Skip Posture Scan" (or do quick camera capture)
- Click "Generate Wellness Insights"

**4. Results Showcase (30s)**
- Show AI narrative: compassionate, personalized response
- Highlight key metrics: stress score, recommendations  
- **Play audio**: "Listen to your personalized narrative"
- **Demo breathing exercise**: Click play on 3-minute breathing
- Show action items: specific, actionable recommendations

### Key Demo Points to Emphasize

🎤 **Voice Analysis**: "Detected moderate stress in your voice tone and speaking patterns"

🧠 **AI Insights**: "Gemini AI generates personalized, compassionate responses - not generic advice"

🎵 **Audio Experiences**: "TTS creates calming audio narratives and breathing exercises"

📊 **Comprehensive**: "Combines voice + biometrics + posture for holistic wellness assessment"

🔒 **Privacy**: "All data stays local - no permanent storage, completely private"

## 🎬 Extended Demo (2-3 minutes)

If you have more time, show:

1. **Full biometric upload** with sample CSV
2. **Camera posture scan** with live pose detection  
3. **Sleep hypnosis generation** - demonstrate personalized sleep audio
4. **Data breakdown** - show technical analysis behind the scenes

## 📁 Demo Assets

Create these files for smooth demo:

**Sample wearable CSV** (`demo_data.csv`):
```csv
timestamp,heart_rate,hrv_rmssd,sleep_stage
2024-01-01 00:00:00,65,28,deep
2024-01-01 01:00:00,62,32,deep
2024-01-01 02:00:00,58,35,light
```

**Demo voice script options**:
- Stressed: "I'm feeling overwhelmed with work deadlines and haven't been sleeping well"
- Tired: "I'm pretty exhausted today, low energy, just trying to get through"
- Positive: "Feeling good today, energetic and ready to tackle my goals"

## 🚨 Troubleshooting During Demo

**If microphone fails:**
- "This works with any audio input - let me show you with a pre-recorded sample"
- Continue with mock audio data

**If camera fails:**
- "Posture analysis works great, but let's skip to show the AI insights"
- Use skip button

**If AI is slow:**
- "While Gemini generates insights, notice the real-time audio analysis we already captured"
- Show the technical metrics

**If TTS fails:**  
- "Audio generation typically takes 10-15 seconds - here's what a sample sounds like"
- Have backup audio file ready

## 💬 Judge Q&A Prep

**"How accurate is the stress detection?"**
- "We use proven audio analysis techniques from LibROSA - same tech used in research"
- "Combined with HRV and posture, it creates a comprehensive picture"

**"What makes this different from other wellness apps?"**
- "Compassionate AI that provides personalized insights, not generic advice" 
- "Multi-modal analysis: voice + biometrics + posture in one platform"
- "Generated audio experiences - not just text recommendations"

**"How do you handle privacy?"**
- "Everything processes locally when possible"
- "No permanent storage - files auto-delete after analysis" 
- "Users control what data they share"

**"What's the technical innovation?"**
- "Real-time multi-modal wellness analysis"
- "AI prompt engineering for compassionate, actionable responses"
- "Seamless integration of multiple AI APIs (Gemini + ElevenLabs)"

## 🏆 Hackathon Categories

Position BioWhisper for these categories:

- **Best Use of AI**: Multi-modal analysis + compassionate AI responses
- **Best UI/UX**: Clean, accessible interface with privacy-first design  
- **Social Impact**: Mental health awareness and wellness accessibility
- **Technical Achievement**: Real-time audio analysis + pose detection integration
- **Most Innovative**: Personalized audio wellness experiences

## 📱 Mobile Demo Notes

If showing on mobile:
- Works as responsive web app
- Voice recording works great on phones
- Camera for posture works well
- Audio playback smooth on mobile browsers

---

**🎯 Key Message**: "BioWhisper makes wellness insights accessible, personalized, and compassionate through AI - helping people understand their bodies and minds better."
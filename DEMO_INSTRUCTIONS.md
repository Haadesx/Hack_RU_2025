# 🎬 BioWhisper Demo Instructions

## Quick Demo Setup (5 Minutes)

### For Judges / Demo Day

1. **Start Backend**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python app.py
   ```
   Backend runs at: `http://localhost:8000`

2. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend opens at: `http://localhost:3000`

3. **Open Browser**
   Navigate to `http://localhost:3000`

---

## 🎯 Demo Flow (60 Seconds)

### Act 1: Welcome (10s)

**Script**: "BioWhisper is your personal wellness assistant that analyzes voice, physiology, and posture to give you actionable health insights."

**Actions**:
- Show welcome page with 3 feature cards
- Highlight "10-second check-in" CTA
- Click "Start 10s Check-in"

### Act 2: Consent & Recording (15s)

**Script**: "Privacy is paramount. We only use data with explicit consent, and everything is processed securely."

**Actions**:
- Show consent modal (read key points)
- Click "I Understand, Continue"
- Record 10s audio: "I'm feeling a bit stressed today. Didn't sleep well last night and have a lot on my mind."
- Show waveform visualization
- Recording auto-stops at 10s

### Act 3: Processing (5s)

**Script**: "Our AI analyzes vocal stress, emotional tone, and correlates with physiological data."

**Actions**:
- Show loading spinner with progress indicators
- Auto-transitions to dashboard

### Act 4: Dashboard (25s)

**Script**: "Here's the magic. BioWhisper shows a comprehensive wellness summary."

**Actions**:
1. **Status Header** (3s): Point out stress level badge (e.g., "Elevated Stress")
2. **Metrics Grid** (5s):
   - Voice analysis: stress score 68%
   - Physiological: HRV 45ms, HR 72bpm, sleep 6.5hrs
   - Wellness score: 68/100
3. **Narrative** (8s): Read first paragraph of personalized story
4. **Action Items** (5s): Show prioritized action plan:
   - Priority 1: 3-minute breathing reset
   - Priority 2: Posture adjustment
   - Priority 3: Sleep optimization
5. **Audio Player** (4s): Click play on breathing exercise (let it run 3-5s)

### Act 5: Features (5s)

**Script**: "You can also upload wearable data and generate custom sleep hypnosis audio."

**Actions**:
- Scroll to wearable upload section
- (Optional) Show sleep hypnosis generation button

---

## 🗣️ Talking Points

### What Problem Does It Solve?

"Modern wellness tracking is fragmented. You have voice journals, wearables, and posture apps—but no unified insights. BioWhisper connects the dots using AI to give you a complete wellness picture in under a minute."

### Why It's Unique

1. **Multi-modal Analysis**: Voice + biometrics + posture in one place
2. **Compassionate AI**: Gemini generates empathetic, non-judgmental guidance
3. **Actionable Insights**: Not just data—prioritized action plans with timing and impact
4. **Audio Interventions**: TTS-generated breathing exercises and sleep hypnosis
5. **Privacy-First**: Local processing, no persistent storage, explicit consent

### Technical Highlights

**Backend**:
- FastAPI for high-performance API
- Librosa for sophisticated audio analysis
- MediaPipe for pose detection
- Gemini for contextual AI insights
- ElevenLabs for premium TTS

**Frontend**:
- React with Vite for blazing-fast dev
- Tailwind for beautiful, responsive UI
- Web Audio API for recording
- Real-time visualizations

### Target Users

- **Individuals**: Daily wellness check-ins
- **Remote workers**: Combat burnout, track stress
- **Athletes**: Recovery and sleep optimization
- **Therapists**: Augment sessions with biometric insights
- **Corporate wellness**: Employee wellbeing programs

---

## 🎥 Demo Tips

### Before Demo

1. **Test microphone**: Ensure permissions granted
2. **Prepare test recording**: Know what to say (stress-related content works best)
3. **Check API keys**: Verify Gemini and ElevenLabs are configured
4. **Clear cache**: Fresh session for clean demo
5. **Full screen browser**: Hide bookmarks/tabs for clean view

### During Demo

1. **Speak slowly**: Let audience absorb features
2. **Pause on key screens**: Dashboard metrics, action items
3. **Highlight privacy**: Judges love privacy-first approaches
4. **Show personality**: The AI narrative is warm and human
5. **Play audio**: Even 3 seconds shows TTS quality

### If Something Breaks

**Fallback Plans**:

- **Recording fails**: Show pre-recorded screen capture
- **API timeout**: Fallback narratives are built-in
- **Audio won't play**: Describe what it would sound like
- **Internet issues**: Demo works 90% offline (except Gemini/TTS)

---

## 📊 Key Metrics to Highlight

- **Speed**: Analysis completes in < 10 seconds
- **Accuracy**: Voice stress correlation with HRV
- **Actionability**: 3 prioritized action items with timing
- **Engagement**: TTS audio keeps users engaged

---

## 🏆 Winning Angles for Judges

### Innovation
"First platform to unify voice, biometrics, and posture with AI-generated interventions"

### Technical Excellence
"Production-ready FastAPI backend, real-time audio processing, seamless Gemini integration"

### Impact
"Makes wellness accessible—no expensive wearables required, just 10 seconds and a microphone"

### Design
"Beautiful, accessible UI with micro-interactions and breathing animations"

### Scalability
"Modular architecture ready for mobile app, wearable SDKs, and telehealth integration"

---

## 🎤 Sample Recording Scripts

### High Stress
"I'm feeling really overwhelmed today. Barely got 5 hours of sleep, and I have back-to-back meetings. My shoulders feel tense, and I can't seem to catch my breath."

### Moderate
"Pretty normal day. Slept okay, around 7 hours. Feeling a bit tired but manageable. Could use a break to reset."

### Calm
"I'm feeling pretty good today! Got 8 hours of sleep, went for a morning walk. Feeling energized and ready to tackle the day."

---

## 📹 Screen Recording Checklist

If recording a demo video:

- [ ] Hide personal bookmarks/tabs
- [ ] Enable "Do Not Disturb" mode
- [ ] Test audio input levels
- [ ] Close unnecessary apps
- [ ] Use 1920x1080 resolution
- [ ] Record at 60fps for smooth animations
- [ ] Add captions/annotations in post

---

## 🐛 Common Demo Issues & Fixes

### Issue: Microphone not working
**Fix**: Open browser settings → Privacy → Microphone → Allow

### Issue: Backend API errors
**Fix**: Check `.env` file has valid API keys

### Issue: CORS errors in frontend
**Fix**: Ensure backend is running and CORS origins configured

### Issue: Audio won't upload
**Fix**: Check `backend/uploads/` directory exists and is writable

### Issue: Gemini timeouts
**Fix**: Fallback narrative will display automatically (designed for demos)

---

## 🌟 Stretch Demo Features (If Time)

1. **Wearable Upload**: Show CSV import functionality
2. **Sleep Hypnosis**: Generate custom sleep audio
3. **Posture Scan**: Use webcam for live pose detection (if implemented)
4. **Historical Tracking**: Show multiple check-ins over time (future feature)

---

## 📝 Q&A Prep

### Likely Judge Questions

**Q: How accurate is the voice stress detection?**
A: We use librosa's audio feature extraction (pitch, energy, zero-crossing rate) combined with established stress correlates. While not clinical-grade, it's effective for wellness trend tracking. Studies show vocal pitch variance correlates with cortisol levels.

**Q: What about false positives?**
A: That's why we use multi-modal analysis. Voice alone can be ambiguous, but combined with HRV and posture, we get higher confidence. The AI is also trained to be cautious and non-diagnostic.

**Q: Privacy concerns with audio?**
A: Audio is processed and deleted immediately. No persistent storage in demo mode. Production version would encrypt and give users full data control.

**Q: Why not just use a wearable?**
A: Wearables are great, but not everyone has one. Voice is universal—you just need a microphone. We integrate wearables as optional enhancement.

**Q: Business model?**
A: B2C subscription ($5-10/mo), B2B corporate wellness ($X per employee), API licensing to telehealth platforms.

**Q: What's the tech stack advantage?**
A: FastAPI is 2-3x faster than Flask, React with Vite has sub-second HMR, Gemini gives us contextual awareness other LLMs lack, ElevenLabs TTS is indistinguishable from humans.

---

## ✅ Pre-Demo Checklist

- [ ] Backend running (`http://localhost:8000/docs` loads)
- [ ] Frontend running (`http://localhost:3000` loads)
- [ ] Microphone permission granted
- [ ] API keys configured (`.env` file)
- [ ] Sample wearable CSV ready (if demoing upload)
- [ ] Demo script printed/memorized
- [ ] Fallback video recorded (just in case)
- [ ] Team roles assigned (who talks, who clicks)

---

**Break a leg! 🎉**

Remember: **Judges are looking for impact, innovation, and execution**. BioWhisper hits all three. Show the personality of the AI, the beauty of the UI, and the real-world value. You've got this!

---

## 📞 Emergency Contacts

**Tech Issues During Demo**: [Your contact]  
**Backend Lead**: [Your contact]  
**Frontend Lead**: [Your contact]

---

Good luck! 🚀

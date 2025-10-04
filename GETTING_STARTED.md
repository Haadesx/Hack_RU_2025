# 🎬 Getting Started with BioWhisper

**Complete checklist to go from setup to first demo in 10 minutes**

---

## ✅ Pre-Flight Checklist

### System Requirements

- [ ] **Python 3.9 or higher** installed
  ```bash
  python3 --version  # Should show 3.9.x or higher
  ```

- [ ] **Node.js 18 or higher** installed
  ```bash
  node --version  # Should show v18.x or higher
  ```

- [ ] **npm** installed (comes with Node.js)
  ```bash
  npm --version
  ```

- [ ] **Git** installed (if cloning from repo)
  ```bash
  git --version
  ```

### Browser Requirements

- [ ] Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+
- [ ] Microphone available (for voice recording)
- [ ] Webcam (optional, for posture scan)

---

## 🚀 Installation Steps

### Step 1: Get the Code

If from GitHub:
```bash
git clone <your-repo-url>
cd biowhisper
```

If from zip:
```bash
unzip biowhisper.zip
cd biowhisper
```

✅ **Verify**: You should see `backend/` and `frontend/` directories

---

### Step 2: Automatic Setup (Recommended)

**Linux / macOS**:
```bash
bash setup.sh
```

**Windows**:
```bash
setup.bat
```

This will:
- Create Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Create `.env` files from examples
- Set up directory structure

⏱️ **Time**: 2-3 minutes

---

### Step 3: Manual Setup (If Automatic Fails)

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
cp .env.example .env

cd ..
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

cd ..
```

---

### Step 4: Configure API Keys

#### Get Your Keys (Free Tier Available)

1. **Gemini API Key**:
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the key

2. **ElevenLabs API Key** (Optional but recommended):
   - Go to: https://elevenlabs.io/
   - Sign up for free account
   - Go to Profile → API Keys
   - Copy the key

#### Add Keys to Backend

Edit `backend/.env`:

```env
GEMINI_API_KEY=your_actual_gemini_key_here
ELEVENLABS_API_KEY=your_actual_elevenlabs_key_here
```

> **Note**: If you skip this, the app will work with fallback features (local narratives and gTTS)

---

### Step 5: Test Backend

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run module tests
python test_modules.py
```

✅ **Expected Output**: "All module tests passed!"

---

### Step 6: Start Backend Server

```bash
# From backend/ directory with venv activated
python app.py
```

✅ **Expected Output**:
```
🎯 Starting BioWhisper API server...
📍 API docs: http://localhost:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it**: Open http://localhost:8000 in browser
- Should see: `{"message": "BioWhisper API - Wellness Analysis Pipeline"}`

**Explore API**: http://localhost:8000/docs
- Interactive Swagger UI documentation

---

### Step 7: Start Frontend (New Terminal)

```bash
cd frontend
npm run dev
```

✅ **Expected Output**:
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

---

### Step 8: Open Application

Open browser to: **http://localhost:3000**

✅ **You Should See**:
- BioWhisper welcome screen
- "Start 10s Check-in" button
- Three feature cards (Voice, Wearable, Posture)

---

## 🎯 First Demo Run

### Test 1: Voice Recording

1. Click **"Start 10s Check-in"**
2. Read consent modal, click **"I Understand, Continue"**
3. Allow microphone access when prompted
4. Click the **microphone button** to start recording
5. Speak for 10 seconds (example below)
6. Recording auto-stops, processes, shows dashboard

**Example Script**:
> "I'm feeling a bit stressed today. Didn't sleep great last night, maybe 6 hours. My neck and shoulders feel tense from sitting at my desk. Could use a break."

✅ **Expected Result**: Dashboard with stress analysis, metrics, narrative, and action items

---

### Test 2: Play Audio

On the dashboard:

1. Find **"Your Wellness Narrative"** card
2. Click the **play button**
3. Listen to AI-generated personalized summary

✅ **Expected Result**: Human-like voice reading your wellness narrative

---

### Test 3: Generate Sample Wearable Data (Optional)

```bash
cd backend
python -c "from modules.hrv_analysis import generate_sample_wearable_csv; generate_sample_wearable_csv('sample_wearable.csv')"
```

Then in the UI:
1. Scroll to **"Add Wearable Data"** section
2. Click **"Upload CSV"**
3. Select `backend/sample_wearable.csv`
4. Analysis updates with HRV and sleep data

---

## 🐛 Troubleshooting

### Backend Won't Start

**Symptom**: Import errors, module not found

**Fix**:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

---

### Frontend Won't Start

**Symptom**: npm errors, dependency issues

**Fix**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

### Port Already in Use

**Symptom**: "Address already in use" error

**Fix (Backend)**:
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
# OR
netstat -ano | findstr :8000  # Windows - note PID
taskkill /PID <PID> /F  # Windows - replace <PID>
```

**Fix (Frontend)**:
```bash
# Kill process on port 3000 (similar to above)
lsof -ti:3000 | xargs kill -9
```

---

### Microphone Not Working

**Symptom**: "Permission denied" or no recording

**Fix**:
1. Ensure using `localhost` or `https://` (not `http://IP`)
2. Check browser permissions:
   - Chrome: Settings → Privacy → Site Settings → Microphone
   - Firefox: Preferences → Privacy → Permissions → Microphone
3. Try different browser (Chrome recommended)
4. Restart browser after granting permissions

---

### API Keys Not Working

**Symptom**: Timeouts, "API error" messages

**Fix**:
1. Verify keys are correct in `backend/.env`
2. Check no extra spaces or quotes in `.env`
3. Restart backend server after editing `.env`
4. Check API quota limits (free tier has limits)

**Fallback**: App works without keys (uses local narratives and gTTS)

---

## 📊 Verification Checklist

Before demo/presentation:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Can record 10-second audio
- [ ] Dashboard displays after recording
- [ ] Audio player works (can play TTS)
- [ ] Metrics show realistic values
- [ ] Action items display properly
- [ ] UI is responsive (test mobile view)
- [ ] No console errors (check browser DevTools)

---

## 🎬 Demo Tips

### Prepare Demo Script

**60-Second Version**:
1. Show welcome screen (5s)
2. Start recording (10s)
3. Show processing (5s)
4. Walk through dashboard (30s)
5. Play audio (10s)

### Test Recording Scripts

**High Stress**:
> "I'm really overwhelmed. Barely slept, maybe 4 hours. Back-to-back meetings all day. My shoulders are killing me and I can't seem to focus."

**Moderate**:
> "Pretty normal day. Slept okay, about 7 hours. Feeling a bit tired but nothing major. Just looking for ways to optimize."

**Low Stress**:
> "Feeling great today! Got a solid 8 hours of sleep, went for a morning walk. Energy levels are high and I'm ready to tackle the day."

---

## 🚀 Next Steps After First Run

1. **Customize Prompts**: Edit `backend/modules/prompt_builder.py`
2. **Add Voices**: Update voice IDs in `backend/modules/tts.py`
3. **Style Frontend**: Modify `frontend/tailwind.config.js`
4. **Add Features**: See `README.md` for architecture
5. **Deploy**: See deployment section in `README.md`

---

## 📚 Documentation Reference

- **Setup Issues**: See "Troubleshooting" in `README.md`
- **Demo Script**: See `DEMO_INSTRUCTIONS.md`
- **Architecture**: See `ARCHITECTURE.md`
- **API Details**: http://localhost:8000/docs (when running)

---

## 🆘 Still Stuck?

1. **Check Logs**:
   - Backend: Look at terminal where `python app.py` is running
   - Frontend: Check browser console (F12)

2. **Test Modules**:
   ```bash
   cd backend
   python test_modules.py
   ```

3. **Verify Files**:
   ```bash
   # Should see all these
   ls backend/*.py
   ls backend/modules/*.py
   ls frontend/src/components/*.jsx
   ```

4. **Clean Restart**:
   ```bash
   # Kill all servers
   # Delete venv/ and node_modules/
   # Re-run setup.sh or setup.bat
   ```

---

## ✅ Success Indicators

You're ready when:

- ✅ Backend starts without errors
- ✅ Frontend shows welcome screen
- ✅ Can record and see waveform
- ✅ Dashboard displays after recording
- ✅ Can play audio without errors
- ✅ Metrics show reasonable values
- ✅ UI looks beautiful and responsive

---

## 🎉 You're Ready!

**Congratulations!** BioWhisper is now running locally.

**Time from zero to demo**: ~10 minutes

**Next**: Try recording different emotional tones and see how the AI adapts its narrative!

---

**Need help?** Review `README.md` or check inline code comments.

**Ready to deploy?** See deployment section in `README.md`.

**Building on this?** See `ARCHITECTURE.md` for technical details.

---

**Happy hacking! 🚀**

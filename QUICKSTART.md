# ⚡ BioWhisper Quick Start

> Get up and running in 5 minutes!

---

## 🚀 One-Command Setup

### Linux / macOS

```bash
bash setup.sh
```

### Windows

```bash
setup.bat
```

This will:
- ✅ Create Python virtual environment
- ✅ Install all dependencies (backend + frontend)
- ✅ Create `.env` files from examples
- ✅ Set up directory structure

---

## 🔑 Configure API Keys

1. **Get API Keys** (both free tier available):
   - [Gemini API](https://makersuite.google.com/app/apikey) - For AI insights
   - [ElevenLabs](https://elevenlabs.io/) - For text-to-speech

2. **Edit `backend/.env`**:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_key_here
   ```

> **Note**: The app will work with fallback features if API keys aren't configured, but AI insights and premium TTS won't be available.

---

## ▶️ Run the Application

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python app.py
```

✅ Backend running at: **http://localhost:8000**  
📚 API docs at: **http://localhost:8000/docs**

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend running at: **http://localhost:3000**

---

## 🎯 Test It Out

1. Open **http://localhost:3000**
2. Click **"Start 10s Check-in"**
3. Accept consent and record a 10-second voice message
4. View your personalized wellness analysis!

### Example Recording Script

> "I'm feeling pretty stressed today. Didn't sleep well last night, only got about 5 hours. My shoulders feel tense from sitting at my desk all day."

---

## 🧪 Verify Installation

### Test Backend Modules

```bash
cd backend
source venv/bin/activate
python test_modules.py
```

Should output:
```
🧪 Testing BioWhisper Backend Modules
...
✅ All module tests passed!
```

### Test API Endpoints

With backend running:

```bash
# Health check
curl http://localhost:8000/

# API docs
open http://localhost:8000/docs  # macOS
# or visit in browser
```

---

## 📦 What Gets Installed

### Backend (Python)
- **FastAPI** - Web framework
- **Librosa** - Audio analysis
- **MediaPipe** - Pose detection
- **Pandas** - Data processing
- **aiohttp** - Async HTTP client

### Frontend (Node)
- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

---

## 🐛 Common Issues

### Issue: `python: command not found`
**Fix**: Use `python3` instead, or create alias:
```bash
alias python=python3
```

### Issue: Port 8000 already in use
**Fix**: Kill existing process or change port in `backend/app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed port
```

### Issue: `npm install` fails
**Fix**: Clear cache and retry:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Issue: Microphone not working
**Fix**: 
- Browser must be on `localhost` or `https://`
- Check browser permissions: Settings → Privacy → Microphone
- Try different browser (Chrome/Firefox recommended)

### Issue: API calls timing out
**Fix**: Check `.env` file for valid API keys, or proceed with fallback mode

---

## 🎨 Optional: Sample Data

Generate sample wearable data for testing:

```bash
cd backend
python -c "from modules.hrv_analysis import generate_sample_wearable_csv; generate_sample_wearable_csv('sample_wearable.csv')"
```

Then upload `sample_wearable.csv` through the UI.

---

## 📱 Mobile Testing

Frontend is responsive! Test on mobile by:

1. Find your local IP: `ifconfig` (macOS/Linux) or `ipconfig` (Windows)
2. Update `frontend/.env`:
   ```
   VITE_API_URL=http://YOUR_IP:8000
   ```
3. Access from mobile browser: `http://YOUR_IP:3000`

---

## 🔥 Pro Tips

1. **Use ngrok for remote demo**:
   ```bash
   ngrok http 8000  # Exposes backend publicly
   # Update frontend .env with ngrok URL
   ```

2. **Hot reload**: Both frontend and backend auto-reload on file changes

3. **Debug mode**: Check browser console (F12) for frontend errors, terminal for backend logs

4. **API exploration**: Use Swagger UI at `http://localhost:8000/docs` to test endpoints manually

---

## 📊 What to Expect

### First Run
- Backend: ~30 seconds to install dependencies
- Frontend: ~2 minutes to install dependencies
- First API call: ~5-10 seconds (Gemini + TTS)

### Subsequent Runs
- Backend startup: <2 seconds
- Frontend dev server: <1 second
- API calls: <3 seconds

---

## 🎯 Next Steps

Once running:

1. ✅ Record a voice check-in
2. ✅ View your wellness dashboard
3. ✅ Play generated audio
4. 📤 (Optional) Upload wearable CSV
5. 📸 (Optional) Add pose analysis
6. 🌙 (Optional) Generate sleep hypnosis

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Demo Script**: See `DEMO_INSTRUCTIONS.md`
- **Architecture**: See `ARCHITECTURE.md`
- **API Reference**: `http://localhost:8000/docs`

---

## 🆘 Need Help?

1. Check the [Troubleshooting](#-common-issues) section above
2. Review `README.md` for detailed setup
3. Test individual modules with `backend/test_modules.py`
4. Check logs in terminal for error messages

---

## ✅ Quick Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (no errors)
- [ ] API keys configured in `.env`
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Browser opened to localhost:3000
- [ ] Microphone permission granted
- [ ] First recording successful

---

**Time to first recording: 5 minutes** ⏱️

**You're all set! Start your wellness journey! 🎉**

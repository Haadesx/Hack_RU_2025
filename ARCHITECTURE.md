# 🏗️ BioWhisper Architecture

## System Overview

BioWhisper is a multi-modal wellness analysis platform that combines voice stress detection, wearable biometric data, and posture assessment to generate personalized health insights using AI.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Welcome  │  │Recording │  │Dashboard │  │ Settings │  │
│  │  Screen  │  │   View   │  │  & Play  │  │   Modal  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                             │
│            React 18 + Vite + Tailwind CSS                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTP REST API
                      │ WebSocket (optional)
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  API ENDPOINTS                        │  │
│  │  /record | /wearable/upload | /camera-scan          │  │
│  │  /analyze | /audio/{file} | /generate-hypnosis      │  │
│  └──────────────────────────────────────────────────────┘  │
│                      ↓                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              PROCESSING MODULES                       │  │
│  │                                                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │    Audio     │  │     HRV      │  │   Pose     │ │  │
│  │  │  Analysis    │  │  Analysis    │  │  Analysis  │ │  │
│  │  │  (librosa)   │  │  (pandas)    │  │(MediaPipe) │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  │                                                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │   Prompt     │  │    Gemini    │  │    TTS     │ │  │
│  │  │   Builder    │  │    Client    │  │  (Eleven)  │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│              Python 3.9+ | Uvicorn ASGI Server             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ External API Calls
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │   Gemini     │  │  ElevenLabs  │  │   MediaPipe      │ │
│  │  (Google)    │  │     TTS      │  │  (Local/Cloud)   │ │
│  │              │  │              │  │                  │ │
│  │  AI Insights │  │  Voice Gen   │  │  Pose Detection  │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Voice Check-in Flow

```
User speaks → WebAudio API → Blob → FormData
                                      ↓
                              POST /record
                                      ↓
                            Save to uploads/
                                      ↓
                            Audio Analysis
                              (librosa)
                                      ↓
                     Extract: stress, pitch, energy
                                      ↓
                         Return features to frontend
```

### 2. Full Analysis Flow

```
Audio filename + Optional (Wearable CSV, Pose JSON)
                    ↓
            POST /analyze endpoint
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
Audio Analysis  HRV Analysis  Pose Analysis
    ↓               ↓               ↓
    └───────────────┼───────────────┘
                    ↓
          Build Gemini Prompt
                    ↓
            Call Gemini API
                    ↓
    Parse JSON Response (narrative, actions, etc.)
                    ↓
        Generate TTS Audio (ElevenLabs)
                    ↓
    Return complete analysis + audio filenames
                    ↓
        Frontend displays results
```

### 3. Audio Playback Flow

```
User clicks play → GET /audio/{filename}
                          ↓
                   Stream audio file
                          ↓
                   Browser audio player
```

---

## Module Architecture

### Backend Modules

#### 1. **app.py** (Main Application)
- FastAPI application instance
- Route definitions
- CORS middleware
- Error handling
- File uploads

#### 2. **audio_analysis.py**
- **Input**: Audio file path
- **Processing**:
  - Load audio with librosa
  - Extract RMS, tempo, pitch, spectral features
  - Calculate stress score (0-1)
  - Classify emotional tone
- **Output**: Dict with features

#### 3. **hrv_analysis.py**
- **Input**: CSV with HR, HRV, sleep data
- **Processing**:
  - Parse CSV with pandas
  - Calculate HRV metrics (RMSSD, std)
  - Analyze sleep stages
  - Compute circadian alignment
  - Generate wellness score
- **Output**: Dict with summary

#### 4. **pose_analysis.py**
- **Input**: JSON with pose keypoints
- **Processing**:
  - Analyze shoulder alignment
  - Check forward head posture
  - Detect slouching
  - Calculate alignment score
- **Output**: Dict with recommendations

#### 5. **prompt_builder.py**
- **Input**: Audio, wearable, pose data
- **Processing**:
  - Format data into structured prompt
  - Add context (time of day, etc.)
  - Include instructions for JSON output
- **Output**: String prompt for Gemini

#### 6. **gemini_client.py**
- **Input**: Prompt string
- **Processing**:
  - Call Gemini API (async)
  - Parse JSON response
  - Handle errors with fallback
- **Output**: Dict with narrative, actions, etc.

#### 7. **tts.py**
- **Input**: Text to speak
- **Processing**:
  - Call ElevenLabs API
  - Save audio to file
  - Fallback to gTTS if needed
- **Output**: File path

---

## Frontend Architecture

### Component Hierarchy

```
App.jsx
├── Welcome.jsx
│   └── (Feature cards, consent modal)
├── RecordingView.jsx
│   └── (WebAudio recording, waveform viz)
└── Dashboard.jsx
    ├── AudioPlayer.jsx
    ├── ActionItems.jsx
    └── WearableUpload.jsx
```

### State Management

**App-level state** (useState):
- `currentView`: 'welcome' | 'recording' | 'dashboard'
- `analysisData`: Full analysis results
- `audioFilename`: Recorded audio file

**Component-level state**:
- Recording: `isRecording`, `countdown`, `error`
- Dashboard: `isLoading`, `wearableFilename`
- AudioPlayer: `isPlaying`, `currentTime`, `duration`

### API Integration

**Axios** for HTTP requests:
- POST `/record`: Upload audio
- POST `/wearable/upload`: Upload CSV
- POST `/analyze`: Run full pipeline
- GET `/audio/{filename}`: Stream audio

---

## Key Design Decisions

### 1. Why FastAPI?
- **Performance**: 2-3x faster than Flask
- **Type safety**: Pydantic models
- **Auto docs**: Swagger UI built-in
- **Async support**: For Gemini API calls

### 2. Why Vite over CRA?
- **Speed**: Sub-second HMR
- **Modern**: ES modules native
- **Smaller bundle**: Better tree-shaking

### 3. Why Tailwind?
- **Rapid prototyping**: Utility classes
- **Consistency**: Design system built-in
- **Performance**: PurgeCSS removes unused styles

### 4. Why Gemini?
- **Context awareness**: Better understanding of health data
- **JSON mode**: Structured outputs
- **Safety**: Built-in medical disclaimer awareness

### 5. Why ElevenLabs?
- **Quality**: Near-human voice synthesis
- **Emotion**: Can convey empathy
- **Flexibility**: Multiple voices, languages

---

## Scalability Considerations

### Current (Hackathon MVP)

- **Storage**: Local filesystem
- **Concurrency**: Single-threaded
- **Auth**: None
- **Database**: None

### Production-Ready Enhancements

1. **Storage**
   - S3/GCS for audio files
   - PostgreSQL for user data
   - Redis for session cache

2. **Concurrency**
   - Celery for background tasks
   - WebSockets for real-time updates
   - Load balancer (Nginx)

3. **Authentication**
   - JWT tokens
   - OAuth2 (Google, Apple)
   - Role-based access

4. **Monitoring**
   - Prometheus metrics
   - Sentry error tracking
   - CloudWatch logs

5. **ML Enhancements**
   - Custom emotion detection model
   - Fine-tuned Gemini prompts
   - Real-time HRV stream processing

---

## Security Architecture

### Current Measures

1. **CORS**: Restricted origins
2. **File validation**: Type checking on uploads
3. **Environment variables**: API keys not hardcoded
4. **No persistent storage**: Privacy by default

### Production Enhancements

1. **Encryption**: TLS 1.3 for all traffic
2. **Authentication**: JWT with refresh tokens
3. **Rate limiting**: Prevent API abuse
4. **Input sanitization**: Validate all user inputs
5. **HIPAA compliance**: If handling medical data

---

## API Contract

### POST /record

**Request**:
```
FormData: { file: Audio blob }
```

**Response**:
```json
{
  "ok": true,
  "filename": "recording_123.webm",
  "features": { "stress_score": 0.65, ... }
}
```

### POST /analyze

**Request**:
```
FormData: {
  audio_filename: "recording_123.webm",
  wearable_filename: "data.csv" (optional),
  pose_keypoints_json: "{...}" (optional)
}
```

**Response**:
```json
{
  "ok": true,
  "narrative": "Your body is...",
  "observations": ["Finding 1", "Finding 2"],
  "action_items": [
    {
      "priority": 1,
      "title": "Breathing reset",
      "description": "...",
      "estimated_time": "3 minutes",
      "impact": "Immediate calm"
    }
  ],
  "audio_features": { ... },
  "wearable_summary": { ... },
  "tts_filename": "tts_narrative.mp3",
  "breathing_filename": "breathing.mp3"
}
```

---

## Performance Targets

### Latency

- Audio upload: < 1s
- Audio analysis: < 3s
- Gemini API call: < 5s
- TTS generation: < 8s
- **Total pipeline**: < 15s

### Throughput

- Concurrent users: 100+ (with proper scaling)
- Requests per second: 50+ (FastAPI capability)

---

## Future Architecture Enhancements

### Phase 2: Real-time Processing

```
Wearable Device (BLE/WiFi)
        ↓
    WebSocket
        ↓
   FastAPI Server
        ↓
   Real-time Stream Processing
        ↓
   Live Dashboard Updates
```

### Phase 3: Mobile App

```
React Native App
        ↓
    GraphQL API
        ↓
   Apollo Server
        ↓
  Existing Backend
```

### Phase 4: ML Pipeline

```
User Data → Feature Extraction → Custom ML Models
                                        ↓
                                  Model Training
                                        ↓
                              Inference at Edge
```

---

## Tech Stack Summary

| Layer | Technology | Justification |
|-------|-----------|---------------|
| Frontend | React 18 | Component reusability, ecosystem |
| Build Tool | Vite | Speed, modern ES modules |
| Styling | Tailwind CSS | Rapid prototyping, consistency |
| Backend | FastAPI | Performance, async, type safety |
| Server | Uvicorn | ASGI, async support |
| Audio | Librosa | Industry-standard audio analysis |
| Pose | MediaPipe | Google's production-ready pose detection |
| AI | Gemini | Contextual understanding, JSON mode |
| TTS | ElevenLabs | Human-like voice quality |
| Data | Pandas/NumPy | Data processing standard |

---

## Deployment Architecture (Production)

```
        ┌───────────┐
        │  Cloudflare │  (CDN + DDoS protection)
        └─────┬─────┘
              ↓
        ┌───────────┐
        │   Vercel   │  (Frontend hosting)
        └─────┬─────┘
              ↓
        ┌───────────┐
        │  AWS ALB   │  (Load balancer)
        └─────┬─────┘
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
┌──────────┐      ┌──────────┐
│ EC2 / ECS│      │ EC2 / ECS│  (Backend containers)
└─────┬────┘      └─────┬────┘
      ↓                 ↓
┌─────────────────────────┐
│        RDS / Aurora      │  (Database)
└─────────────────────────┘
      ↓                 ↓
┌──────────┐      ┌──────────┐
│    S3     │      │  Redis   │  (Storage & Cache)
└──────────┘      └──────────┘
```

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-04  
**Maintained By**: BioWhisper Team

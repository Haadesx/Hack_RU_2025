import React, { useState, useEffect } from 'react'
import { Heart, Mic, Camera, Upload, Play, Pause, RotateCcw } from 'lucide-react'
import RecordingInterface from './components/RecordingInterface'
import WearableUpload from './components/WearableUpload'
import CameraCapture from './components/CameraCapture'
import AnalysisResults from './components/AnalysisResults'
import LoadingSpinner from './components/LoadingSpinner'

const API_BASE = '/api'

function App() {
  const [currentStep, setCurrentStep] = useState('welcome')
  const [sessionData, setSessionData] = useState({
    audioFilename: null,
    wearableFilename: null,
    poseData: null,
    analysisResult: null,
    error: null
  })
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  // Auto-cleanup function for old files
  useEffect(() => {
    const cleanup = () => {
      // This could call a cleanup endpoint if needed
      console.log('Session cleanup')
    }
    
    window.addEventListener('beforeunload', cleanup)
    return () => window.removeEventListener('beforeunload', cleanup)
  }, [])

  const handleAudioRecorded = (filename) => {
    setSessionData(prev => ({ ...prev, audioFilename: filename }))
    setCurrentStep('wearable')
  }

  const handleWearableUploaded = (filename) => {
    setSessionData(prev => ({ ...prev, wearableFilename: filename }))
    setCurrentStep('camera')
  }

  const handlePoseCapture = (poseData) => {
    setSessionData(prev => ({ ...prev, poseData }))
    setCurrentStep('analyze')
  }

  const handleSkipWearable = () => {
    setCurrentStep('camera')
  }

  const handleSkipCamera = () => {
    setCurrentStep('analyze')
  }

  const performAnalysis = async () => {
    if (!sessionData.audioFilename) {
      setSessionData(prev => ({ ...prev, error: 'Audio recording required for analysis' }))
      return
    }

    setIsAnalyzing(true)
    setSessionData(prev => ({ ...prev, error: null }))

    try {
      const formData = new FormData()
      formData.append('audio_filename', sessionData.audioFilename)
      
      if (sessionData.wearableFilename) {
        formData.append('wearable_filename', sessionData.wearableFilename)
      }
      
      if (sessionData.poseData) {
        formData.append('pose_data', JSON.stringify(sessionData.poseData))
      }

      const response = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.status} ${response.statusText}`)
      }

      const result = await response.json()
      setSessionData(prev => ({ ...prev, analysisResult: result }))
      setCurrentStep('results')
      
    } catch (error) {
      console.error('Analysis error:', error)
      setSessionData(prev => ({ 
        ...prev, 
        error: error.message || 'Analysis failed. Please try again.' 
      }))
    } finally {
      setIsAnalyzing(false)
    }
  }

  const resetSession = () => {
    setCurrentStep('welcome')
    setSessionData({
      audioFilename: null,
      wearableFilename: null,
      poseData: null,
      analysisResult: null,
      error: null
    })
  }

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 'welcome':
        return (
          <WelcomeScreen onStartRecording={() => setCurrentStep('recording')} />
        )
      
      case 'recording':
        return (
          <RecordingInterface 
            onRecordingComplete={handleAudioRecorded}
            onBack={() => setCurrentStep('welcome')}
          />
        )
      
      case 'wearable':
        return (
          <WearableUpload
            onUploadComplete={handleWearableUploaded}
            onSkip={handleSkipWearable}
            onBack={() => setCurrentStep('recording')}
          />
        )
      
      case 'camera':
        return (
          <CameraCapture
            onCaptureComplete={handlePoseCapture}
            onSkip={handleSkipCamera}
            onBack={() => setCurrentStep('wearable')}
          />
        )
      
      case 'analyze':
        return (
          <AnalysisStep
            sessionData={sessionData}
            isAnalyzing={isAnalyzing}
            onAnalyze={performAnalysis}
            onBack={() => setCurrentStep('camera')}
            error={sessionData.error}
          />
        )
      
      case 'results':
        return (
          <AnalysisResults
            result={sessionData.analysisResult}
            onReset={resetSession}
          />
        )
      
      default:
        return <WelcomeScreen onStartRecording={() => setCurrentStep('recording')} />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200/50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Heart className="w-8 h-8 text-wellness-600" />
            <h1 className="text-2xl font-bold text-gray-900">BioWhisper</h1>
          </div>
          <div className="text-sm text-gray-600">
            Your compassionate wellness assistant
          </div>
        </div>
      </header>

      {/* Progress indicator */}
      {currentStep !== 'welcome' && currentStep !== 'results' && (
        <ProgressIndicator currentStep={currentStep} />
      )}

      {/* Main content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {renderCurrentStep()}
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 text-center text-sm text-gray-500">
        <p>BioWhisper keeps your data private and secure. No information is stored permanently.</p>
      </footer>
    </div>
  )
}

const WelcomeScreen = ({ onStartRecording }) => (
  <div className="text-center max-w-2xl mx-auto">
    <div className="mb-8">
      <Heart className="w-16 h-16 text-wellness-600 mx-auto mb-4 animate-pulse-slow" />
      <h2 className="text-4xl font-bold text-gray-900 mb-4">
        Welcome to BioWhisper
      </h2>
      <p className="text-xl text-gray-600 leading-relaxed">
        Your compassionate AI wellness companion. Share how you're feeling through voice, 
        posture, and biometric data to receive personalized wellness insights and guidance.
      </p>
    </div>

    <div className="glass-card mb-8">
      <h3 className="text-lg font-semibold mb-4">What we'll analyze:</h3>
      <div className="grid md:grid-cols-3 gap-6 text-sm">
        <div className="flex flex-col items-center">
          <Mic className="w-8 h-8 text-primary-600 mb-2" />
          <div className="font-medium">Voice Analysis</div>
          <div className="text-gray-600">Stress, emotion, energy levels</div>
        </div>
        <div className="flex flex-col items-center">
          <Upload className="w-8 h-8 text-primary-600 mb-2" />
          <div className="font-medium">Biometric Data</div>
          <div className="text-gray-600">HRV, sleep, heart rate (optional)</div>
        </div>
        <div className="flex flex-col items-center">
          <Camera className="w-8 h-8 text-primary-600 mb-2" />
          <div className="font-medium">Posture Scan</div>
          <div className="text-gray-600">Body alignment, tension (optional)</div>
        </div>
      </div>
    </div>

    <button
      onClick={onStartRecording}
      className="btn-wellness text-lg py-4 px-8 animate-breathe"
    >
      <Mic className="w-6 h-6 mr-3" />
      Start 10-Second Check-in
    </button>

    <div className="mt-6 text-sm text-gray-500">
      <p>🔒 All data stays private • 🎯 Personalized insights • 🌱 Compassionate guidance</p>
    </div>
  </div>
)

const ProgressIndicator = ({ currentStep }) => {
  const steps = [
    { id: 'recording', label: 'Voice', icon: Mic },
    { id: 'wearable', label: 'Biometrics', icon: Upload },
    { id: 'camera', label: 'Posture', icon: Camera },
    { id: 'analyze', label: 'Analysis', icon: Heart }
  ]

  const currentIndex = steps.findIndex(step => step.id === currentStep)

  return (
    <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200/50">
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => {
            const Icon = step.icon
            const isActive = index === currentIndex
            const isCompleted = index < currentIndex
            
            return (
              <div
                key={step.id}
                className={`flex items-center ${index < steps.length - 1 ? 'flex-1' : ''}`}
              >
                <div className={`
                  flex items-center justify-center w-10 h-10 rounded-full border-2 transition-colors
                  ${isActive ? 'border-primary-600 bg-primary-600 text-white' : 
                    isCompleted ? 'border-wellness-600 bg-wellness-600 text-white' : 
                    'border-gray-300 bg-gray-100 text-gray-400'}
                `}>
                  <Icon className="w-5 h-5" />
                </div>
                <span className={`ml-2 text-sm font-medium ${
                  isActive || isCompleted ? 'text-gray-900' : 'text-gray-500'
                }`}>
                  {step.label}
                </span>
                {index < steps.length - 1 && (
                  <div className={`flex-1 h-0.5 mx-4 ${
                    isCompleted ? 'bg-wellness-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

const AnalysisStep = ({ sessionData, isAnalyzing, onAnalyze, onBack, error }) => (
  <div className="max-w-2xl mx-auto text-center">
    <h2 className="text-3xl font-bold mb-6">Ready for Analysis</h2>
    
    <div className="glass-card mb-8">
      <h3 className="text-lg font-semibold mb-4">Data Collected:</h3>
      <div className="space-y-3 text-left">
        <div className="flex items-center justify-between">
          <span className="flex items-center">
            <Mic className="w-5 h-5 mr-2 text-wellness-600" />
            Voice Recording
          </span>
          <span className="text-wellness-600">✓ Complete</span>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="flex items-center">
            <Upload className="w-5 h-5 mr-2" />
            Biometric Data
          </span>
          <span className={sessionData.wearableFilename ? 'text-wellness-600' : 'text-gray-400'}>
            {sessionData.wearableFilename ? '✓ Uploaded' : '○ Skipped'}
          </span>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="flex items-center">
            <Camera className="w-5 h-5 mr-2" />
            Posture Scan
          </span>
          <span className={sessionData.poseData ? 'text-wellness-600' : 'text-gray-400'}>
            {sessionData.poseData ? '✓ Captured' : '○ Skipped'}
          </span>
        </div>
      </div>
    </div>

    {error && (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
        {error}
      </div>
    )}

    <div className="flex gap-4 justify-center">
      <button onClick={onBack} className="btn-secondary">
        Back
      </button>
      <button
        onClick={onAnalyze}
        disabled={isAnalyzing}
        className="btn-wellness flex items-center"
      >
        {isAnalyzing ? (
          <>
            <LoadingSpinner className="w-5 h-5 mr-2" />
            Analyzing...
          </>
        ) : (
          <>
            <Heart className="w-5 h-5 mr-2" />
            Generate Wellness Insights
          </>
        )}
      </button>
    </div>

    <div className="mt-6 text-sm text-gray-500">
      <p>This may take 30-60 seconds as we analyze your data and generate personalized insights.</p>
    </div>
  </div>
)

export default App
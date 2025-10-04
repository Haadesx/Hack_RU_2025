import { useState } from 'react'
import Welcome from './components/Welcome'
import RecordingView from './components/RecordingView'
import Dashboard from './components/Dashboard'
import './styles/index.css'

function App() {
  const [currentView, setCurrentView] = useState('welcome') // welcome, recording, dashboard
  const [analysisData, setAnalysisData] = useState(null)
  const [audioFilename, setAudioFilename] = useState(null)

  const handleStartRecording = () => {
    setCurrentView('recording')
  }

  const handleRecordingComplete = (filename) => {
    setAudioFilename(filename)
    // Auto-trigger analysis after recording
    setTimeout(() => {
      handleAnalyze(filename)
    }, 500)
  }

  const handleAnalyze = async (filename) => {
    setCurrentView('dashboard')
    // Analysis will be triggered in Dashboard component
  }

  const handleRestart = () => {
    setCurrentView('welcome')
    setAnalysisData(null)
    setAudioFilename(null)
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white text-xl font-bold">B</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  BioWhisper
                </h1>
                <p className="text-xs text-gray-500">Your Personal Wellness Assistant</p>
              </div>
            </div>
            
            {currentView !== 'welcome' && (
              <button
                onClick={handleRestart}
                className="px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              >
                New Check-in
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === 'welcome' && (
          <Welcome onStart={handleStartRecording} />
        )}
        
        {currentView === 'recording' && (
          <RecordingView
            onComplete={handleRecordingComplete}
            onCancel={() => setCurrentView('welcome')}
          />
        )}
        
        {currentView === 'dashboard' && (
          <Dashboard
            audioFilename={audioFilename}
            onRestart={handleRestart}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="mt-16 pb-8 text-center text-sm text-gray-500">
        <p>
          BioWhisper • Built for HackerTron 2025 • 
          <span className="text-blue-600"> Privacy-First Wellness</span>
        </p>
        <p className="mt-2 text-xs">
          Not a medical device. For wellness optimization only.
        </p>
      </footer>
    </div>
  )
}

export default App

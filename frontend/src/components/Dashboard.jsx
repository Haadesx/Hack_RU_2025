import { useState, useEffect } from 'react'
import { FaPlay, FaPause, FaDownload, FaSpinner, FaHeart, FaBrain, FaRunning } from 'react-icons/fa'
import axios from 'axios'
import AudioPlayer from './AudioPlayer'
import ActionItems from './ActionItems'
import WearableUpload from './WearableUpload'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Dashboard({ audioFilename, onRestart }) {
  const [analysisData, setAnalysisData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [wearableFilename, setWearableFilename] = useState(null)

  useEffect(() => {
    if (audioFilename) {
      performAnalysis()
    }
  }, [audioFilename, wearableFilename])

  const performAnalysis = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('audio_filename', audioFilename)
      
      if (wearableFilename) {
        formData.append('wearable_filename', wearableFilename)
      }

      const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      if (response.data.ok) {
        setAnalysisData(response.data)
      } else {
        throw new Error('Analysis failed')
      }
    } catch (err) {
      console.error('Analysis error:', err)
      setError('Failed to analyze data. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleWearableUpload = (filename) => {
    setWearableFilename(filename)
  }

  if (isLoading) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card text-center py-12">
          <div className="spinner mx-auto mb-4"></div>
          <h3 className="text-xl font-semibold mb-2">Analyzing Your Wellness Data</h3>
          <p className="text-gray-600">
            Processing voice patterns, physiological signals, and generating personalized insights...
          </p>
          <div className="mt-6 flex justify-center space-x-4 text-sm text-gray-500">
            <span>✓ Voice analysis</span>
            <span>✓ Stress detection</span>
            <span>✓ AI insights</span>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card border-2 border-red-200">
          <div className="text-center">
            <div className="text-red-500 text-5xl mb-4">⚠️</div>
            <h3 className="text-xl font-semibold mb-2">Analysis Error</h3>
            <p className="text-gray-600 mb-6">{error}</p>
            <button onClick={onRestart} className="btn-primary">
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!analysisData) {
    return null
  }

  const { narrative, observations, action_items, audio_features, wearable_summary, tts_filename, breathing_filename } = analysisData

  // Calculate wellness status color
  const stressScore = audio_features?.stress_score || 0.5
  const getStatusColor = (score) => {
    if (score < 0.35) return 'text-green-600 bg-green-50 border-green-200'
    if (score < 0.65) return 'text-yellow-600 bg-yellow-50 border-yellow-200'
    return 'text-red-600 bg-red-50 border-red-200'
  }

  const getStatusLabel = (score) => {
    if (score < 0.35) return 'Calm'
    if (score < 0.65) return 'Moderate'
    return 'Elevated Stress'
  }

  return (
    <div className="space-y-6">
      {/* Status Header */}
      <div className="card bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Your Wellness Summary</h2>
            <p className="text-gray-600">Based on voice, physiological, and posture analysis</p>
          </div>
          <div className={`px-6 py-3 rounded-full border-2 font-semibold ${getStatusColor(stressScore)}`}>
            {getStatusLabel(stressScore)}
          </div>
        </div>
      </div>

      {/* Main Metrics Grid */}
      <div className="grid md:grid-cols-3 gap-6">
        {/* Voice Analysis */}
        <div className="card hover:shadow-xl transition-shadow">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <FaBrain className="text-blue-600 text-xl" />
            </div>
            <h3 className="font-semibold text-lg">Voice Analysis</h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Stress Level:</span>
              <span className="font-semibold">{Math.round(stressScore * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${stressScore < 0.35 ? 'bg-green-500' : stressScore < 0.65 ? 'bg-yellow-500' : 'bg-red-500'}`}
                style={{ width: `${stressScore * 100}%` }}
              />
            </div>
            <div className="mt-3 text-sm">
              <p className="text-gray-600">Emotional Tone:</p>
              <p className="font-medium capitalize">{audio_features?.emotional_tone || 'N/A'}</p>
            </div>
          </div>
        </div>

        {/* HRV / Wearable Data */}
        <div className="card hover:shadow-xl transition-shadow">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
              <FaHeart className="text-purple-600 text-xl" />
            </div>
            <h3 className="font-semibold text-lg">Physiological</h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">HRV (RMSSD):</span>
              <span className="font-semibold">{wearable_summary?.hrv_rmssd?.toFixed(1) || 'N/A'} ms</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Avg HR:</span>
              <span className="font-semibold">{wearable_summary?.avg_hr || 'N/A'} bpm</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Sleep:</span>
              <span className="font-semibold">{wearable_summary?.total_sleep_hours?.toFixed(1) || 'N/A'} hrs</span>
            </div>
          </div>
          {wearable_summary?.note && (
            <p className="mt-3 text-xs text-gray-500 italic">{wearable_summary.note}</p>
          )}
        </div>

        {/* Wellness Score */}
        <div className="card hover:shadow-xl transition-shadow">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <FaRunning className="text-green-600 text-xl" />
            </div>
            <h3 className="font-semibold text-lg">Wellness Score</h3>
          </div>
          <div className="text-center">
            <div className="text-5xl font-bold text-blue-600 mb-2">
              {wearable_summary?.wellness_score?.toFixed(0) || '68'}
            </div>
            <p className="text-gray-600 text-sm">Out of 100</p>
            <div className="mt-4 text-xs text-gray-500">
              Based on HRV, sleep, and stress indicators
            </div>
          </div>
        </div>
      </div>

      {/* Narrative Section */}
      {narrative && (
        <div className="card bg-gradient-to-br from-blue-50 to-white">
          <h3 className="text-xl font-semibold mb-4">Your Body's Story</h3>
          <div className="prose prose-blue max-w-none">
            <p className="text-gray-700 leading-relaxed whitespace-pre-line">{narrative}</p>
          </div>
        </div>
      )}

      {/* Observations */}
      {observations && observations.length > 0 && (
        <div className="card">
          <h3 className="text-xl font-semibold mb-4">Key Observations</h3>
          <ul className="space-y-2">
            {observations.map((obs, idx) => (
              <li key={idx} className="flex items-start space-x-3">
                <span className="text-blue-600 text-xl">•</span>
                <span className="text-gray-700">{obs}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Action Items */}
      {action_items && <ActionItems items={action_items} />}

      {/* Audio Players */}
      <div className="grid md:grid-cols-2 gap-6">
        {tts_filename && (
          <AudioPlayer
            title="Your Wellness Narrative"
            filename={tts_filename}
            icon="🎧"
            description="Listen to your personalized wellness summary"
          />
        )}
        
        {breathing_filename && (
          <AudioPlayer
            title="Guided Breathing Exercise"
            filename={breathing_filename}
            icon="🧘"
            description="3-minute calming breathwork"
          />
        )}
      </div>

      {/* Wearable Upload (if not already uploaded) */}
      {!wearableFilename && (
        <WearableUpload onUpload={handleWearableUpload} />
      )}

      {/* Actions */}
      <div className="flex justify-center space-x-4">
        <button onClick={onRestart} className="btn-primary">
          New Check-in
        </button>
        <button
          onClick={() => window.print()}
          className="btn-secondary"
        >
          <FaDownload className="inline mr-2" />
          Export Report
        </button>
      </div>
    </div>
  )
}

export default Dashboard

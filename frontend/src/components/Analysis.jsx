import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Play, Pause, Download, Heart, Brain, Activity, RefreshCw } from 'lucide-react'
import { useWellness } from '../context/WellnessContext'
import AudioPlayer from './AudioPlayer'

function Analysis() {
  const navigate = useNavigate()
  const { state, dispatch, setInsights, setLoading, setError } = useWellness()
  
  const [isPlayingNarration, setIsPlayingNarration] = useState(false)
  const [isPlayingBreathing, setIsPlayingBreathing] = useState(false)
  
  useEffect(() => {
    if (!state.audioFeatures) {
      navigate('/record')
      return
    }
    
    // Auto-run analysis if we have audio features but no insights
    if (state.audioFeatures && !state.insights) {
      runAnalysis()
    }
  }, [state.audioFeatures, state.insights, navigate])
  
  const runAnalysis = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('audio_filename', state.audioFilename)
      
      // Add wearable data if available
      if (state.wearableData) {
        formData.append('wearable_filename', state.wearableData.filename)
      }
      
      // Add pose data if available
      if (state.poseData) {
        formData.append('pose_keypoints', JSON.stringify(state.poseData))
      }
      
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error('Analysis failed')
      }
      
      const result = await response.json()
      
      if (result.ok) {
        setInsights(result.insights, result.audio_urls)
      } else {
        throw new Error('Analysis failed')
      }
      
    } catch (error) {
      console.error('Analysis error:', error)
      setError('Failed to analyze your data. Please try again.')
    } finally {
      setLoading(false)
    }
  }
  
  const getStressLevel = () => {
    if (!state.audioFeatures) return 'Unknown'
    const stress = state.audioFeatures.stress_score
    if (stress < 0.3) return 'Low'
    if (stress < 0.7) return 'Moderate'
    return 'High'
  }
  
  const getStressColor = () => {
    const stress = state.audioFeatures?.stress_score || 0.5
    if (stress < 0.3) return 'text-green-600 bg-green-100'
    if (stress < 0.7) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }
  
  const getEnergyLevel = () => {
    if (!state.audioFeatures) return 'Unknown'
    const energy = state.audioFeatures.energy
    if (energy < 0.3) return 'Low'
    if (energy < 0.7) return 'Moderate'
    return 'High'
  }
  
  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={() => navigate('/record')}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back</span>
        </button>
        
        <h1 className="text-2xl font-bold text-gray-900">Wellness Analysis</h1>
        
        <button
          onClick={runAnalysis}
          disabled={state.isLoading}
          className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 transition-colors"
        >
          <RefreshCw className={`w-5 h-5 ${state.isLoading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>
      
      {/* Loading State */}
      {state.isLoading && (
        <div className="card text-center py-12">
          <div className="loading-dots mx-auto mb-4">
            <div></div>
            <div></div>
            <div></div>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Analyzing Your Wellness</h3>
          <p className="text-gray-600">
            Processing your voice, biometrics, and posture data...
          </p>
        </div>
      )}
      
      {/* Error State */}
      {state.error && (
        <div className="card bg-red-50 border-red-200 mb-6">
          <p className="text-red-700">{state.error}</p>
        </div>
      )}
      
      {/* Analysis Results */}
      {state.insights && !state.isLoading && (
        <>
          {/* Key Metrics */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="card text-center">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="w-8 h-8 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Stress Level</h3>
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStressColor()}`}>
                {getStressLevel()}
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Score: {(state.audioFeatures?.stress_score * 100 || 0).toFixed(0)}%
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Activity className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Energy Level</h3>
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-600">
                {getEnergyLevel()}
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Score: {(state.audioFeatures?.energy * 100 || 0).toFixed(0)}%
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Speaking Rate</h3>
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-600">
                {(state.audioFeatures?.speaking_rate || 0).toFixed(1)} wps
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Words per second
              </p>
            </div>
          </div>
          
          {/* AI Insights */}
          <div className="card mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Personalized Insights</h2>
            <div className="prose max-w-none">
              <p className="text-gray-700 leading-relaxed mb-6">
                {state.insights.narrative}
              </p>
            </div>
          </div>
          
          {/* Observations */}
          <div className="card mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Observations</h3>
            <ul className="space-y-3">
              {state.insights.observations?.map((observation, index) => (
                <li key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                  <p className="text-gray-700">{observation}</p>
                </li>
              ))}
            </ul>
          </div>
          
          {/* Action Items */}
          <div className="card mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended Actions</h3>
            <div className="space-y-4">
              {state.insights.action_items?.map((action, index) => (
                <div key={index} className="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
                  <div className="w-6 h-6 bg-primary-500 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                    {index + 1}
                  </div>
                  <p className="text-gray-700">{action}</p>
                </div>
              ))}
            </div>
          </div>
          
          {/* Audio Players */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Narration</h3>
              <AudioPlayer
                url={state.audioUrls?.narration}
                title="Listen to your personalized wellness insights"
                onPlay={() => setIsPlayingNarration(true)}
                onPause={() => setIsPlayingNarration(false)}
              />
            </div>
            
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Breathing Exercise</h3>
              <AudioPlayer
                url={state.audioUrls?.breathing}
                title="3-minute guided breathing exercise"
                onPlay={() => setIsPlayingBreathing(true)}
                onPause={() => setIsPlayingBreathing(false)}
              />
            </div>
          </div>
          
          {/* Action Buttons */}
          <div className="flex justify-between">
            <button
              onClick={() => navigate('/record')}
              className="btn-secondary"
            >
              New Check-in
            </button>
            
            <button
              onClick={() => navigate('/dashboard')}
              className="btn-primary flex items-center space-x-2"
            >
              <span>View Dashboard</span>
              <ArrowLeft className="w-4 h-4 rotate-180" />
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default Analysis
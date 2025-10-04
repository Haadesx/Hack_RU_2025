import React, { useState, useRef } from 'react'
import { Play, Pause, Download, RotateCcw, Heart, Mic, Camera, Upload, TrendingUp, Clock, User, Moon } from 'lucide-react'
import { Howl } from 'howler'
import LoadingSpinner from './LoadingSpinner'

const API_BASE = '/api'

const AnalysisResults = ({ result, onReset }) => {
  const [currentAudio, setCurrentAudio] = useState(null)
  const [playingAudio, setPlayingAudio] = useState(null)
  const [generatingHypnosis, setGeneratingHypnosis] = useState(false)
  const [hypnosisAudio, setHypnosisAudio] = useState(null)
  
  const audioRefs = useRef({})

  const playAudio = (audioType, url) => {
    // Stop any currently playing audio
    if (currentAudio) {
      currentAudio.stop()
    }

    // Create new Howl instance
    const sound = new Howl({
      src: [url],
      html5: true,
      onplay: () => setPlayingAudio(audioType),
      onend: () => setPlayingAudio(null),
      onerror: (id, error) => {
        console.error('Audio playback error:', error)
        setPlayingAudio(null)
      }
    })

    sound.play()
    setCurrentAudio(sound)
    audioRefs.current[audioType] = sound
  }

  const pauseAudio = () => {
    if (currentAudio) {
      currentAudio.pause()
      setPlayingAudio(null)
    }
  }

  const generateSleepHypnosis = async () => {
    setGeneratingHypnosis(true)
    try {
      const response = await fetch(`${API_BASE}/generate-sleep-hypnosis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          duration_minutes: 10,
          focus_area: 'general relaxation'
        })
      })

      if (!response.ok) {
        throw new Error('Failed to generate sleep hypnosis')
      }

      const hypnosisResult = await response.json()
      setHypnosisAudio(hypnosisResult)
      
    } catch (error) {
      console.error('Error generating sleep hypnosis:', error)
      alert('Failed to generate sleep hypnosis. Please try again.')
    } finally {
      setGeneratingHypnosis(false)
    }
  }

  if (!result) {
    return (
      <div className="text-center py-12">
        <LoadingSpinner className="w-12 h-12 mx-auto mb-4" />
        <div className="text-gray-600">Loading your wellness insights...</div>
      </div>
    )
  }

  const stressLevel = result.analysis_data?.audio_features?.stress_score || 0.5
  const postureScore = result.analysis_data?.pose_summary?.posture_score || 0.7
  const recoveryScore = result.analysis_data?.wearable_summary?.recovery_score || 0.7

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <Heart className="w-12 h-12 text-wellness-600 mx-auto mb-4" />
        <h2 className="text-3xl font-bold mb-2">Your Wellness Insights</h2>
        <p className="text-gray-600">
          Based on your voice, biometrics, and posture analysis
        </p>
      </div>

      {/* Main narrative */}
      <div className="glass-card mb-8">
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <Heart className="w-6 h-6 mr-2 text-wellness-600" />
          Personal Wellness Summary
        </h3>
        <div className="prose prose-lg text-gray-700 leading-relaxed">
          {result.narrative?.split('\n').map((paragraph, index) => (
            <p key={index} className="mb-4 last:mb-0">{paragraph}</p>
          ))}
        </div>
      </div>

      {/* Quick metrics */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="glass-card text-center">
          <Mic className="w-8 h-8 text-blue-500 mx-auto mb-3" />
          <div className="text-2xl font-bold mb-1">
            {(100 - stressLevel * 100).toFixed(0)}%
          </div>
          <div className="text-sm text-gray-600">Voice Calm Score</div>
          <div className={`text-xs mt-1 ${
            stressLevel < 0.3 ? 'text-wellness-600' : 
            stressLevel < 0.7 ? 'text-yellow-600' : 'text-red-600'
          }`}>
            {stressLevel < 0.3 ? 'Relaxed' : stressLevel < 0.7 ? 'Moderate' : 'Elevated'}
          </div>
        </div>

        <div className="glass-card text-center">
          <User className="w-8 h-8 text-purple-500 mx-auto mb-3" />
          <div className="text-2xl font-bold mb-1">
            {(postureScore * 100).toFixed(0)}%
          </div>
          <div className="text-sm text-gray-600">Posture Score</div>
          <div className={`text-xs mt-1 ${
            postureScore > 0.7 ? 'text-wellness-600' : 
            postureScore > 0.4 ? 'text-yellow-600' : 'text-red-600'
          }`}>
            {postureScore > 0.7 ? 'Excellent' : postureScore > 0.4 ? 'Good' : 'Needs Attention'}
          </div>
        </div>

        <div className="glass-card text-center">
          <TrendingUp className="w-8 h-8 text-wellness-500 mx-auto mb-3" />
          <div className="text-2xl font-bold mb-1">
            {(recoveryScore * 100).toFixed(0)}%
          </div>
          <div className="text-sm text-gray-600">Recovery Score</div>
          <div className={`text-xs mt-1 ${
            recoveryScore > 0.7 ? 'text-wellness-600' : 
            recoveryScore > 0.4 ? 'text-yellow-600' : 'text-red-600'
          }`}>
            {recoveryScore > 0.7 ? 'Well Rested' : recoveryScore > 0.4 ? 'Moderate' : 'Needs Rest'}
          </div>
        </div>
      </div>

      {/* Key observations */}
      {result.observations && result.observations.length > 0 && (
        <div className="glass-card mb-8">
          <h3 className="text-xl font-semibold mb-4">Key Observations</h3>
          <div className="space-y-3">
            {result.observations.map((observation, index) => (
              <div key={index} className="flex items-start">
                <div className="w-2 h-2 rounded-full bg-wellness-500 mt-2 mr-3 flex-shrink-0" />
                <div className="text-gray-700">{observation}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action items */}
      {result.action_items && result.action_items.length > 0 && (
        <div className="glass-card mb-8">
          <h3 className="text-xl font-semibold mb-4">Personalized Action Items</h3>
          <div className="space-y-4">
            {result.action_items.map((item, index) => (
              <div key={index} className="flex items-start p-3 bg-wellness-50 rounded-lg">
                <div className="flex items-center justify-center w-6 h-6 bg-wellness-600 text-white text-sm font-medium rounded-full mr-3 mt-0.5 flex-shrink-0">
                  {index + 1}
                </div>
                <div className="text-gray-800">{item}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Audio experiences */}
      <div className="glass-card mb-8">
        <h3 className="text-xl font-semibold mb-6">Personalized Audio Experiences</h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Narrative audio */}
          {result.audio?.narrative_url && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-medium mb-2">Personalized Narrative</h4>
              <p className="text-sm text-gray-600 mb-4">
                Listen to your wellness insights read in a calming voice
              </p>
              <button
                onClick={() => playingAudio === 'narrative' ? pauseAudio() : playAudio('narrative', result.audio.narrative_url)}
                className="btn-primary flex items-center w-full justify-center"
              >
                {playingAudio === 'narrative' ? <Pause className="w-5 h-5 mr-2" /> : <Play className="w-5 h-5 mr-2" />}
                {playingAudio === 'narrative' ? 'Pause' : 'Play'} Narrative
              </button>
            </div>
          )}

          {/* Breathing exercise */}
          {result.audio?.breathing_url && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-medium mb-2">3-Minute Breathing Exercise</h4>
              <p className="text-sm text-gray-600 mb-4">
                Guided breathing to help you relax and center yourself
              </p>
              <button
                onClick={() => playingAudio === 'breathing' ? pauseAudio() : playAudio('breathing', result.audio.breathing_url)}
                className="btn-wellness flex items-center w-full justify-center"
              >
                {playingAudio === 'breathing' ? <Pause className="w-5 h-5 mr-2" /> : <Play className="w-5 h-5 mr-2" />}
                {playingAudio === 'breathing' ? 'Pause' : 'Start'} Breathing
              </button>
            </div>
          )}

          {/* Sleep hypnosis */}
          <div className="bg-gray-50 rounded-lg p-4 md:col-span-2">
            <h4 className="font-medium mb-2 flex items-center">
              <Moon className="w-5 h-5 mr-2" />
              Sleep Hypnosis Audio
            </h4>
            <p className="text-sm text-gray-600 mb-4">
              Generate a personalized 10-minute sleep hypnosis based on your current state
            </p>
            
            {!hypnosisAudio ? (
              <button
                onClick={generateSleepHypnosis}
                disabled={generatingHypnosis}
                className="btn-secondary flex items-center"
              >
                {generatingHypnosis ? (
                  <>
                    <LoadingSpinner className="w-5 h-5 mr-2" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Moon className="w-5 h-5 mr-2" />
                    Generate Sleep Audio
                  </>
                )}
              </button>
            ) : (
              <div className="flex gap-3">
                <button
                  onClick={() => playingAudio === 'hypnosis' ? pauseAudio() : playAudio('hypnosis', hypnosisAudio.audio_url)}
                  className="btn-secondary flex items-center"
                >
                  {playingAudio === 'hypnosis' ? <Pause className="w-5 h-5 mr-2" /> : <Play className="w-5 h-5 mr-2" />}
                  {playingAudio === 'hypnosis' ? 'Pause' : 'Play'} Sleep Audio
                </button>
                <a
                  href={hypnosisAudio.audio_url}
                  download="sleep-hypnosis.mp3"
                  className="btn-secondary flex items-center"
                >
                  <Download className="w-5 h-5 mr-2" />
                  Download
                </a>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Data breakdown */}
      {result.analysis_data && (
        <div className="glass-card mb-8">
          <h3 className="text-xl font-semibold mb-4">Analysis Data</h3>
          <div className="grid md:grid-cols-3 gap-6">
            {/* Audio analysis */}
            {result.analysis_data.audio_features && (
              <div>
                <h4 className="font-medium mb-2 flex items-center">
                  <Mic className="w-4 h-4 mr-1" /> Voice Analysis
                </h4>
                <div className="text-sm space-y-1">
                  <div>Stress Score: {(result.analysis_data.audio_features.stress_score * 100).toFixed(0)}%</div>
                  <div>Emotional State: {result.analysis_data.audio_features.emotional_state}</div>
                  <div>Energy Level: {result.analysis_data.audio_features.energy?.toFixed(3)}</div>
                </div>
              </div>
            )}

            {/* Wearable data */}
            {result.analysis_data.wearable_summary && Object.keys(result.analysis_data.wearable_summary).length > 0 && (
              <div>
                <h4 className="font-medium mb-2 flex items-center">
                  <Upload className="w-4 h-4 mr-1" /> Biometrics
                </h4>
                <div className="text-sm space-y-1">
                  {result.analysis_data.wearable_summary.avg_heart_rate && (
                    <div>Avg HR: {result.analysis_data.wearable_summary.avg_heart_rate.toFixed(0)} BPM</div>
                  )}
                  {result.analysis_data.wearable_summary.hrv_status && (
                    <div>HRV Status: {result.analysis_data.wearable_summary.hrv_status}</div>
                  )}
                  {result.analysis_data.wearable_summary.total_sleep_time && (
                    <div>Sleep: {result.analysis_data.wearable_summary.total_sleep_time.toFixed(1)}h</div>
                  )}
                </div>
              </div>
            )}

            {/* Posture data */}
            {result.analysis_data.pose_summary && Object.keys(result.analysis_data.pose_summary).length > 0 && (
              <div>
                <h4 className="font-medium mb-2 flex items-center">
                  <Camera className="w-4 h-4 mr-1" /> Posture
                </h4>
                <div className="text-sm space-y-1">
                  <div>Score: {((result.analysis_data.pose_summary.posture_score || 0.7) * 100).toFixed(0)}%</div>
                  <div>Risk: {result.analysis_data.pose_summary.risk_level || 'Low'}</div>
                  <div>Status: {result.analysis_data.pose_summary.analysis_quality || 'Good'}</div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Reset button */}
      <div className="text-center">
        <button
          onClick={onReset}
          className="btn-secondary flex items-center mx-auto"
        >
          <RotateCcw className="w-5 h-5 mr-2" />
          Start New Wellness Check-in
        </button>
      </div>

      {/* Footer message */}
      <div className="mt-8 text-center text-sm text-gray-500">
        <p>💖 Remember: These insights are for wellness support, not medical diagnosis. Always consult healthcare professionals for medical concerns.</p>
      </div>
    </div>
  )
}

export default AnalysisResults
import React, { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Mic, MicOff, Upload, Camera, ArrowLeft, ArrowRight } from 'lucide-react'
import { useWellness } from '../context/WellnessContext'
import AudioVisualizer from './AudioVisualizer'

function Recording() {
  const navigate = useNavigate()
  const { state, dispatch, setAudioData, setLoading, setError } = useWellness()
  
  const [mediaRecorder, setMediaRecorder] = useState(null)
  const [audioChunks, setAudioChunks] = useState([])
  const [recordingTime, setRecordingTime] = useState(0)
  const [permissionGranted, setPermissionGranted] = useState(false)
  
  const audioRef = useRef(null)
  const timerRef = useRef(null)
  const streamRef = useRef(null)
  
  useEffect(() => {
    requestMicrophonePermission()
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }, [])
  
  const requestMicrophonePermission = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      setPermissionGranted(true)
      streamRef.current = stream
    } catch (error) {
      console.error('Microphone permission denied:', error)
      setError('Microphone access is required for voice analysis. Please allow microphone access and try again.')
    }
  }
  
  const startRecording = async () => {
    try {
      if (!permissionGranted) {
        await requestMicrophonePermission()
        return
      }
      
      const stream = streamRef.current
      const recorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      
      setMediaRecorder(recorder)
      setAudioChunks([])
      setRecordingTime(0)
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setAudioChunks(prev => [...prev, event.data])
        }
      }
      
      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
        const audioUrl = URL.createObjectURL(audioBlob)
        
        if (audioRef.current) {
          audioRef.current.src = audioUrl
        }
        
        // Convert to WAV format for backend
        convertToWav(audioBlob)
      }
      
      recorder.start()
      dispatch({ type: 'SET_RECORDING', payload: true })
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => {
          if (prev >= 10) {
            stopRecording()
            return 10
          }
          return prev + 1
        })
      }, 1000)
      
    } catch (error) {
      console.error('Recording failed:', error)
      setError('Failed to start recording. Please check your microphone and try again.')
    }
  }
  
  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop()
      dispatch({ type: 'SET_RECORDING', payload: false })
      
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }
  
  const convertToWav = async (audioBlob) => {
    try {
      const arrayBuffer = await audioBlob.arrayBuffer()
      const audioContext = new (window.AudioContext || window.webkitAudioContext)()
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)
      
      // Convert to WAV format
      const wavBlob = audioBufferToWav(audioBuffer)
      const filename = `recording_${Date.now()}.wav`
      
      setAudioData(wavBlob, filename)
      
    } catch (error) {
      console.error('Audio conversion failed:', error)
      setError('Failed to process audio. Please try recording again.')
    }
  }
  
  const audioBufferToWav = (audioBuffer) => {
    const numberOfChannels = audioBuffer.numberOfChannels
    const sampleRate = audioBuffer.sampleRate
    const length = audioBuffer.length
    
    const buffer = new ArrayBuffer(44 + length * numberOfChannels * 2)
    const view = new DataView(buffer)
    
    // WAV header
    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i))
      }
    }
    
    writeString(0, 'RIFF')
    view.setUint32(4, 36 + length * numberOfChannels * 2, true)
    writeString(8, 'WAVE')
    writeString(12, 'fmt ')
    view.setUint32(16, 16, true)
    view.setUint16(20, 1, true)
    view.setUint16(22, numberOfChannels, true)
    view.setUint32(24, sampleRate, true)
    view.setUint32(28, sampleRate * numberOfChannels * 2, true)
    view.setUint16(32, numberOfChannels * 2, true)
    view.setUint16(34, 16, true)
    writeString(36, 'data')
    view.setUint32(40, length * numberOfChannels * 2, true)
    
    // Convert audio data
    let offset = 44
    for (let i = 0; i < length; i++) {
      for (let channel = 0; channel < numberOfChannels; channel++) {
        const sample = Math.max(-1, Math.min(1, audioBuffer.getChannelData(channel)[i]))
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true)
        offset += 2
      }
    }
    
    return new Blob([buffer], { type: 'audio/wav' })
  }
  
  const uploadAudio = async () => {
    if (!state.audioBlob) return
    
    setLoading(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('file', state.audioBlob, state.audioFilename)
      
      const response = await fetch('/api/record', {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error('Upload failed')
      }
      
      const result = await response.json()
      
      if (result.ok) {
        dispatch({ type: 'SET_AUDIO_FEATURES', payload: result.features })
        navigate('/analysis')
      } else {
        throw new Error('Analysis failed')
      }
      
    } catch (error) {
      console.error('Upload error:', error)
      setError('Failed to upload audio. Please try again.')
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back</span>
        </button>
        
        <h1 className="text-2xl font-bold text-gray-900">Voice Check-in</h1>
        
        <div className="w-20"></div> {/* Spacer */}
      </div>
      
      {/* Recording Interface */}
      <div className="card text-center mb-8">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            How are you feeling right now?
          </h2>
          <p className="text-gray-600">
            Speak naturally for 10 seconds about your current state, mood, or anything on your mind.
          </p>
        </div>
        
        {/* Audio Visualizer */}
        <div className="mb-8">
          <AudioVisualizer isRecording={state.isRecording} />
        </div>
        
        {/* Recording Controls */}
        <div className="flex flex-col items-center space-y-4">
          {!state.isRecording ? (
            <button
              onClick={startRecording}
              disabled={!permissionGranted}
              className="w-20 h-20 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center transition-colors duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Mic className="w-8 h-8" />
            </button>
          ) : (
            <button
              onClick={stopRecording}
              className="w-20 h-20 bg-gray-500 hover:bg-gray-600 text-white rounded-full flex items-center justify-center transition-colors duration-200 shadow-lg hover:shadow-xl"
            >
              <MicOff className="w-8 h-8" />
            </button>
          )}
          
          {/* Recording Timer */}
          {state.isRecording && (
            <div className="text-center">
              <div className="text-3xl font-bold text-red-500 mb-2">
                {recordingTime}s
              </div>
              <div className="w-64 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-red-500 h-2 rounded-full transition-all duration-1000"
                  style={{ width: `${(recordingTime / 10) * 100}%` }}
                ></div>
              </div>
            </div>
          )}
          
          {/* Status Messages */}
          {!permissionGranted && (
            <p className="text-sm text-amber-600">
              Please allow microphone access to continue
            </p>
          )}
          
          {state.audioBlob && !state.isRecording && (
            <div className="text-center">
              <p className="text-sm text-green-600 mb-4">
                ✓ Recording complete! Ready to analyze.
              </p>
              <audio ref={audioRef} controls className="w-full max-w-md mx-auto" />
            </div>
          )}
        </div>
      </div>
      
      {/* Additional Data Collection */}
      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <Upload className="w-6 h-6 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Wearable Data</h3>
          </div>
          <p className="text-gray-600 mb-4">
            Upload CSV data from your fitness tracker for comprehensive analysis.
          </p>
          <input
            type="file"
            accept=".csv"
            className="input-field"
            onChange={(e) => {
              // Handle wearable data upload
              console.log('Wearable file selected:', e.target.files[0])
            }}
          />
        </div>
        
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <Camera className="w-6 h-6 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Posture Scan</h3>
          </div>
          <p className="text-gray-600 mb-4">
            Take a quick photo for posture analysis and tension detection.
          </p>
          <button className="btn-secondary w-full">
            <Camera className="w-4 h-4 mr-2" />
            Scan Posture
          </button>
        </div>
      </div>
      
      {/* Error Display */}
      {state.error && (
        <div className="card bg-red-50 border-red-200 mb-6">
          <p className="text-red-700">{state.error}</p>
        </div>
      )}
      
      {/* Action Buttons */}
      <div className="flex justify-between">
        <button
          onClick={() => navigate('/')}
          className="btn-secondary"
        >
          Cancel
        </button>
        
        <button
          onClick={uploadAudio}
          disabled={!state.audioBlob || state.isLoading}
          className="btn-primary flex items-center space-x-2"
        >
          {state.isLoading ? (
            <>
              <div className="loading-dots">
                <div></div>
                <div></div>
                <div></div>
              </div>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <span>Analyze My Wellness</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  )
}

export default Recording
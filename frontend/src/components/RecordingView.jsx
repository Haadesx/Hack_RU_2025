import { useState, useRef, useEffect } from 'react'
import { FaMicrophone, FaStop, FaTimes } from 'react-icons/fa'
import axios from 'axios'

const RECORDING_DURATION = 10 // seconds
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function RecordingView({ onComplete, onCancel }) {
  const [isRecording, setIsRecording] = useState(false)
  const [countdown, setCountdown] = useState(RECORDING_DURATION)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [permissionGranted, setPermissionGranted] = useState(false)
  
  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])
  const timerRef = useRef(null)

  useEffect(() => {
    // Request microphone permission on mount
    requestMicrophonePermission()
    
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        mediaRecorderRef.current.stop()
      }
    }
  }, [])

  const requestMicrophonePermission = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      setPermissionGranted(true)
      // Stop the stream immediately - we'll request it again when recording
      stream.getTracks().forEach(track => track.stop())
    } catch (err) {
      console.error('Microphone permission denied:', err)
      setError('Microphone permission denied. Please allow access and refresh.')
    }
  }

  const startRecording = async () => {
    try {
      setError(null)
      chunksRef.current = []
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      
      // Create MediaRecorder with best available codec
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm'
      
      const mediaRecorder = new MediaRecorder(stream, { mimeType })
      mediaRecorderRef.current = mediaRecorder

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach(track => track.stop())
        await handleRecordingComplete()
      }

      mediaRecorder.start()
      setIsRecording(true)
      setCountdown(RECORDING_DURATION)

      // Start countdown timer
      timerRef.current = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            stopRecording()
            return 0
          }
          return prev - 1
        })
      }, 1000)
      
    } catch (err) {
      console.error('Recording error:', err)
      setError('Failed to start recording. Please check microphone permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }

  const handleRecordingComplete = async () => {
    setIsProcessing(true)
    
    try {
      // Create blob from recorded chunks
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
      
      // Create FormData for upload
      const formData = new FormData()
      const filename = `recording_${Date.now()}.webm`
      formData.append('file', blob, filename)

      // Upload to backend
      const response = await axios.post(`${API_BASE_URL}/record`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      if (response.data.ok) {
        // Pass filename to parent
        onComplete(response.data.filename)
      } else {
        throw new Error('Upload failed')
      }
      
    } catch (err) {
      console.error('Upload error:', err)
      setError('Failed to upload recording. Please try again.')
      setIsProcessing(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card text-center">
        {/* Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Voice Check-in</h2>
          <p className="text-gray-600">
            {!isRecording && !isProcessing && 'Tell us how you\'re feeling - what\'s on your mind?'}
            {isRecording && `Recording... ${countdown}s remaining`}
            {isProcessing && 'Processing your recording...'}
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Recording Visualization */}
        <div className="mb-8">
          {!isRecording && !isProcessing && permissionGranted && (
            <div className="flex justify-center">
              <button
                onClick={startRecording}
                className="w-32 h-32 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full 
                         flex items-center justify-center shadow-2xl hover:scale-110 
                         transition-transform duration-200 focus:outline-none focus:ring-4 focus:ring-blue-300"
              >
                <FaMicrophone className="text-white text-5xl" />
              </button>
            </div>
          )}

          {isRecording && (
            <div className="space-y-6">
              {/* Countdown Circle */}
              <div className="flex justify-center">
                <div className="relative">
                  <div className="w-32 h-32 bg-red-500 rounded-full flex items-center justify-center 
                                mic-pulse shadow-2xl">
                    <span className="text-white text-4xl font-bold">{countdown}</span>
                  </div>
                  <div className="absolute inset-0 rounded-full border-4 border-red-300 animate-ping"></div>
                </div>
              </div>

              {/* Waveform Visualization */}
              <div className="waveform">
                {[...Array(20)].map((_, i) => (
                  <div
                    key={i}
                    className="waveform-bar"
                    style={{
                      height: `${Math.random() * 60 + 20}px`,
                      animationDelay: `${i * 0.1}s`
                    }}
                  />
                ))}
              </div>

              {/* Stop Button */}
              <button
                onClick={stopRecording}
                className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 
                         transition-colors inline-flex items-center space-x-2"
              >
                <FaStop />
                <span>Stop Recording</span>
              </button>
            </div>
          )}

          {isProcessing && (
            <div className="flex flex-col items-center space-y-4">
              <div className="spinner"></div>
              <p className="text-gray-600">Analyzing your voice...</p>
            </div>
          )}

          {!permissionGranted && !error && (
            <div className="text-center">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Requesting microphone permission...</p>
            </div>
          )}
        </div>

        {/* Instructions */}
        {!isRecording && !isProcessing && permissionGranted && (
          <div className="mb-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>Tips:</strong> Speak naturally about how you're feeling. 
              You can talk about your energy level, stress, sleep quality, or anything on your mind.
            </p>
          </div>
        )}

        {/* Cancel Button */}
        {!isRecording && !isProcessing && (
          <button
            onClick={onCancel}
            className="text-gray-600 hover:text-gray-900 inline-flex items-center space-x-2"
          >
            <FaTimes />
            <span>Cancel</span>
          </button>
        )}
      </div>

      {/* Privacy Notice */}
      <div className="mt-6 text-center text-sm text-gray-500">
        <p>🔒 Your recording is encrypted and processed securely</p>
      </div>
    </div>
  )
}

export default RecordingView

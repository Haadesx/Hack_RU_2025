import React, { useState, useRef, useEffect } from 'react'
import { Mic, MicOff, Play, Pause, Square, RotateCcw } from 'lucide-react'
import LoadingSpinner from './LoadingSpinner'

const API_BASE = '/api'

const RecordingInterface = ({ onRecordingComplete, onBack }) => {
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [audioBlob, setAudioBlob] = useState(null)
  const [audioUrl, setAudioUrl] = useState(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [waveformData, setWaveformData] = useState([])
  const [permissionDenied, setPermissionDenied] = useState(false)
  
  const mediaRecorderRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const audioRef = useRef(null)
  const chunksRef = useRef([])
  const timerRef = useRef(null)
  const animationRef = useRef(null)

  useEffect(() => {
    return () => {
      // Cleanup
      if (timerRef.current) clearInterval(timerRef.current)
      if (animationRef.current) cancelAnimationFrame(animationRef.current)
      if (audioContextRef.current) audioContextRef.current.close()
    }
  }, [])

  const startRecording = async () => {
    try {
      setPermissionDenied(false)
      
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        }
      })

      // Set up audio context for visualization
      audioContextRef.current = new AudioContext()
      analyserRef.current = audioContextRef.current.createAnalyser()
      const source = audioContextRef.current.createMediaStreamSource(stream)
      source.connect(analyserRef.current)
      
      analyserRef.current.fftSize = 256
      
      // Set up media recorder
      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      })
      
      chunksRef.current = []
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }
      
      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        setAudioBlob(blob)
        setAudioUrl(URL.createObjectURL(blob))
        stream.getTracks().forEach(track => track.stop())
      }
      
      // Start recording
      mediaRecorderRef.current.start()
      setIsRecording(true)
      setRecordingTime(0)
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => {
          const newTime = prev + 0.1
          if (newTime >= 10) {
            stopRecording()
            return 10
          }
          return newTime
        })
      }, 100)
      
      // Start waveform animation
      updateWaveform()
      
    } catch (error) {
      console.error('Error starting recording:', error)
      setPermissionDenied(true)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      
      if (timerRef.current) {
        clearInterval(timerRef.current)
        timerRef.current = null
      }
      
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
        animationRef.current = null
      }
    }
  }

  const updateWaveform = () => {
    if (!analyserRef.current || !isRecording) return
    
    const bufferLength = analyserRef.current.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)
    analyserRef.current.getByteFrequencyData(dataArray)
    
    // Sample some frequencies for visualization
    const sampleSize = 32
    const step = Math.floor(bufferLength / sampleSize)
    const samples = []
    
    for (let i = 0; i < sampleSize; i++) {
      samples.push(dataArray[i * step] / 255)
    }
    
    setWaveformData(samples)
    
    if (isRecording) {
      animationRef.current = requestAnimationFrame(updateWaveform)
    }
  }

  const playRecording = () => {
    if (audioRef.current) {
      audioRef.current.play()
      setIsPlaying(true)
    }
  }

  const pauseRecording = () => {
    if (audioRef.current) {
      audioRef.current.pause()
      setIsPlaying(false)
    }
  }

  const resetRecording = () => {
    setAudioBlob(null)
    setAudioUrl(null)
    setRecordingTime(0)
    setWaveformData([])
    setIsPlaying(false)
  }

  const uploadRecording = async () => {
    if (!audioBlob) return

    setIsUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', audioBlob, 'recording.webm')

      const response = await fetch(`${API_BASE}/record`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      const result = await response.json()
      onRecordingComplete(result.filename)
      
    } catch (error) {
      console.error('Upload error:', error)
      alert('Failed to upload recording. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold mb-4">Voice Check-in</h2>
        <p className="text-gray-600 text-lg">
          Take a moment to share how you're feeling. Speak naturally for up to 10 seconds.
        </p>
      </div>

      {/* Permission denied message */}
      {permissionDenied && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <h3 className="font-medium text-red-800 mb-2">Microphone Access Required</h3>
          <p className="text-red-600 text-sm">
            Please allow microphone access to record your voice check-in. 
            You may need to refresh the page and try again.
          </p>
        </div>
      )}

      {/* Recording interface */}
      <div className="glass-card mb-6">
        {/* Waveform visualization */}
        <div className="mb-6 h-32 flex items-center justify-center bg-gray-50 rounded-lg">
          {isRecording || waveformData.length > 0 ? (
            <div className="flex items-end justify-center gap-1 h-20">
              {waveformData.map((level, index) => (
                <div
                  key={index}
                  className="bg-wellness-500 rounded-full transition-all duration-100"
                  style={{
                    width: '4px',
                    height: `${Math.max(4, level * 60)}px`
                  }}
                />
              ))}
            </div>
          ) : (
            <div className="text-gray-400 text-center">
              <Mic className="w-12 h-12 mx-auto mb-2" />
              <div>Waveform will appear here</div>
            </div>
          )}
        </div>

        {/* Timer */}
        <div className="text-center mb-6">
          <div className="text-4xl font-mono font-bold text-gray-700">
            {recordingTime.toFixed(1)}s
          </div>
          <div className="text-sm text-gray-500">
            {isRecording ? 'Recording...' : audioBlob ? 'Recording complete' : 'Ready to record'}
          </div>
        </div>

        {/* Controls */}
        <div className="flex justify-center gap-4">
          {!audioBlob ? (
            <>
              <button
                onClick={isRecording ? stopRecording : startRecording}
                disabled={permissionDenied}
                className={`
                  w-16 h-16 rounded-full flex items-center justify-center transition-all duration-200
                  ${isRecording 
                    ? 'bg-red-500 hover:bg-red-600 text-white animate-pulse' 
                    : 'bg-wellness-500 hover:bg-wellness-600 text-white'
                  }
                  disabled:bg-gray-300 disabled:cursor-not-allowed
                `}
              >
                {isRecording ? <Square className="w-8 h-8" /> : <Mic className="w-8 h-8" />}
              </button>
            </>
          ) : (
            <>
              <button
                onClick={isPlaying ? pauseRecording : playRecording}
                className="w-12 h-12 rounded-full bg-primary-500 hover:bg-primary-600 text-white flex items-center justify-center"
              >
                {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6" />}
              </button>
              
              <button
                onClick={resetRecording}
                className="w-12 h-12 rounded-full bg-gray-400 hover:bg-gray-500 text-white flex items-center justify-center"
              >
                <RotateCcw className="w-6 h-6" />
              </button>
            </>
          )}
        </div>

        {/* Hidden audio element for playback */}
        {audioUrl && (
          <audio
            ref={audioRef}
            src={audioUrl}
            onEnded={() => setIsPlaying(false)}
            className="hidden"
          />
        )}
      </div>

      {/* Navigation buttons */}
      <div className="flex justify-between">
        <button onClick={onBack} className="btn-secondary">
          Back
        </button>
        
        {audioBlob && (
          <button
            onClick={uploadRecording}
            disabled={isUploading}
            className="btn-wellness flex items-center"
          >
            {isUploading ? (
              <>
                <LoadingSpinner className="w-5 h-5 mr-2" />
                Uploading...
              </>
            ) : (
              'Continue to Biometrics'
            )}
          </button>
        )}
      </div>

      {/* Help text */}
      <div className="mt-6 text-center text-sm text-gray-500">
        <p>💡 Tip: Speak naturally about how you're feeling - energy levels, stress, mood, or anything on your mind.</p>
      </div>
    </div>
  )
}

export default RecordingInterface
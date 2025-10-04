import React, { useState, useRef, useEffect } from 'react'
import { Camera, CameraOff, Check, RotateCcw, User, AlertTriangle } from 'lucide-react'
import LoadingSpinner from './LoadingSpinner'

const API_BASE = '/api'

const CameraCapture = ({ onCaptureComplete, onSkip, onBack }) => {
  const [hasPermission, setHasPermission] = useState(null)
  const [isCapturing, setIsCapturing] = useState(false)
  const [captured, setCaptured] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [poseResult, setPoseResult] = useState(null)
  const [error, setError] = useState(null)
  
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const streamRef = useRef(null)

  useEffect(() => {
    return () => {
      // Cleanup camera stream
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
    }
  }, [])

  const startCamera = async () => {
    try {
      setError(null)
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        }
      })
      
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }
      setHasPermission(true)
      setIsCapturing(true)
      
    } catch (err) {
      console.error('Camera access error:', err)
      setHasPermission(false)
      setError('Camera access denied. Please allow camera access to continue.')
    }
  }

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    setIsCapturing(false)
  }

  const captureFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return

    const video = videoRef.current
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    // Draw current video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height)

    // Convert to blob for analysis
    canvas.toBlob(async (blob) => {
      await analyzePosture(blob)
    }, 'image/jpeg', 0.8)

    setCaptured(true)
    stopCamera()
  }

  const analyzePosture = async (imageBlob) => {
    setAnalyzing(true)
    setError(null)

    try {
      // For demo purposes, we'll simulate pose analysis
      // In a real implementation, you'd either:
      // 1. Use MediaPipe in the browser to extract pose landmarks
      // 2. Send the image to the backend for pose analysis
      
      // Simulate analysis delay
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Mock pose keypoints (in a real app, these would come from MediaPipe)
      const mockPoseData = {
        landmarks: generateMockPoseKeypoints(),
        confidence: 0.85,
        timestamp: Date.now()
      }

      // Send pose data to backend for analysis
      const response = await fetch(`${API_BASE}/camera-scan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(mockPoseData)
      })

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`)
      }

      const result = await response.json()
      setPoseResult(result)

    } catch (err) {
      console.error('Posture analysis error:', err)
      setError(err.message || 'Failed to analyze posture. Please try again.')
    } finally {
      setAnalyzing(false)
    }
  }

  const generateMockPoseKeypoints = () => {
    // Generate realistic pose keypoints for demo
    // In reality, these would come from MediaPipe pose detection
    const keypoints = []
    
    // Add 33 pose landmarks (MediaPipe format)
    for (let i = 0; i < 33; i++) {
      keypoints.push({
        x: 0.3 + Math.random() * 0.4, // Normalized coordinates
        y: 0.2 + Math.random() * 0.6,
        z: Math.random() * 0.1,
        visibility: 0.7 + Math.random() * 0.3
      })
    }
    
    return keypoints
  }

  const resetCapture = () => {
    setCaptured(false)
    setPoseResult(null)
    setAnalyzing(false)
    setError(null)
    startCamera()
  }

  const continueWithResults = () => {
    if (poseResult) {
      onCaptureComplete(poseResult.summary)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold mb-4">Posture Scan</h2>
        <p className="text-gray-600 text-lg">
          Take a quick photo to analyze your posture and detect any tension or alignment issues.
        </p>
      </div>

      {/* Camera interface */}
      <div className="glass-card mb-6">
        {!hasPermission ? (
          <div className="text-center py-12">
            <Camera className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-4">Camera Access Required</h3>
            <p className="text-gray-600 mb-6">
              We need camera access to capture a photo for posture analysis.
            </p>
            <button onClick={startCamera} className="btn-primary">
              <Camera className="w-5 h-5 mr-2" />
              Enable Camera
            </button>
          </div>
        ) : hasPermission === false ? (
          <div className="text-center py-12">
            <CameraOff className="w-16 h-16 text-red-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-red-700 mb-4">Camera Access Denied</h3>
            <p className="text-red-600 mb-6">
              Please allow camera access in your browser settings and refresh the page.
            </p>
          </div>
        ) : (
          <div className="relative">
            {/* Video feed */}
            {isCapturing && (
              <div className="relative">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="w-full h-64 object-cover rounded-lg bg-gray-900"
                />
                
                {/* Posture guidance overlay */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="border-2 border-white/50 rounded-lg w-48 h-64 flex items-end justify-center pb-4">
                    <User className="w-8 h-8 text-white/70" />
                  </div>
                </div>
                
                <div className="absolute bottom-4 left-4 right-4">
                  <div className="bg-black/50 text-white text-sm p-2 rounded">
                    💡 Sit up straight, look at the camera, and position your shoulders in frame
                  </div>
                </div>
              </div>
            )}

            {/* Canvas for capture (hidden) */}
            <canvas ref={canvasRef} className="hidden" />

            {/* Analysis state */}
            {analyzing && (
              <div className="text-center py-12">
                <LoadingSpinner className="w-12 h-12 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">Analyzing Your Posture</h3>
                <p className="text-gray-600">
                  Using AI to detect your body alignment and identify areas of tension...
                </p>
              </div>
            )}

            {/* Results */}
            {poseResult && !analyzing && (
              <div className="text-center py-8">
                <Check className="w-12 h-12 text-wellness-600 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-4">Posture Analysis Complete</h3>
                
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="text-center">
                      <div className="font-medium">Posture Score</div>
                      <div className={`text-2xl font-bold ${
                        poseResult.summary?.posture_score > 0.7 ? 'text-wellness-600' : 
                        poseResult.summary?.posture_score > 0.4 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {((poseResult.summary?.posture_score || 0.7) * 100).toFixed(0)}%
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="font-medium">Risk Level</div>
                      <div className={`font-bold ${
                        poseResult.summary?.risk_level === 'low' ? 'text-wellness-600' :
                        poseResult.summary?.risk_level === 'moderate' ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {poseResult.summary?.risk_level || 'Low'}
                      </div>
                    </div>
                  </div>
                </div>

                {poseResult.summary?.recommendations && (
                  <div className="text-left">
                    <h4 className="font-medium mb-2">Quick Recommendations:</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      {poseResult.summary.recommendations.slice(0, 2).map((rec, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-wellness-600 mr-2">•</span>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-start">
            <AlertTriangle className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
            {error}
          </div>
        )}
      </div>

      {/* Controls */}
      {isCapturing && (
        <div className="text-center mb-6">
          <button
            onClick={captureFrame}
            className="btn-wellness text-lg py-4 px-8"
          >
            <Camera className="w-6 h-6 mr-3" />
            Capture Posture Photo
          </button>
        </div>
      )}

      {captured && !poseResult && !analyzing && (
        <div className="text-center mb-6">
          <button
            onClick={resetCapture}
            className="btn-secondary"
          >
            <RotateCcw className="w-5 h-5 mr-2" />
            Take Another Photo
          </button>
        </div>
      )}

      {/* Navigation buttons */}
      <div className="flex justify-between">
        <button onClick={onBack} className="btn-secondary">
          Back
        </button>
        
        <div className="flex gap-3">
          <button onClick={onSkip} className="btn-secondary">
            Skip Posture Scan
          </button>
          
          {poseResult && (
            <button
              onClick={continueWithResults}
              className="btn-wellness"
            >
              Continue to Analysis
            </button>
          )}
        </div>
      </div>

      {/* Help text */}
      <div className="mt-6 text-center text-sm text-gray-500">
        <p>💡 Good posture helps reduce tension and improve your overall wellbeing throughout the day.</p>
      </div>
    </div>
  )
}

export default CameraCapture
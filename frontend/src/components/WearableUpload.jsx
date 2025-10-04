import React, { useState, useRef } from 'react'
import { Upload, FileText, Check, X, Heart, Clock, TrendingUp } from 'lucide-react'
import LoadingSpinner from './LoadingSpinner'

const API_BASE = '/api'

const WearableUpload = ({ onUploadComplete, onSkip, onBack }) => {
  const [dragOver, setDragOver] = useState(false)
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      validateAndSetFile(droppedFile)
    }
  }

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      validateAndSetFile(selectedFile)
    }
  }

  const validateAndSetFile = (selectedFile) => {
    // Check file type
    if (!selectedFile.name.toLowerCase().endsWith('.csv')) {
      setError('Please select a CSV file containing your wearable data.')
      return
    }

    // Check file size (max 10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size too large. Please select a file under 10MB.')
      return
    }

    setFile(selectedFile)
    setError(null)
  }

  const uploadFile = async () => {
    if (!file) return

    setUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_BASE}/wearable/upload`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      const result = await response.json()
      setUploadResult(result)
      
    } catch (err) {
      console.error('Upload error:', err)
      setError(err.message || 'Failed to upload file. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  const continueWithData = () => {
    if (uploadResult) {
      onUploadComplete(uploadResult.filename)
    }
  }

  const removeFile = () => {
    setFile(null)
    setUploadResult(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold mb-4">Biometric Data</h2>
        <p className="text-gray-600 text-lg">
          Upload your wearable device data (heart rate, HRV, sleep) for comprehensive analysis.
        </p>
      </div>

      {/* Upload area */}
      <div className="glass-card mb-6">
        {!file && !uploadResult ? (
          <div
            className={`
              border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer
              ${dragOver 
                ? 'border-primary-400 bg-primary-50' 
                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
              }
            `}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-2">Upload Wearable Data</h3>
            <p className="text-gray-600 mb-4">
              Drag and drop your CSV file here, or click to select
            </p>
            <div className="text-sm text-gray-500">
              Supports CSV files from Fitbit, Apple Health, Garmin, Oura, and more
            </div>
            
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>
        ) : uploadResult ? (
          <div className="text-center">
            <Check className="w-12 h-12 text-wellness-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-4">Data Uploaded Successfully</h3>
            
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <h4 className="font-medium mb-3">Analysis Summary:</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="flex items-center">
                  <Heart className="w-4 h-4 text-red-500 mr-2" />
                  <span>Avg HR: {uploadResult.summary?.avg_heart_rate?.toFixed(0) || 'N/A'} BPM</span>
                </div>
                <div className="flex items-center">
                  <TrendingUp className="w-4 h-4 text-blue-500 mr-2" />
                  <span>HRV: {uploadResult.summary?.hrv_status || 'N/A'}</span>
                </div>
                <div className="flex items-center">
                  <Clock className="w-4 h-4 text-purple-500 mr-2" />
                  <span>Sleep: {uploadResult.summary?.total_sleep_time?.toFixed(1) || 'N/A'}h</span>
                </div>
                <div className="flex items-center">
                  <Heart className="w-4 h-4 text-wellness-600 mr-2" />
                  <span>Recovery: {(uploadResult.summary?.recovery_score * 100)?.toFixed(0) || 'N/A'}%</span>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center">
              <FileText className="w-8 h-8 text-gray-600 mr-3" />
              <div>
                <div className="font-medium">{file.name}</div>
                <div className="text-sm text-gray-600">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </div>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="text-gray-400 hover:text-red-500"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        )}

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {file && !uploadResult && !uploading && (
          <div className="mt-4 text-center">
            <button
              onClick={uploadFile}
              className="btn-wellness"
            >
              Upload and Analyze Data
            </button>
          </div>
        )}

        {uploading && (
          <div className="mt-4 text-center">
            <LoadingSpinner className="w-6 h-6 mx-auto mb-2" />
            <div className="text-gray-600">Processing your biometric data...</div>
          </div>
        )}
      </div>

      {/* Expected data format info */}
      <div className="glass-card mb-6">
        <h3 className="font-medium mb-3">Expected CSV Format:</h3>
        <div className="text-sm text-gray-600 space-y-2">
          <div>• <strong>timestamp</strong>: Date/time of measurement</div>
          <div>• <strong>heart_rate</strong>: Heart rate in BPM</div>
          <div>• <strong>hrv_rmssd</strong>: Heart rate variability (optional)</div>
          <div>• <strong>sleep_stage</strong>: Sleep stage (deep, light, REM, awake)</div>
        </div>
        <div className="mt-3 text-xs text-gray-500">
          Don't have this format? No worries - we'll do our best to analyze whatever data you have!
        </div>
      </div>

      {/* Navigation buttons */}
      <div className="flex justify-between">
        <button onClick={onBack} className="btn-secondary">
          Back
        </button>
        
        <div className="flex gap-3">
          <button onClick={onSkip} className="btn-secondary">
            Skip Biometrics
          </button>
          
          {uploadResult && (
            <button
              onClick={continueWithData}
              className="btn-wellness"
            >
              Continue to Posture Scan
            </button>
          )}
        </div>
      </div>

      {/* Help text */}
      <div className="mt-6 text-center text-sm text-gray-500">
        <p>💡 Biometric data helps us understand your stress, recovery, and sleep patterns for more personalized insights.</p>
      </div>
    </div>
  )
}

export default WearableUpload
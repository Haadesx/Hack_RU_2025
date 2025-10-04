import { useState } from 'react'
import { FaUpload, FaFileCsv, FaCheck } from 'react-icons/fa'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function WearableUpload({ onUpload }) {
  const [isUploading, setIsUploading] = useState(false)
  const [uploadSuccess, setUploadSuccess] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    // Validate file type
    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file')
      return
    }

    setIsUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_BASE_URL}/wearable/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      if (response.data.ok) {
        setUploadSuccess(true)
        onUpload(response.data.filename)
        
        // Reset success message after 3 seconds
        setTimeout(() => setUploadSuccess(false), 3000)
      } else {
        throw new Error('Upload failed')
      }
    } catch (err) {
      console.error('Wearable upload error:', err)
      setError('Failed to upload wearable data. Please check the file format.')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="card border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors">
      <div className="text-center">
        <div className="mb-4">
          <FaFileCsv className="text-5xl text-gray-400 mx-auto" />
        </div>

        <h3 className="text-lg font-semibold mb-2">Add Wearable Data (Optional)</h3>
        <p className="text-sm text-gray-600 mb-4">
          Upload CSV with heart rate, HRV, and sleep data for deeper insights
        </p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {uploadSuccess && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm flex items-center justify-center space-x-2">
            <FaCheck />
            <span>Wearable data uploaded successfully!</span>
          </div>
        )}

        <div className="relative">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={isUploading}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
            id="wearable-upload"
          />
          <label
            htmlFor="wearable-upload"
            className={`btn-secondary inline-flex items-center space-x-2 cursor-pointer
                      ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {isUploading ? (
              <>
                <div className="spinner w-4 h-4 border-2"></div>
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <FaUpload />
                <span>Upload CSV</span>
              </>
            )}
          </label>
        </div>

        <div className="mt-4 text-xs text-gray-500">
          <p className="mb-2">Expected CSV format:</p>
          <code className="bg-gray-100 px-2 py-1 rounded text-xs">
            timestamp, heart_rate, hrv_rmssd, sleep_stage, activity_level
          </code>
        </div>
      </div>
    </div>
  )
}

export default WearableUpload

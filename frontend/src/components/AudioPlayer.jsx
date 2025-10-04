import { useState, useRef, useEffect } from 'react'
import { FaPlay, FaPause, FaVolumeUp } from 'react-icons/fa'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function AudioPlayer({ title, filename, icon, description }) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [error, setError] = useState(null)
  
  const audioRef = useRef(null)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleLoadedMetadata = () => {
      setDuration(audio.duration)
    }

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime)
    }

    const handleEnded = () => {
      setIsPlaying(false)
      setCurrentTime(0)
    }

    const handleError = (e) => {
      console.error('Audio playback error:', e)
      setError('Failed to load audio')
      setIsPlaying(false)
    }

    audio.addEventListener('loadedmetadata', handleLoadedMetadata)
    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('ended', handleEnded)
    audio.addEventListener('error', handleError)

    return () => {
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata)
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('ended', handleEnded)
      audio.removeEventListener('error', handleError)
    }
  }, [])

  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio) return

    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }

  const handleSeek = (e) => {
    const audio = audioRef.current
    if (!audio) return

    const rect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - rect.left
    const percentage = x / rect.width
    audio.currentTime = percentage * duration
  }

  const formatTime = (seconds) => {
    if (isNaN(seconds)) return '0:00'
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0

  return (
    <div className="card bg-gradient-to-br from-purple-50 to-white hover:shadow-xl transition-shadow">
      <div className="flex items-start space-x-4">
        {/* Icon */}
        <div className="flex-shrink-0 text-4xl">{icon}</div>
        
        {/* Content */}
        <div className="flex-1">
          <h4 className="font-semibold text-lg mb-1">{title}</h4>
          {description && (
            <p className="text-sm text-gray-600 mb-4">{description}</p>
          )}
          
          {error && (
            <div className="mb-3 p-2 bg-red-50 text-red-600 text-sm rounded">
              {error}
            </div>
          )}

          {/* Audio Element */}
          <audio
            ref={audioRef}
            src={`${API_BASE_URL}/audio/${filename}`}
            preload="metadata"
          />

          {/* Controls */}
          <div className="space-y-3">
            {/* Progress Bar */}
            <div
              className="w-full h-2 bg-gray-200 rounded-full cursor-pointer hover:h-3 transition-all"
              onClick={handleSeek}
            >
              <div
                className="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>

            {/* Time and Play Button */}
            <div className="flex items-center justify-between">
              <button
                onClick={togglePlay}
                className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 text-white 
                         rounded-full flex items-center justify-center hover:scale-110 
                         transition-transform shadow-lg focus:outline-none focus:ring-4 focus:ring-blue-300"
                disabled={error}
              >
                {isPlaying ? (
                  <FaPause className="text-xl" />
                ) : (
                  <FaPlay className="text-xl ml-1" />
                )}
              </button>

              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <span>{formatTime(currentTime)}</span>
                <span>/</span>
                <span>{formatTime(duration)}</span>
              </div>

              <div className="flex items-center space-x-2 text-gray-400">
                <FaVolumeUp />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AudioPlayer

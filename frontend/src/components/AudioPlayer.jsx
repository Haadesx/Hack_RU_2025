import React, { useState, useRef, useEffect } from 'react'
import { Play, Pause, Volume2, Download } from 'lucide-react'

function AudioPlayer({ url, title, onPlay, onPause }) {
  const audioRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return
    
    const updateTime = () => setCurrentTime(audio.currentTime)
    const updateDuration = () => setDuration(audio.duration)
    
    audio.addEventListener('timeupdate', updateTime)
    audio.addEventListener('loadedmetadata', updateDuration)
    audio.addEventListener('ended', () => {
      setIsPlaying(false)
      onPause?.()
    })
    
    return () => {
      audio.removeEventListener('timeupdate', updateTime)
      audio.removeEventListener('loadedmetadata', updateDuration)
    }
  }, [onPause])
  
  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio) return
    
    if (isPlaying) {
      audio.pause()
      setIsPlaying(false)
      onPause?.()
    } else {
      audio.play()
      setIsPlaying(true)
      onPlay?.()
    }
  }
  
  const handleSeek = (e) => {
    const audio = audioRef.current
    if (!audio) return
    
    const rect = e.currentTarget.getBoundingClientRect()
    const clickX = e.clientX - rect.left
    const newTime = (clickX / rect.width) * duration
    audio.currentTime = newTime
    setCurrentTime(newTime)
  }
  
  const handleVolumeChange = (e) => {
    const newVolume = parseFloat(e.target.value)
    setVolume(newVolume)
    if (audioRef.current) {
      audioRef.current.volume = newVolume
    }
  }
  
  const formatTime = (time) => {
    if (isNaN(time)) return '0:00'
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }
  
  const downloadAudio = () => {
    if (url) {
      const link = document.createElement('a')
      link.href = url
      link.download = 'wellness-audio.mp3'
      link.click()
    }
  }
  
  return (
    <div className="space-y-4">
      {/* Hidden audio element */}
      <audio
        ref={audioRef}
        src={url}
        preload="metadata"
      />
      
      {/* Play/Pause Button */}
      <div className="flex items-center justify-center">
        <button
          onClick={togglePlay}
          disabled={!url}
          className="w-16 h-16 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white rounded-full flex items-center justify-center transition-colors duration-200 shadow-lg hover:shadow-xl disabled:cursor-not-allowed"
        >
          {isPlaying ? (
            <Pause className="w-6 h-6" />
          ) : (
            <Play className="w-6 h-6 ml-1" />
          )}
        </button>
      </div>
      
      {/* Progress Bar */}
      <div className="space-y-2">
        <div
          className="w-full h-2 bg-gray-200 rounded-full cursor-pointer"
          onClick={handleSeek}
        >
          <div
            className="h-2 bg-primary-500 rounded-full transition-all duration-100"
            style={{ width: `${duration ? (currentTime / duration) * 100 : 0}%` }}
          />
        </div>
        
        <div className="flex justify-between text-sm text-gray-500">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>
      
      {/* Volume Control */}
      <div className="flex items-center space-x-3">
        <Volume2 className="w-4 h-4 text-gray-500" />
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={volume}
          onChange={handleVolumeChange}
          className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
        <span className="text-sm text-gray-500 w-8">
          {Math.round(volume * 100)}%
        </span>
      </div>
      
      {/* Download Button */}
      {url && (
        <button
          onClick={downloadAudio}
          className="w-full flex items-center justify-center space-x-2 py-2 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
        >
          <Download className="w-4 h-4" />
          <span>Download Audio</span>
        </button>
      )}
      
      {/* Title */}
      <p className="text-sm text-gray-600 text-center">{title}</p>
    </div>
  )
}

export default AudioPlayer
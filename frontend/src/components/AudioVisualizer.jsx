import React, { useEffect, useRef, useState } from 'react'

function AudioVisualizer({ isRecording }) {
  const canvasRef = useRef(null)
  const animationRef = useRef(null)
  const [bars, setBars] = useState([])
  
  useEffect(() => {
    if (isRecording) {
      startVisualization()
    } else {
      stopVisualization()
    }
    
    return () => stopVisualization()
  }, [isRecording])
  
  const startVisualization = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    const barCount = 32
    const barWidth = canvas.width / barCount
    
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      for (let i = 0; i < barCount; i++) {
        const barHeight = Math.random() * canvas.height * 0.8
        const x = i * barWidth
        const y = canvas.height - barHeight
        
        // Create gradient
        const gradient = ctx.createLinearGradient(0, y, 0, canvas.height)
        gradient.addColorStop(0, '#ef4444') // red-500
        gradient.addColorStop(1, '#dc2626') // red-600
        
        ctx.fillStyle = gradient
        ctx.fillRect(x, y, barWidth - 2, barHeight)
      }
      
      animationRef.current = requestAnimationFrame(animate)
    }
    
    animate()
  }
  
  const stopVisualization = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current)
      animationRef.current = null
    }
    
    // Fade out animation
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    let opacity = 1
    
    const fadeOut = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      opacity -= 0.05
      
      if (opacity > 0) {
        requestAnimationFrame(fadeOut)
      }
    }
    
    fadeOut()
  }
  
  return (
    <div className="audio-visualizer">
      <canvas
        ref={canvasRef}
        width={400}
        height={64}
        className="w-full h-full"
      />
    </div>
  )
}

export default AudioVisualizer
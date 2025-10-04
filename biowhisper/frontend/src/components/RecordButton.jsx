import { useEffect, useRef, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function RecordButton({ onUploaded }) {
  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])
  const [recording, setRecording] = useState(false)
  const [countdown, setCountdown] = useState(0)

  useEffect(() => {
    let timer
    if (recording) {
      setCountdown(10)
      timer = setInterval(() => {
        setCountdown((c) => {
          if (c <= 1) {
            stopRecording()
            return 0
          }
          return c - 1
        })
      }, 1000)
    }
    return () => timer && clearInterval(timer)
  }, [recording])

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mediaRecorder = new MediaRecorder(stream)
    mediaRecorderRef.current = mediaRecorder
    chunksRef.current = []

    mediaRecorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) {
        chunksRef.current.push(e.data)
      }
    }

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
      const wavBlob = await convertWebmToWav(blob)
      const file = new File([wavBlob], `checkin_${Date.now()}.wav`, { type: 'audio/wav' })

      const form = new FormData()
      form.append('file', file)
      const resp = await fetch(`${API_BASE}/record`, { method: 'POST', body: form })
      const data = await resp.json()
      onUploaded?.(data)
    }

    mediaRecorder.start(100)
    setRecording(true)
  }

  function stopRecording() {
    setRecording(false)
    mediaRecorderRef.current?.stop()
    mediaRecorderRef.current?.stream.getTracks().forEach(t => t.stop())
  }

  return (
    <div className="flex items-center gap-3">
      {!recording ? (
        <button className="px-4 py-2 rounded bg-emerald-600 text-white" onClick={startRecording}>
          Start 10s Check-in
        </button>
      ) : (
        <button className="px-4 py-2 rounded bg-red-600 text-white" onClick={stopRecording}>
          Stop ({countdown}s)
        </button>
      )}
    </div>
  )
}

// Convert WebM/Opus to WAV using WebAudio for backend compatibility
async function convertWebmToWav(webmBlob) {
  const arrayBuffer = await webmBlob.arrayBuffer()
  const audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)

  const wavBuffer = audioBufferToWav(audioBuffer)
  return new Blob([wavBuffer], { type: 'audio/wav' })
}

function audioBufferToWav(buffer) {
  const numOfChan = buffer.numberOfChannels
  const sampleRate = buffer.sampleRate
  const format = 1 // PCM
  let samples

  if (numOfChan === 2) {
    const chan0 = buffer.getChannelData(0)
    const chan1 = buffer.getChannelData(1)
    samples = interleave(chan0, chan1)
  } else {
    samples = buffer.getChannelData(0)
  }

  const bytesPerSample = 2
  const blockAlign = numOfChan * bytesPerSample
  const bufferLength = 44 + samples.length * bytesPerSample
  const arrayBuffer = new ArrayBuffer(bufferLength)
  const view = new DataView(arrayBuffer)

  /* RIFF identifier */
  writeString(view, 0, 'RIFF')
  /* RIFF chunk length */
  view.setUint32(4, 36 + samples.length * bytesPerSample, true)
  /* RIFF type */
  writeString(view, 8, 'WAVE')
  /* format chunk identifier */
  writeString(view, 12, 'fmt ')
  /* format chunk length */
  view.setUint32(16, 16, true)
  /* sample format (raw) */
  view.setUint16(20, format, true)
  /* channel count */
  view.setUint16(22, numOfChan, true)
  /* sample rate */
  view.setUint32(24, sampleRate, true)
  /* byte rate (sample rate * block align) */
  view.setUint32(28, sampleRate * blockAlign, true)
  /* block align (channel count * bytes per sample) */
  view.setUint16(32, blockAlign, true)
  /* bits per sample */
  view.setUint16(34, 8 * bytesPerSample, true)
  /* data chunk identifier */
  writeString(view, 36, 'data')
  /* data chunk length */
  view.setUint32(40, samples.length * bytesPerSample, true)

  // write PCM samples
  floatTo16BitPCM(view, 44, samples)

  return arrayBuffer
}

function writeString(view, offset, string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i))
  }
}

function floatTo16BitPCM(output, offset, input) {
  for (let i = 0; i < input.length; i++, offset += 2) {
    let s = Math.max(-1, Math.min(1, input[i]))
    s = s < 0 ? s * 0x8000 : s * 0x7fff
    output.setInt16(offset, s, true)
  }
}

function interleave(inputL, inputR) {
  const length = inputL.length + inputR.length
  const result = new Float32Array(length)
  let index = 0
  let inputIndex = 0

  while (index < length) {
    result[index++] = inputL[inputIndex]
    result[index++] = inputR[inputIndex]
    inputIndex++
  }
  return result
}

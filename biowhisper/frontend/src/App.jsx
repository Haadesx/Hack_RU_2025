import { useState } from 'react'
import RecordButton from './components/RecordButton.jsx'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App() {
  const [features, setFeatures] = useState(null)
  const [filename, setFilename] = useState(null)
  const [narrative, setNarrative] = useState('')
  const [ttsUrl, setTtsUrl] = useState('')
  const [busy, setBusy] = useState(false)

  async function handleUploaded(res) {
    setFeatures(res.features)
    setFilename(res.filename)
  }

  async function runAnalyze() {
    if (!filename) return
    setBusy(true)
    try {
      const form = new FormData()
      form.append('audio_filename', filename)
      const resp = await fetch(`${API_BASE}/analyze`, { method: 'POST', body: form })
      const data = await resp.json()
      setNarrative(data.narrative)
      setTtsUrl(`${API_BASE}${data.tts_url}`)
    } catch (e) {
      console.error(e)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="min-h-screen text-gray-900">
      <header className="p-6 border-b bg-white">
        <h1 className="text-2xl font-semibold">BioWhisper</h1>
        <p className="text-sm text-gray-600">Quick check-in for voice and wellness</p>
      </header>
      <main className="max-w-4xl mx-auto p-6 space-y-8">
        <section className="bg-white rounded-xl p-6 shadow">
          <h2 className="text-xl font-medium mb-2">Quick 10s Check-in</h2>
          <RecordButton onUploaded={handleUploaded} />
          {features && (
            <div className="mt-4 text-sm text-gray-700">
              <div>Energy: {features.energy?.toFixed?.(3)}</div>
              <div>Tempo: {features.tempo?.toFixed?.(1)}</div>
              <div>Pitch mean: {features.pitch_mean?.toFixed?.(1)}</div>
              <div>Stress score: {(features.stress_score ?? 0).toFixed(2)}</div>
            </div>
          )}
        </section>

        <section className="bg-white rounded-xl p-6 shadow">
          <h2 className="text-xl font-medium mb-2">Results</h2>
          <button
            className="px-4 py-2 rounded bg-indigo-600 text-white disabled:opacity-50"
            disabled={!filename || busy}
            onClick={runAnalyze}
          >
            {busy ? 'Analyzing…' : 'Analyze'}
          </button>
          {narrative && (
            <div className="mt-4 space-y-3">
              <p className="text-gray-800 whitespace-pre-wrap">{narrative}</p>
              {ttsUrl && (
                <audio controls src={ttsUrl} className="w-full" />
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

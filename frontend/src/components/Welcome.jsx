import { useState } from 'react'
import { FaMicrophone, FaHeart, FaCamera, FaShieldAlt } from 'react-icons/fa'

function Welcome({ onStart }) {
  const [showConsent, setShowConsent] = useState(false)

  const handleStart = () => {
    setShowConsent(true)
  }

  const handleConsent = () => {
    onStart()
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-float">
        <div className="inline-block mb-6">
          <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-2xl">
            <FaHeart className="text-white text-4xl animate-pulse" />
          </div>
        </div>
        
        <h2 className="text-5xl font-bold text-gray-900 mb-4">
          How are you feeling?
        </h2>
        
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Take a 10-second voice check-in and get personalized wellness insights 
          powered by AI analysis of your voice, physiology, and posture.
        </p>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="card text-center hover:scale-105 transition-transform">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FaMicrophone className="text-blue-600 text-2xl" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Voice Analysis</h3>
          <p className="text-gray-600 text-sm">
            Detect stress and emotional tone through vocal patterns
          </p>
        </div>

        <div className="card text-center hover:scale-105 transition-transform">
          <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FaHeart className="text-purple-600 text-2xl" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Wearable Data</h3>
          <p className="text-gray-600 text-sm">
            Import HRV and sleep data for deeper insights
          </p>
        </div>

        <div className="card text-center hover:scale-105 transition-transform">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FaCamera className="text-green-600 text-2xl" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Posture Scan</h3>
          <p className="text-gray-600 text-sm">
            Quick webcam check for tension and alignment
          </p>
        </div>
      </div>

      {/* CTA Button */}
      {!showConsent ? (
        <div className="text-center">
          <button
            onClick={handleStart}
            className="btn-primary text-lg px-12 py-4 inline-flex items-center space-x-3"
          >
            <FaMicrophone className="text-xl" />
            <span>Start 10s Check-in</span>
          </button>
          
          <p className="mt-4 text-sm text-gray-500">
            Takes less than a minute • Privacy-first • No account needed
          </p>
        </div>
      ) : (
        <div className="card max-w-2xl mx-auto border-2 border-blue-200">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <FaShieldAlt className="text-blue-600 text-3xl" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold mb-3">Privacy & Consent</h3>
              <div className="space-y-2 text-sm text-gray-700 mb-6">
                <p>
                  <strong>What we'll use:</strong>
                </p>
                <ul className="list-disc list-inside space-y-1 ml-4">
                  <li>Microphone: 10-second voice recording for analysis</li>
                  <li>Camera (optional): Single posture snapshot</li>
                  <li>Wearable data (optional): CSV upload only</li>
                </ul>
                <p className="mt-4">
                  <strong>Your data:</strong>
                </p>
                <ul className="list-disc list-inside space-y-1 ml-4">
                  <li>Processed locally or on our secure server</li>
                  <li>Not stored permanently (demo mode)</li>
                  <li>Never shared with third parties</li>
                  <li>This is not a medical diagnostic tool</li>
                </ul>
              </div>
              
              <div className="flex space-x-4">
                <button
                  onClick={handleConsent}
                  className="btn-primary flex-1"
                >
                  I Understand, Continue
                </button>
                <button
                  onClick={() => setShowConsent(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* How It Works */}
      <div className="mt-16 max-w-3xl mx-auto">
        <h3 className="text-2xl font-bold text-center mb-8">How It Works</h3>
        
        <div className="space-y-6">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
              1
            </div>
            <div>
              <h4 className="font-semibold">Record Your Voice</h4>
              <p className="text-gray-600">Tell us how you're feeling in 10 seconds</p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
              2
            </div>
            <div>
              <h4 className="font-semibold">AI Analysis</h4>
              <p className="text-gray-600">We analyze voice stress, optional wearable data, and posture</p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
              3
            </div>
            <div>
              <h4 className="font-semibold">Get Personalized Guidance</h4>
              <p className="text-gray-600">Receive compassionate insights and actionable recommendations</p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
              4
            </div>
            <div>
              <h4 className="font-semibold">Listen & Practice</h4>
              <p className="text-gray-600">Play generated breathing exercises and sleep hypnosis audio</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Welcome

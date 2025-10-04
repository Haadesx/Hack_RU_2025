import React from 'react'
import { Link } from 'react-router-dom'
import { Mic, Upload, Camera, Heart, ArrowRight, Shield, Clock } from 'lucide-react'

function Welcome() {
  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Welcome to{' '}
          <span className="wellness-gradient bg-clip-text text-transparent">
            BioWhisper
          </span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Your AI-powered wellness companion that analyzes your voice, biometrics, and posture 
          to provide personalized insights and guided relaxation.
        </p>
        
        <Link
          to="/record"
          className="btn-primary text-lg px-8 py-4 inline-flex items-center space-x-2"
        >
          <Mic className="w-5 h-5" />
          <span>Start Your Wellness Check-in</span>
          <ArrowRight className="w-5 h-5" />
        </Link>
      </div>
      
      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-8 mb-12">
        <div className="card text-center">
          <div className="w-16 h-16 wellness-gradient rounded-full flex items-center justify-center mx-auto mb-4">
            <Mic className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-3">Voice Analysis</h3>
          <p className="text-gray-600">
            Advanced audio processing detects stress levels, energy, and emotional tone 
            from just 10 seconds of your voice.
          </p>
        </div>
        
        <div className="card text-center">
          <div className="w-16 h-16 wellness-gradient rounded-full flex items-center justify-center mx-auto mb-4">
            <Heart className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-3">Biometric Insights</h3>
          <p className="text-gray-600">
            Import wearable data to analyze heart rate variability, sleep patterns, 
            and circadian rhythms for comprehensive wellness assessment.
          </p>
        </div>
        
        <div className="card text-center">
          <div className="w-16 h-16 wellness-gradient rounded-full flex items-center justify-center mx-auto mb-4">
            <Camera className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-3">Posture Scan</h3>
          <p className="text-gray-600">
            AI-powered posture analysis detects tension patterns and provides 
            personalized recommendations for better body alignment.
          </p>
        </div>
      </div>
      
      {/* How It Works */}
      <div className="card mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">How It Works</h2>
        <div className="grid md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center mx-auto mb-3 font-bold text-lg">
              1
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Record</h4>
            <p className="text-sm text-gray-600">Speak for 10 seconds about how you're feeling</p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center mx-auto mb-3 font-bold text-lg">
              2
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Analyze</h4>
            <p className="text-sm text-gray-600">AI processes your voice, biometrics, and posture</p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center mx-auto mb-3 font-bold text-lg">
              3
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Insights</h4>
            <p className="text-sm text-gray-600">Receive personalized wellness insights and recommendations</p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center mx-auto mb-3 font-bold text-lg">
              4
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Relax</h4>
            <p className="text-sm text-gray-600">Listen to guided breathing and relaxation audio</p>
          </div>
        </div>
      </div>
      
      {/* Privacy & Safety */}
      <div className="card bg-gradient-to-r from-wellness-50 to-primary-50 border-wellness-200">
        <div className="flex items-start space-x-4">
          <Shield className="w-8 h-8 text-wellness-600 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Privacy & Safety First</h3>
            <p className="text-gray-600 mb-4">
              Your data stays local and private. We use advanced encryption and never store 
              your personal information. All analysis is done securely with your explicit consent.
            </p>
            <div className="flex items-center space-x-6 text-sm text-gray-500">
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4" />
                <span>Real-time processing</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="w-4 h-4" />
                <span>End-to-end encrypted</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Welcome
import React, { createContext, useContext, useReducer } from 'react'

const WellnessContext = createContext()

const initialState = {
  // Recording state
  isRecording: false,
  audioBlob: null,
  audioFilename: null,
  
  // Analysis data
  audioFeatures: null,
  wearableData: null,
  poseData: null,
  
  // AI insights
  insights: null,
  audioUrls: null,
  
  // UI state
  currentStep: 'welcome',
  isLoading: false,
  error: null,
  
  // User preferences
  preferences: {
    voice: 'alloy',
    notifications: true,
    privacyMode: false
  }
}

function wellnessReducer(state, action) {
  switch (action.type) {
    case 'SET_RECORDING':
      return { ...state, isRecording: action.payload }
    
    case 'SET_AUDIO_DATA':
      return { 
        ...state, 
        audioBlob: action.payload.blob,
        audioFilename: action.payload.filename 
      }
    
    case 'SET_AUDIO_FEATURES':
      return { ...state, audioFeatures: action.payload }
    
    case 'SET_WEARABLE_DATA':
      return { ...state, wearableData: action.payload }
    
    case 'SET_POSE_DATA':
      return { ...state, poseData: action.payload }
    
    case 'SET_INSIGHTS':
      return { 
        ...state, 
        insights: action.payload.insights,
        audioUrls: action.payload.audioUrls 
      }
    
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload }
    
    case 'SET_ERROR':
      return { ...state, error: action.payload }
    
    case 'SET_STEP':
      return { ...state, currentStep: action.payload }
    
    case 'RESET_ANALYSIS':
      return {
        ...state,
        audioBlob: null,
        audioFilename: null,
        audioFeatures: null,
        wearableData: null,
        poseData: null,
        insights: null,
        audioUrls: null,
        error: null
      }
    
    case 'UPDATE_PREFERENCES':
      return {
        ...state,
        preferences: { ...state.preferences, ...action.payload }
      }
    
    default:
      return state
  }
}

export function WellnessProvider({ children }) {
  const [state, dispatch] = useReducer(wellnessReducer, initialState)
  
  const value = {
    state,
    dispatch,
    
    // Action helpers
    startRecording: () => dispatch({ type: 'SET_RECORDING', payload: true }),
    stopRecording: () => dispatch({ type: 'SET_RECORDING', payload: false }),
    
    setAudioData: (blob, filename) => 
      dispatch({ type: 'SET_AUDIO_DATA', payload: { blob, filename } }),
    
    setAudioFeatures: (features) => 
      dispatch({ type: 'SET_AUDIO_FEATURES', payload: features }),
    
    setWearableData: (data) => 
      dispatch({ type: 'SET_WEARABLE_DATA', payload: data }),
    
    setPoseData: (data) => 
      dispatch({ type: 'SET_POSE_DATA', payload: data }),
    
    setInsights: (insights, audioUrls) => 
      dispatch({ type: 'SET_INSIGHTS', payload: { insights, audioUrls } }),
    
    setLoading: (loading) => 
      dispatch({ type: 'SET_LOADING', payload: loading }),
    
    setError: (error) => 
      dispatch({ type: 'SET_ERROR', payload: error }),
    
    setStep: (step) => 
      dispatch({ type: 'SET_STEP', payload: step }),
    
    resetAnalysis: () => 
      dispatch({ type: 'RESET_ANALYSIS' }),
    
    updatePreferences: (prefs) => 
      dispatch({ type: 'UPDATE_PREFERENCES', payload: prefs })
  }
  
  return (
    <WellnessContext.Provider value={value}>
      {children}
    </WellnessContext.Provider>
  )
}

export function useWellness() {
  const context = useContext(WellnessContext)
  if (!context) {
    throw new Error('useWellness must be used within a WellnessProvider')
  }
  return context
}
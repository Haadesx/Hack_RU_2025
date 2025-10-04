import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Welcome from './components/Welcome'
import Recording from './components/Recording'
import Analysis from './components/Analysis'
import Dashboard from './components/Dashboard'
import { WellnessProvider } from './context/WellnessContext'

function App() {
  return (
    <WellnessProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-wellness-50 to-primary-50">
          <Header />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Welcome />} />
              <Route path="/record" element={<Recording />} />
              <Route path="/analysis" element={<Analysis />} />
              <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
          </main>
        </div>
      </Router>
    </WellnessProvider>
  )
}

export default App
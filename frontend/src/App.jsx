import React, { useState, useEffect } from 'react'
import ChatInterface from './components/ChatInterface'
import './App.css'

function App() {
  const [particles, setParticles] = useState([])

  useEffect(() => {
    // Generate floating particles
    const newParticles = Array.from({ length: 20 }, (_, i) => ({
      id: i,
      size: Math.random() * 60 + 20,
      left: Math.random() * 100,
      top: Math.random() * 100,
      duration: Math.random() * 10 + 5,
      delay: Math.random() * 5,
      color: ['#667eea', '#764ba2', '#f093fb', '#4facfe'][Math.floor(Math.random() * 4)]
    }))
    setParticles(newParticles)
  }, [])

  return (
    <div className="min-h-screen animated-gradient relative overflow-hidden">
      {/* Floating Particles */}
      {particles.map(particle => (
        <div
          key={particle.id}
          className="particle"
          style={{
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            left: `${particle.left}%`,
            top: `${particle.top}%`,
            background: particle.color,
            animationDuration: `${particle.duration}s`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(40px)'
          }}
        />
      ))}

      <div className="container mx-auto h-screen flex flex-col relative z-10">
        {/* Header */}
        <header className="glass-morphism-strong shadow-2xl border-b border-white/20">
          <div className="px-8 py-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  Personal Assistant
                </h1>
                <p className="text-sm text-gray-600 mt-1 font-medium">
                  ✨ AI-powered intelligence at your fingertips
                </p>
              </div>
            </div>
          </div>
        </header>

        {/* Chat Interface */}
        <main className="flex-1 overflow-hidden p-6">
          <ChatInterface />
        </main>
      </div>
    </div>
  )
}

export default App

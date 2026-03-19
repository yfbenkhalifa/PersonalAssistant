import React, { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto h-screen flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <div className="px-6 py-4">
            <h1 className="text-2xl font-bold text-gray-800">
              Personal Assistant
            </h1>
            <p className="text-sm text-gray-600 mt-1">
              AI-powered assistant to help you with your tasks
            </p>
          </div>
        </header>

        {/* Chat Interface */}
        <main className="flex-1 overflow-hidden p-4">
          <ChatInterface />
        </main>
      </div>
    </div>
  )
}

export default App

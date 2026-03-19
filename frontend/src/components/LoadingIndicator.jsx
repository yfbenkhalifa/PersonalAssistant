import React from 'react'
import { Sparkles } from 'lucide-react'

const LoadingIndicator = () => {
  return (
    <div className="flex gap-4 message-enter">
      {/* Avatar */}
      <div className="flex-shrink-0 w-10 h-10 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-lg animate-pulse">
        <Sparkles className="w-5 h-5 text-white" />
      </div>

      {/* Loading Animation */}
      <div className="bg-white/90 backdrop-blur-sm border border-gray-200 rounded-3xl px-6 py-4 shadow-lg">
        <div className="flex gap-2 items-center">
          <div className="w-3 h-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-3 h-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-3 h-3 bg-gradient-to-br from-pink-500 to-red-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          <span className="text-sm text-gray-600 ml-2 font-medium">Thinking...</span>
        </div>
      </div>
    </div>
  )
}

export default LoadingIndicator

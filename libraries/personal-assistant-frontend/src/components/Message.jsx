import React from 'react'
import { User, Bot, Sparkles } from 'lucide-react'

const Message = ({ message }) => {
  const isUser = message.role === 'user'
  const isError = message.isError

  return (
    <div className={`flex gap-4 message-enter ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-10 h-10 rounded-2xl flex items-center justify-center shadow-lg transition-transform hover:scale-110 ${
        isUser 
          ? 'bg-gradient-to-br from-indigo-500 to-purple-600' 
          : isError 
          ? 'bg-gradient-to-br from-red-500 to-pink-600' 
          : 'bg-gradient-to-br from-purple-500 to-pink-600'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : isError ? (
          <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        ) : (
          <Sparkles className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex flex-col max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`rounded-3xl px-5 py-3 shadow-lg transition-all hover:shadow-xl ${
          isUser 
            ? 'bg-gradient-to-br from-indigo-500 to-purple-600 text-white' 
            : isError 
            ? 'bg-gradient-to-br from-red-50 to-pink-50 text-red-900 border-2 border-red-200'
            : 'bg-white/90 backdrop-blur-sm text-gray-800 border border-gray-200'
        }`}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap break-words font-medium">{message.content}</p>
        </div>
        <span className="text-xs text-gray-500 mt-2 px-2 font-medium">
          {new Date(message.timestamp).toLocaleTimeString()}
        </span>
      </div>
    </div>
  )
}

export default Message

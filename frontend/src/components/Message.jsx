import React from 'react'
import { User, Bot } from 'lucide-react'

const Message = ({ message }) => {
  const isUser = message.role === 'user'
  const isError = message.isError

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-blue-500' : isError ? 'bg-red-500' : 'bg-gray-700'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex flex-col max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`rounded-2xl px-4 py-2 ${
          isUser 
            ? 'bg-blue-500 text-white' 
            : isError 
            ? 'bg-red-50 text-red-900 border border-red-200'
            : 'bg-gray-100 text-gray-900'
        }`}>
          <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>
        </div>
        <span className="text-xs text-gray-400 mt-1 px-2">
          {new Date(message.timestamp).toLocaleTimeString()}
        </span>
      </div>
    </div>
  )
}

export default Message

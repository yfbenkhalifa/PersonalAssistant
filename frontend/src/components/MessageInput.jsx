import React, { useState, useRef } from 'react'
import { Send } from 'lucide-react'

const MessageInput = ({ onSend, disabled }) => {
  const [input, setInput] = useState('')
  const textareaRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSend(input)
      setInput('')
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleInput = (e) => {
    setInput(e.target.value)
    // Auto-resize textarea
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px'
    }
  }

  return (
    <div className="border-t border-gray-200/50 p-6 bg-gradient-to-br from-gray-50/50 to-white/50 backdrop-blur-sm">
      <form onSubmit={handleSubmit} className="flex gap-3 items-end">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="✨ Type your message... (Shift+Enter for new line)"
          disabled={disabled}
          rows={1}
          className="flex-1 resize-none rounded-2xl border-2 border-gray-200 px-5 py-4 focus:outline-none focus:ring-4 focus:ring-indigo-200 focus:border-indigo-400 disabled:bg-gray-50 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg bg-white font-medium"
          style={{ maxHeight: '200px' }}
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="flex-shrink-0 bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-2xl px-6 py-4 hover:from-indigo-600 hover:to-purple-700 focus:outline-none focus:ring-4 focus:ring-indigo-200 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl hover:scale-105 active:scale-95"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>
    </div>
  )
}

export default MessageInput

import React, { useState, useRef, useEffect } from 'react'
import { sendMessage } from '../services/api'
import MessageList from './MessageList'
import MessageInput from './MessageInput'

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m your Personal Assistant. How can I help you today?',
      timestamp: new Date().toISOString()
    }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId] = useState(() => `conv_${Date.now()}`)

  const handleSendMessage = async (content) => {
    if (!content.trim()) return

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: content,
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Send to API
      const response = await sendMessage(content, conversationId)
      
      // Add assistant response
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}`,
        timestamp: new Date().toISOString(),
        isError: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-full flex flex-col bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Messages Container */}
      <MessageList messages={messages} isLoading={isLoading} />
      
      {/* Input Area */}
      <MessageInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  )
}

export default ChatInterface

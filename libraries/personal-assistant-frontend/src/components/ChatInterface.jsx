import React, { useState } from 'react'
import { sendMessage } from '../services/api'
import MessageList from './MessageList'
import MessageInput from './MessageInput'

const ChatInterface = ({
  sendMessageHandler = sendMessage,
  initialAssistantMessage = 'Hello! I\'m your Personal Assistant. How can I help you today?',
  conversationId: providedConversationId = null,
  className = '',
}) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: initialAssistantMessage,
      timestamp: new Date().toISOString()
    }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId] = useState(() => providedConversationId || `conv_${Date.now()}`)

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
      const response = await sendMessageHandler(content, conversationId)
      
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
    <div className={`h-full flex flex-col glass-morphism-strong rounded-3xl shadow-2xl overflow-hidden glow-effect hover-lift border border-white/30 ${className}`.trim()}>
      {/* Messages Container */}
      <MessageList messages={messages} isLoading={isLoading} />
      
      {/* Input Area */}
      <MessageInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  )
}

export default ChatInterface

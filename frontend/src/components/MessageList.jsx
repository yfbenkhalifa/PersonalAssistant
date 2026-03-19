import React, { useRef, useEffect } from 'react'
import Message from './Message'
import LoadingIndicator from './LoadingIndicator'

const MessageList = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide">
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
      {isLoading && <LoadingIndicator />}
      <div ref={messagesEndRef} />
    </div>
  )
}

export default MessageList

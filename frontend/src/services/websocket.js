/**
 * WebSocket service for real-time chat communication
 */
class WebSocketService {
  constructor() {
    this.ws = null
    this.conversationId = null
    this.messageHandlers = []
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
  }

  /**
   * Connect to WebSocket server
   * @param {string} conversationId - Conversation ID
   */
  connect(conversationId) {
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
    this.conversationId = conversationId
    
    try {
      this.ws = new WebSocket(`${wsUrl}/ws/${conversationId}`)
      
      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0
      }
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          this.notifyHandlers(data)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      
      this.ws.onclose = () => {
        console.log('WebSocket disconnected')
        this.attemptReconnect()
      }
    } catch (error) {
      console.error('Error connecting to WebSocket:', error)
    }
  }

  /**
   * Attempt to reconnect to WebSocket
   */
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`)
      
      setTimeout(() => {
        if (this.conversationId) {
          this.connect(this.conversationId)
        }
      }, this.reconnectDelay * this.reconnectAttempts)
    }
  }

  /**
   * Send a message through WebSocket
   * @param {string} message - Message to send
   */
  sendMessage(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ message }))
    } else {
      console.error('WebSocket is not connected')
    }
  }

  /**
   * Register a message handler
   * @param {Function} handler - Handler function
   */
  onMessage(handler) {
    this.messageHandlers.push(handler)
  }

  /**
   * Notify all registered handlers
   * @param {Object} data - Message data
   */
  notifyHandlers(data) {
    this.messageHandlers.forEach(handler => handler(data))
  }

  /**
   * Disconnect from WebSocket
   */
  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.messageHandlers = []
  }

  /**
   * Check if WebSocket is connected
   * @returns {boolean}
   */
  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN
  }
}

// Export singleton instance
export default new WebSocketService()

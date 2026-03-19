import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Send a chat message to the API
 * @param {string} message - The message to send
 * @param {string} conversationId - Optional conversation ID
 * @returns {Promise} Response from the API
 */
export const sendMessage = async (message, conversationId = null) => {
  try {
    const response = await api.post('/api/chat', {
      message,
      conversation_id: conversationId,
    })
    return response.data
  } catch (error) {
    console.error('Error sending message:', error)
    throw error
  }
}

/**
 * Clear a conversation
 * @param {string} conversationId - The conversation ID to clear
 * @returns {Promise} Response from the API
 */
export const clearConversation = async (conversationId) => {
  try {
    const response = await api.delete(`/api/chat/${conversationId}`)
    return response.data
  } catch (error) {
    console.error('Error clearing conversation:', error)
    throw error
  }
}

/**
 * Check API health
 * @returns {Promise} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Error checking health:', error)
    throw error
  }
}

export default api

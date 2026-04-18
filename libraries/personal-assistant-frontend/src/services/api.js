import axios from 'axios'

const DEFAULT_API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const createApiClient = (baseURL = DEFAULT_API_BASE_URL) => axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
})

let api = createApiClient()

export const setApiBaseUrl = (baseURL) => {
  api = createApiClient(baseURL)
  return api
}

export const getApiClient = () => api

/**
 * Send a chat message to the API
 * @param {string} message - The message to send
 * @param {string} conversationId - Optional conversation ID
 * @returns {Promise} Response from the API
 */
export const sendMessage = async (message, conversationId = null) => {
  try {
    const response = await getApiClient().post('/api/chat', {
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
    const response = await getApiClient().delete(`/api/chat/${conversationId}`)
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
    const response = await getApiClient().get('/health')
    return response.data
  } catch (error) {
    console.error('Error checking health:', error)
    throw error
  }
}


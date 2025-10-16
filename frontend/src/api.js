import axios from 'axios'

// Use environment variable or fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // Disable credentials for CORS
})

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.config?.url, error.message)
    return Promise.reject(error)
  }
)

const api = {
  // Stats
  getStats: () => apiClient.get('/api/stats'),

  // Channels
  getChannels: () => apiClient.get('/api/channels'),
  createChannel: (name, username) => 
    apiClient.post('/api/channels', { name, username }),
  startChannel: (id) => apiClient.post(`/api/channels/${id}/start`),
  stopChannel: (id) => apiClient.post(`/api/channels/${id}/stop`),
  deleteChannel: (id) => apiClient.delete(`/api/channels/${id}`),

  // Signals
  getSignals: (channelId = null, limit = 50) => {
    const params = { limit }
    if (channelId) params.channel_id = channelId
    return apiClient.get('/api/signals', { params })
  },
  getRecentSignals: () => apiClient.get('/api/signals/recent'),
}

export default api

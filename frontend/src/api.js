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
})

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

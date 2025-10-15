import { useState, useEffect } from 'react'
import { Activity, TrendingUp, Radio, AlertCircle } from 'lucide-react'
import ChannelList from './components/ChannelList'
import AddChannelModal from './components/AddChannelModal'
import SignalList from './components/SignalList'
import Stats from './components/Stats'
import api from './api'

function App() {
  const [channels, setChannels] = useState([])
  const [signals, setSignals] = useState([])
  const [stats, setStats] = useState({
    total_channels: 0,
    active_channels: 0,
    total_signals: 0,
    signals_today: 0
  })
  const [showAddModal, setShowAddModal] = useState(false)
  const [loading, setLoading] = useState(true)
  const [selectedChannelId, setSelectedChannelId] = useState(null)

  // Fetch data on mount
  useEffect(() => {
    fetchData()
    // Refresh every 5 seconds
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [selectedChannelId])

  const fetchData = async () => {
    try {
      const [channelsRes, signalsRes, statsRes] = await Promise.all([
        api.getChannels(),
        api.getSignals(selectedChannelId),
        api.getStats()
      ])
      setChannels(channelsRes.data)
      setSignals(signalsRes.data)
      setStats(statsRes.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  const handleAddChannel = async (name, username) => {
    try {
      await api.createChannel(name, username)
      fetchData()
      setShowAddModal(false)
    } catch (error) {
      console.error('Error adding channel:', error)
      alert(error.response?.data?.detail || 'Error adding channel')
    }
  }

  const handleStartChannel = async (channelId) => {
    try {
      await api.startChannel(channelId)
      fetchData()
    } catch (error) {
      console.error('Error starting channel:', error)
      alert(error.response?.data?.detail || 'Error starting channel')
    }
  }

  const handleStopChannel = async (channelId) => {
    try {
      await api.stopChannel(channelId)
      fetchData()
    } catch (error) {
      console.error('Error stopping channel:', error)
    }
  }

  const handleDeleteChannel = async (channelId) => {
    if (!confirm('Are you sure you want to delete this channel?')) return
    
    try {
      await api.deleteChannel(channelId)
      fetchData()
    } catch (error) {
      console.error('Error deleting channel:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
      {/* Header */}
      <header className="bg-black bg-opacity-30 backdrop-blur-md border-b border-gray-700">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="w-8 h-8 text-blue-400" />
              <h1 className="text-2xl font-bold text-white">Telegram Trading Bot</h1>
            </div>
            <button
              onClick={() => setShowAddModal(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
            >
              <span>+ Add Channel</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        {/* Stats Cards */}
        <Stats stats={stats} />

        {/* Channels and Signals Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
          {/* Channels List */}
          <div className="lg:col-span-1">
            <ChannelList
              channels={channels}
              onStart={handleStartChannel}
              onStop={handleStopChannel}
              onDelete={handleDeleteChannel}
              selectedChannelId={selectedChannelId}
              onSelectChannel={setSelectedChannelId}
            />
          </div>

          {/* Signals List */}
          <div className="lg:col-span-2">
            <SignalList signals={signals} selectedChannelId={selectedChannelId} />
          </div>
        </div>
      </div>

      {/* Add Channel Modal */}
      {showAddModal && (
        <AddChannelModal
          onClose={() => setShowAddModal(false)}
          onAdd={handleAddChannel}
        />
      )}
    </div>
  )
}

export default App

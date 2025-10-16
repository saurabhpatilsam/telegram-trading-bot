import React, { useState, useEffect } from 'react'
import { Bot, Plus, AlertCircle } from 'lucide-react'
import api from './api'
import { Button } from './components/ui/button'
import { Card, CardContent } from './components/ui/card'
import Stats from './components/Stats'
import ChannelList from './components/ChannelList'
import SignalList from './components/SignalList'
import AddChannelModal from './components/AddChannelModal'

function App() {
  const [stats, setStats] = useState({
    total_channels: 0,
    active_channels: 0,
    total_signals: 0,
    signals_today: 0
  })
  const [channels, setChannels] = useState([])
  const [signals, setSignals] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      const [statsRes, channelsRes, signalsRes] = await Promise.all([
        api.getStats(),
        api.getChannels(),
        api.getSignals(null, 20)
      ])
      
      setStats(statsRes.data)
      setChannels(channelsRes.data)
      setSignals(signalsRes.data)
      setError(null)
    } catch (err) {
      console.error('Error fetching data:', err)
      setError('Failed to fetch data. Please check if the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const handleAddChannel = async (name, username) => {
    try {
      await api.createChannel(name, username)
      fetchData() // Refresh data
      setIsModalOpen(false)
    } catch (err) {
      console.error('Error adding channel:', err)
      alert('Failed to add channel')
    }
  }

  const handleStartChannel = async (id) => {
    try {
      await api.startChannel(id)
      fetchData() // Refresh data
    } catch (err) {
      console.error('Error starting channel:', err)
      alert('Failed to start channel')
    }
  }

  const handleStopChannel = async (id) => {
    try {
      await api.stopChannel(id)
      fetchData() // Refresh data
    } catch (err) {
      console.error('Error stopping channel:', err)
      alert('Failed to stop channel')
    }
  }

  const handleDeleteChannel = async (id) => {
    if (window.confirm('Are you sure you want to delete this channel?')) {
      try {
        await api.deleteChannel(id)
        fetchData() // Refresh data
      } catch (err) {
        console.error('Error deleting channel:', err)
        alert('Failed to delete channel')
      }
    }
  }

  if (loading && channels.length === 0) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-primary rounded-lg">
                <Bot className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  Telegram Trading Bot
                </h1>
                <p className="text-sm text-muted-foreground">
                  AI-powered signal monitoring dashboard
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-1 text-sm text-muted-foreground">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>Live</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        {/* Error Message */}
        {error && (
          <Card className="mb-6 border-destructive">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2 text-destructive">
                <AlertCircle className="h-5 w-5" />
                <div>
                  <p className="font-medium">Connection Error</p>
                  <p className="text-sm text-muted-foreground mt-1">{error}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Stats */}
        <Stats stats={stats} />

        {/* Main Content */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mt-8">
          {/* Channels Section */}
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-foreground">Channels</h2>
                <p className="text-sm text-muted-foreground">
                  Manage your Telegram channel monitoring
                </p>
              </div>
              <Button onClick={() => setIsModalOpen(true)} className="gap-2">
                <Plus className="h-4 w-4" />
                Add Channel
              </Button>
            </div>
            <ChannelList
              channels={channels}
              onStart={handleStartChannel}
              onStop={handleStopChannel}
              onDelete={handleDeleteChannel}
            />
          </div>

          {/* Signals Section */}
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-foreground">Recent Signals</h2>
              <p className="text-sm text-muted-foreground">
                Latest trading signals from monitored channels
              </p>
            </div>
            <SignalList signals={signals} />
          </div>
        </div>
      </main>

      {/* Add Channel Modal */}
      <AddChannelModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onAdd={handleAddChannel}
      />
    </div>
  )
}

export default App

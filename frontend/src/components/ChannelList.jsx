import { Play, Square, Trash2, Radio, AlertCircle } from 'lucide-react'

export default function ChannelList({ channels, onStart, onStop, onDelete, selectedChannelId, onSelectChannel }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'bg-green-500'
      case 'stopped':
        return 'bg-gray-500'
      case 'error':
        return 'bg-red-500'
      default:
        return 'bg-gray-500'
    }
  }

  return (
    <div className="bg-white bg-opacity-5 backdrop-blur-lg rounded-xl border border-gray-700 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-700">
        <h2 className="text-xl font-semibold text-white flex items-center">
          <Radio className="w-5 h-5 mr-2" />
          Telegram Channels
        </h2>
      </div>

      <div className="divide-y divide-gray-700 max-h-[600px] overflow-y-auto">
        {channels.length === 0 ? (
          <div className="p-8 text-center text-gray-400">
            No channels added yet. Click "Add Channel" to get started.
          </div>
        ) : (
          channels.map((channel) => (
            <div
              key={channel.id}
              className={`p-4 hover:bg-white hover:bg-opacity-5 transition-colors cursor-pointer ${
                selectedChannelId === channel.id ? 'bg-blue-500 bg-opacity-10' : ''
              }`}
              onClick={() => onSelectChannel(channel.id === selectedChannelId ? null : channel.id)}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center mb-1">
                    <span className={`w-2 h-2 rounded-full ${getStatusColor(channel.status)} mr-2`}></span>
                    <h3 className="text-white font-medium">{channel.name}</h3>
                  </div>
                  <p className="text-gray-400 text-sm">{channel.username}</p>
                  <div className="flex items-center mt-2 text-xs text-gray-500">
                    <span className="mr-3">Signals: {channel.total_signals}</span>
                    <span className="capitalize">{channel.status}</span>
                  </div>
                </div>
              </div>

              {channel.error_message && (
                <div className="mb-3 flex items-start text-xs text-red-400 bg-red-500 bg-opacity-10 p-2 rounded">
                  <AlertCircle className="w-4 h-4 mr-1 flex-shrink-0 mt-0.5" />
                  <span>{channel.error_message}</span>
                </div>
              )}

              <div className="flex items-center space-x-2">
                {channel.status === 'running' ? (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      onStop(channel.id)
                    }}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg text-sm transition-colors flex items-center justify-center"
                  >
                    <Square className="w-4 h-4 mr-1" />
                    Stop
                  </button>
                ) : (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      onStart(channel.id)
                    }}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-lg text-sm transition-colors flex items-center justify-center"
                  >
                    <Play className="w-4 h-4 mr-1" />
                    Start
                  </button>
                )}

                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    onDelete(channel.id)
                  }}
                  className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-2 rounded-lg text-sm transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

import { TrendingUp, TrendingDown, Clock, Target, Shield } from 'lucide-react'

export default function SignalList({ signals, selectedChannelId }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  return (
    <div className="bg-white bg-opacity-5 backdrop-blur-lg rounded-xl border border-gray-700 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-700">
        <h2 className="text-xl font-semibold text-white flex items-center">
          <TrendingUp className="w-5 h-5 mr-2" />
          Trading Signals {selectedChannelId && <span className="ml-2 text-sm text-gray-400">(Filtered)</span>}
        </h2>
      </div>

      <div className="max-h-[600px] overflow-y-auto">
        {signals.length === 0 ? (
          <div className="p-8 text-center text-gray-400">
            No signals detected yet. Start monitoring channels to see signals.
          </div>
        ) : (
          <div className="divide-y divide-gray-700">
            {signals.map((signal) => (
              <div key={signal.id} className="p-6 hover:bg-white hover:bg-opacity-5 transition-colors">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${
                      signal.action === 'BUY' 
                        ? 'bg-green-500 bg-opacity-20' 
                        : 'bg-red-500 bg-opacity-20'
                    }`}>
                      {signal.action === 'BUY' ? (
                        <TrendingUp className="w-5 h-5 text-green-400" />
                      ) : (
                        <TrendingDown className="w-5 h-5 text-red-400" />
                      )}
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <h3 className={`text-lg font-bold ${
                          signal.action === 'BUY' ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {signal.action}
                        </h3>
                        <span className="text-xl font-bold text-white">{signal.instrument}</span>
                      </div>
                      <p className="text-sm text-gray-400">{signal.channel_name}</p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <span className={`inline-block px-2 py-1 rounded text-xs ${
                      signal.signal_type === 'image' 
                        ? 'bg-purple-500 bg-opacity-20 text-purple-400' 
                        : 'bg-blue-500 bg-opacity-20 text-blue-400'
                    }`}>
                      {signal.signal_type}
                    </span>
                  </div>
                </div>

                {/* Signal Details */}
                <div className="grid grid-cols-3 gap-4 mb-4">
                  {signal.entry_price && signal.entry_price !== '' && (
                    <div className="bg-white bg-opacity-5 rounded-lg p-3">
                      <div className="flex items-center text-gray-400 text-xs mb-1">
                        <Target className="w-3 h-3 mr-1" />
                        Entry
                      </div>
                      <div className="text-white font-semibold">{signal.entry_price}</div>
                    </div>
                  )}

                  {signal.stop_loss && signal.stop_loss !== '' && (
                    <div className="bg-white bg-opacity-5 rounded-lg p-3">
                      <div className="flex items-center text-gray-400 text-xs mb-1">
                        <Shield className="w-3 h-3 mr-1" />
                        Stop Loss
                      </div>
                      <div className="text-red-400 font-semibold">{signal.stop_loss}</div>
                    </div>
                  )}

                  {signal.take_profits && signal.take_profits.length > 0 && (
                    <div className="bg-white bg-opacity-5 rounded-lg p-3">
                      <div className="flex items-center text-gray-400 text-xs mb-1">
                        <TrendingUp className="w-3 h-3 mr-1" />
                        Take Profit
                      </div>
                      <div className="text-green-400 font-semibold">
                        {signal.take_profits.slice(0, 2).join(', ')}
                        {signal.take_profits.length > 2 && ' ...'}
                      </div>
                    </div>
                  )}
                </div>

                {/* Timestamp */}
                <div className="flex items-center text-xs text-gray-500">
                  <Clock className="w-3 h-3 mr-1" />
                  {formatDate(signal.created_at)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

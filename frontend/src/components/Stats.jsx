import { Radio, TrendingUp, Activity, AlertCircle } from 'lucide-react'

export default function Stats({ stats }) {
  const statCards = [
    {
      title: 'Total Channels',
      value: stats.total_channels,
      icon: Radio,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500 bg-opacity-10'
    },
    {
      title: 'Active Channels',
      value: stats.active_channels,
      icon: Activity,
      color: 'text-green-400',
      bgColor: 'bg-green-500 bg-opacity-10'
    },
    {
      title: 'Total Signals',
      value: stats.total_signals,
      icon: TrendingUp,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500 bg-opacity-10'
    },
    {
      title: 'Signals Today',
      value: stats.signals_today,
      icon: AlertCircle,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500 bg-opacity-10'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((stat, index) => {
        const Icon = stat.icon
        return (
          <div
            key={index}
            className="bg-white bg-opacity-5 backdrop-blur-lg rounded-xl p-6 border border-gray-700 hover:border-gray-600 transition-all"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm mb-1">{stat.title}</p>
                <p className="text-3xl font-bold text-white">{stat.value}</p>
              </div>
              <div className={`${stat.bgColor} p-3 rounded-lg`}>
                <Icon className={`w-6 h-6 ${stat.color}`} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

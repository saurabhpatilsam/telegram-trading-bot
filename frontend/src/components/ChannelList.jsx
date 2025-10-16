import React from 'react'
import { Play, Square, Trash2, MessageCircle, BarChart3 } from 'lucide-react'
import { Card, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'

function ChannelList({ channels, onStart, onStop, onDelete }) {
  if (channels.length === 0) {
    return (
      <Card className="p-8 text-center">
        <div className="text-muted-foreground mb-4">
          <MessageCircle className="w-12 h-12 mx-auto" />
        </div>
        <h3 className="text-lg font-medium text-foreground mb-2">
          No channels added yet
        </h3>
        <p className="text-muted-foreground">
          Add your first Telegram channel to start monitoring trading signals.
        </p>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {channels.map((channel) => (
        <Card key={channel.id} className="transition-all duration-200 hover:shadow-md">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex-1 space-y-3">
                <div>
                  <h3 className="text-lg font-semibold text-foreground">
                    {channel.name}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {channel.username}
                  </p>
                </div>
                
                <div className="flex items-center space-x-4">
                  <Badge 
                    variant={channel.is_active ? 'success' : 'secondary'}
                    className="gap-1"
                  >
                    <div className={`w-2 h-2 rounded-full ${
                      channel.is_active ? 'bg-green-500' : 'bg-gray-400'
                    }`} />
                    {channel.is_active ? 'Active' : 'Stopped'}
                  </Badge>
                  
                  <div className="flex items-center text-sm text-muted-foreground gap-1">
                    <BarChart3 className="h-4 w-4" />
                    <span>{channel.signal_count || 0} signals</span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2 ml-4">
                {channel.is_active ? (
                  <Button
                    onClick={() => onStop(channel.id)}
                    variant="outline"
                    size="sm"
                    className="gap-2 text-red-600 border-red-200 hover:bg-red-50"
                  >
                    <Square className="h-4 w-4" />
                    Stop
                  </Button>
                ) : (
                  <Button
                    onClick={() => onStart(channel.id)}
                    variant="outline"
                    size="sm"
                    className="gap-2 text-green-600 border-green-200 hover:bg-green-50"
                  >
                    <Play className="h-4 w-4" />
                    Start
                  </Button>
                )}
                
                <Button
                  onClick={() => onDelete(channel.id)}
                  variant="outline"
                  size="sm"
                  className="gap-2 text-red-600 border-red-200 hover:bg-red-50"
                >
                  <Trash2 className="h-4 w-4" />
                  Delete
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

export default ChannelList

import React from 'react'
import { TrendingUp, TrendingDown, DollarSign, Shield, Target, Clock } from 'lucide-react'
import { Card, CardContent, CardHeader } from './ui/card'
import { Badge } from './ui/badge'
import { formatDate } from '../lib/utils'

function SignalList({ signals }) {
  if (signals.length === 0) {
    return (
      <Card className="p-8 text-center">
        <div className="text-muted-foreground mb-4">
          <TrendingUp className="w-12 h-12 mx-auto" />
        </div>
        <h3 className="text-lg font-medium text-foreground mb-2">
          No signals yet
        </h3>
        <p className="text-muted-foreground">
          Trading signals will appear here when channels are active.
        </p>
      </Card>
    )
  }

  const getSignalIcon = (action) => {
    if (action === 'BUY' || action === 'LONG') {
      return <TrendingUp className="h-4 w-4" />
    }
    if (action === 'SELL' || action === 'SHORT') {
      return <TrendingDown className="h-4 w-4" />
    }
    return <TrendingUp className="h-4 w-4" />
  }

  const getSignalVariant = (action) => {
    if (action === 'BUY' || action === 'LONG') return 'success'
    if (action === 'SELL' || action === 'SHORT') return 'destructive'
    return 'secondary'
  }

  return (
    <div className="space-y-4 max-h-[600px] overflow-y-auto">
      {signals.map((signal, index) => (
        <Card key={index} className="transition-all duration-200 hover:shadow-md">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Badge 
                  variant={getSignalVariant(signal.action)}
                  className="gap-1"
                >
                  {getSignalIcon(signal.action)}
                  {signal.action || 'UNKNOWN'}
                </Badge>
                <h3 className="text-lg font-semibold text-foreground">
                  {signal.instrument || 'Unknown Instrument'}
                </h3>
              </div>
              <div className="flex items-center text-sm text-muted-foreground gap-1">
                <Clock className="h-4 w-4" />
                <span>
                  {signal.message_date ? formatDate(signal.message_date) : 'Unknown time'}
                </span>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {signal.entry_price && (
                <div className="space-y-1">
                  <div className="flex items-center gap-1 text-sm font-medium text-muted-foreground">
                    <DollarSign className="h-4 w-4" />
                    <span>Entry Price</span>
                  </div>
                  <p className="text-lg font-semibold text-foreground">
                    {signal.entry_price}
                  </p>
                </div>
              )}
              
              {signal.stop_loss && (
                <div className="space-y-1">
                  <div className="flex items-center gap-1 text-sm font-medium text-muted-foreground">
                    <Shield className="h-4 w-4" />
                    <span>Stop Loss</span>
                  </div>
                  <p className="text-lg font-semibold text-red-600">
                    {signal.stop_loss}
                  </p>
                </div>
              )}
              
              {signal.take_profits && signal.take_profits.length > 0 && (
                <div className="space-y-1">
                  <div className="flex items-center gap-1 text-sm font-medium text-muted-foreground">
                    <Target className="h-4 w-4" />
                    <span>Take Profit</span>
                  </div>
                  <p className="text-lg font-semibold text-green-600">
                    {Array.isArray(signal.take_profits) 
                      ? signal.take_profits.join(', ') 
                      : signal.take_profits}
                  </p>
                </div>
              )}
            </div>
            
            {signal.raw_text && (
              <div className="bg-muted rounded-lg p-4">
                <p className="text-sm font-medium text-muted-foreground mb-2">
                  Original Message
                </p>
                <p className="text-sm text-foreground whitespace-pre-wrap">
                  {signal.raw_text}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

export default SignalList

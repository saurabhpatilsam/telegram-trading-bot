import React, { useState } from 'react'
import { Plus, MessageCircle } from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from './ui/dialog'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'

function AddChannelModal({ isOpen, onClose, onAdd }) {
  const [name, setName] = useState('')
  const [username, setUsername] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim() || !username.trim()) {
      alert('Please fill in all fields')
      return
    }

    setLoading(true)
    try {
      await onAdd(name.trim(), username.trim())
      setName('')
      setUsername('')
    } catch (error) {
      console.error('Error adding channel:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <MessageCircle className="h-5 w-5" />
            Add Telegram Channel
          </DialogTitle>
          <DialogDescription>
            Add a new Telegram channel to monitor for trading signals.
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Channel Name</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Forex Signals Pro"
              disabled={loading}
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="username">Channel Username/Link</Label>
            <Input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="@channelname or https://t.me/channelname"
              disabled={loading}
            />
          </div>
          
          <DialogFooter className="gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={loading || !name.trim() || !username.trim()}
              className="gap-2"
            >
              {loading ? (
                'Adding...'
              ) : (
                <>
                  <Plus className="h-4 w-4" />
                  Add Channel
                </>
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export default AddChannelModal

"""
FastAPI backend server for managing Telegram trading bot
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from database import init_db, get_db, TelegramChannel, TradingSignal
from channel_monitor import channel_manager
from datetime import datetime
import asyncio

# Initialize FastAPI app
app = FastAPI(title="Telegram Trading Bot API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Pydantic models for API
class ChannelCreate(BaseModel):
    name: str
    username: str  # @channel_name or https://t.me/channel_name

class ChannelResponse(BaseModel):
    id: int
    name: str
    username: str
    is_active: bool
    added_at: datetime
    last_checked: Optional[datetime]
    total_signals: int
    status: str
    error_message: Optional[str]
    
    class Config:
        from_attributes = True

class SignalResponse(BaseModel):
    id: int
    channel_name: str
    action: str
    instrument: str
    entry_price: Optional[str]
    stop_loss: Optional[str]
    take_profits: Optional[List]
    signal_type: str
    message_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_channels: int
    active_channels: int
    total_signals: int
    signals_today: int

# API Endpoints

@app.get("/")
async def root():
    return {"message": "Telegram Trading Bot API", "status": "running"}

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total_channels = db.query(TelegramChannel).count()
    active_channels = db.query(TelegramChannel).filter(TelegramChannel.is_active == True).count()
    total_signals = db.query(TradingSignal).count()
    
    # Signals today
    today = datetime.utcnow().date()
    signals_today = db.query(TradingSignal).filter(
        TradingSignal.created_at >= datetime.combine(today, datetime.min.time())
    ).count()
    
    return {
        "total_channels": total_channels,
        "active_channels": active_channels,
        "total_signals": total_signals,
        "signals_today": signals_today
    }

@app.get("/api/channels", response_model=List[ChannelResponse])
async def get_channels(db: Session = Depends(get_db)):
    """Get all channels"""
    channels = db.query(TelegramChannel).order_by(TelegramChannel.added_at.desc()).all()
    return channels

@app.post("/api/channels", response_model=ChannelResponse)
async def create_channel(channel: ChannelCreate, db: Session = Depends(get_db)):
    """Add a new channel"""
    # Check if channel already exists
    existing = db.query(TelegramChannel).filter(
        TelegramChannel.username == channel.username
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Channel already exists")
    
    # Create new channel
    db_channel = TelegramChannel(
        name=channel.name,
        username=channel.username,
        is_active=False,
        status="stopped"
    )
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    
    return db_channel

@app.post("/api/channels/{channel_id}/start")
async def start_channel(channel_id: int, db: Session = Depends(get_db)):
    """Start monitoring a channel"""
    channel = db.query(TelegramChannel).filter(TelegramChannel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    if channel.is_active:
        raise HTTPException(status_code=400, detail="Channel is already running")
    
    # Start the channel monitor
    asyncio.create_task(
        channel_manager.start_channel(channel.id, channel.username, channel.name)
    )
    
    return {"message": f"Started monitoring {channel.name}"}

@app.post("/api/channels/{channel_id}/stop")
async def stop_channel(channel_id: int, db: Session = Depends(get_db)):
    """Stop monitoring a channel"""
    channel = db.query(TelegramChannel).filter(TelegramChannel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Stop the channel monitor
    await channel_manager.stop_channel(channel.id)
    
    return {"message": f"Stopped monitoring {channel.name}"}

@app.delete("/api/channels/{channel_id}")
async def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    """Delete a channel"""
    channel = db.query(TelegramChannel).filter(TelegramChannel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Stop monitoring if active
    if channel.is_active:
        await channel_manager.stop_channel(channel.id)
    
    # Delete from database
    db.delete(channel)
    db.commit()
    
    return {"message": f"Deleted channel {channel.name}"}

@app.get("/api/signals", response_model=List[SignalResponse])
async def get_signals(
    limit: int = 50,
    channel_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get trading signals"""
    query = db.query(TradingSignal)
    
    if channel_id:
        query = query.filter(TradingSignal.channel_id == channel_id)
    
    signals = query.order_by(TradingSignal.created_at.desc()).limit(limit).all()
    return signals

@app.get("/api/signals/recent", response_model=List[SignalResponse])
async def get_recent_signals(db: Session = Depends(get_db)):
    """Get most recent signals (last 24 hours)"""
    yesterday = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    signals = db.query(TradingSignal).filter(
        TradingSignal.created_at >= yesterday
    ).order_by(TradingSignal.created_at.desc()).limit(20).all()
    
    return signals

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

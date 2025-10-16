"""
FastAPI backend server for managing Telegram trading bot
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from supabase_database import init_supabase_db, get_supabase_db, Channel, Signal, supabase_client
from datetime import datetime
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Telegram Trading Bot API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "https://telegram-trading-bot-magicreview.vercel.app",
        "https://telegram-trading-bot-bay.vercel.app",
        "https://telegram-trading-bot-git-main-magicreview.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase database
init_supabase_db()

# Pydantic models for API
class ChannelCreate(BaseModel):
    name: str
    username: str  # @channel_name or https://t.me/channel_name

class ChannelResponse(BaseModel):
    id: int
    name: str
    username: str
    is_active: bool
    signal_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SignalResponse(BaseModel):
    id: int
    channel_id: Optional[int]
    raw_text: str
    action: Optional[str]
    instrument: Optional[str]
    entry_price: Optional[str]
    stop_loss: Optional[str]
    take_profits: Optional[List[str]]
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
async def get_stats(db: Session = Depends(get_supabase_db)):
    """Get dashboard statistics"""
    try:
        total_channels = db.query(Channel).count()
        active_channels = db.query(Channel).filter(Channel.is_active == True).count()
        total_signals = db.query(Signal).count()
        
        # Signals today
        today = datetime.utcnow().date()
        signals_today = db.query(Signal).filter(
            Signal.created_at >= datetime.combine(today, datetime.min.time())
        ).count()
        
        return {
            "total_channels": total_channels,
            "active_channels": active_channels,
            "total_signals": total_signals,
            "signals_today": signals_today
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {
            "total_channels": 0,
            "active_channels": 0,
            "total_signals": 0,
            "signals_today": 0
        }

@app.get("/api/channels", response_model=List[ChannelResponse])
async def get_channels(db: Session = Depends(get_supabase_db)):
    """Get all channels"""
    try:
        channels = db.query(Channel).order_by(Channel.created_at.desc()).all()
        return channels
    except Exception as e:
        logger.error(f"Error getting channels: {e}")
        return []

@app.post("/api/channels", response_model=ChannelResponse)
async def create_channel(channel: ChannelCreate, db: Session = Depends(get_supabase_db)):
    """Add a new channel"""
    try:
        # Check if channel already exists
        existing = db.query(Channel).filter(
            Channel.username == channel.username
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Channel already exists")
        
        # Create new channel
        db_channel = Channel(
            name=channel.name,
            username=channel.username,
            is_active=False,
            signal_count=0
        )
        db.add(db_channel)
        db.commit()
        db.refresh(db_channel)
        
        logger.info(f"✅ Channel created: {channel.name} ({channel.username})")
        return db_channel
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating channel: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create channel: {str(e)}")

@app.post("/api/channels/{channel_id}/start")
async def start_channel(channel_id: int, db: Session = Depends(get_supabase_db)):
    """Start monitoring a channel"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        if channel.is_active:
            raise HTTPException(status_code=400, detail="Channel is already running")
        
        # Update channel status
        channel.is_active = True
        db.commit()
        
        logger.info(f"✅ Started monitoring: {channel.name}")
        return {"message": f"Started monitoring {channel.name}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting channel: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start channel: {str(e)}")

@app.post("/api/channels/{channel_id}/stop")
async def stop_channel(channel_id: int, db: Session = Depends(get_supabase_db)):
    """Stop monitoring a channel"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        # Update channel status
        channel.is_active = False
        db.commit()
        
        logger.info(f"⏹️ Stopped monitoring: {channel.name}")
        return {"message": f"Stopped monitoring {channel.name}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping channel: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stop channel: {str(e)}")

@app.delete("/api/channels/{channel_id}")
async def delete_channel(channel_id: int, db: Session = Depends(get_supabase_db)):
    """Delete a channel"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        channel_name = channel.name
        
        # Delete from database
        db.delete(channel)
        db.commit()
        
        logger.info(f"🗑️ Deleted channel: {channel_name}")
        return {"message": f"Deleted channel {channel_name}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting channel: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete channel: {str(e)}")

@app.get("/api/signals", response_model=List[SignalResponse])
async def get_signals(
    limit: int = 50,
    channel_id: Optional[int] = None,
    db: Session = Depends(get_supabase_db)
):
    """Get trading signals"""
    try:
        query = db.query(Signal)
        
        if channel_id:
            query = query.filter(Signal.channel_id == channel_id)
        
        signals = query.order_by(Signal.created_at.desc()).limit(limit).all()
        return signals
    except Exception as e:
        logger.error(f"Error getting signals: {e}")
        return []

@app.get("/api/signals/recent", response_model=List[SignalResponse])
async def get_recent_signals(db: Session = Depends(get_supabase_db)):
    """Get most recent signals (last 24 hours)"""
    try:
        yesterday = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        signals = db.query(Signal).filter(
            Signal.created_at >= yesterday
        ).order_by(Signal.created_at.desc()).limit(20).all()
        
        return signals
    except Exception as e:
        logger.error(f"Error getting recent signals: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

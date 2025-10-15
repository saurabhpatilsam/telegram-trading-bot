"""
Database models and configuration
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import os

# Create SQLite database
DATABASE_URL = "sqlite:///./trading_bot.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TelegramChannel(Base):
    """Model for Telegram channels being monitored"""
    __tablename__ = "telegram_channels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)  # @channel_name or link
    is_active = Column(Boolean, default=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, nullable=True)
    total_signals = Column(Integer, default=0)
    status = Column(String, default="stopped")  # stopped, running, error
    error_message = Column(Text, nullable=True)

class TradingSignal(Base):
    """Model for trading signals detected"""
    __tablename__ = "trading_signals_local"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, nullable=False)
    channel_name = Column(String, nullable=False)
    action = Column(String, nullable=False)  # BUY/SELL
    instrument = Column(String, nullable=False)
    entry_price = Column(String, nullable=True)
    stop_loss = Column(String, nullable=True)
    take_profits = Column(JSON, nullable=True)
    signal_type = Column(String, nullable=False)  # text/image
    raw_text = Column(Text, nullable=True)
    message_id = Column(Integer, nullable=True)
    message_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_to_supabase = Column(Boolean, default=False)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

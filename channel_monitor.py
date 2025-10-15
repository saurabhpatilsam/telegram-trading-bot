"""
Background worker for monitoring Telegram channels
"""
import asyncio
from typing import Dict, Optional
from datetime import datetime
from telethon import TelegramClient, events
from config import Config
from text_parser import TradingSignalParser
from image_analyzer import ImageAnalyzer
from supabase_client import SupabaseClient
from database import SessionLocal, TelegramChannel, TradingSignal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChannelMonitor:
    """Monitors a single Telegram channel for trading signals"""
    
    def __init__(self, channel_id: int, channel_username: str, channel_name: str):
        self.channel_id = channel_id
        self.channel_username = channel_username
        self.channel_name = channel_name
        self.is_running = False
        self.client = None
        self.group_entity = None
        
        # Initialize parsers
        self.text_parser = TradingSignalParser()
        self.image_analyzer = ImageAnalyzer(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            azure_api_key=Config.AZURE_OPENAI_KEY,
            azure_deployment=Config.AZURE_OPENAI_DEPLOYMENT
        )
        
        # Initialize Supabase
        self.supabase_client = SupabaseClient(
            url=Config.SUPABASE_URL,
            key=Config.SUPABASE_KEY,
            table_name=Config.SUPABASE_TABLE
        )
    
    async def start(self):
        """Start monitoring the channel"""
        try:
            self.is_running = True
            
            # Create Telegram client with unique session name
            session_name = f"session_{self.channel_id}_{self.channel_username.replace('@', '')}"
            self.client = TelegramClient(
                session_name,
                Config.TELEGRAM_API_ID,
                Config.TELEGRAM_API_HASH
            )
            
            await self.client.start(phone=Config.TELEGRAM_PHONE)
            logger.info(f"✓ Connected to Telegram for channel: {self.channel_name}")
            
            # Get the group entity
            username = self.channel_username
            if username.startswith('@'):
                username = username[1:]
            elif 'https://t.me/' in username:
                username = username.split('/')[-1]
            
            self.group_entity = await self.client.get_entity(username)
            logger.info(f"✓ Connected to group: {self.group_entity.title}")
            
            # Update database status
            self._update_channel_status("running", None)
            
            # Register event handler
            @self.client.on(events.NewMessage(chats=self.group_entity))
            async def handler(event):
                await self.process_message(event)
            
            # Process recent messages (optional)
            await self.process_recent_messages(limit=10)
            
            # Keep running
            logger.info(f"✓ Now monitoring {self.channel_name} for new signals...")
            await self.client.run_until_disconnected()
            
        except Exception as e:
            logger.error(f"✗ Error in channel monitor for {self.channel_name}: {str(e)}")
            self._update_channel_status("error", str(e))
            self.is_running = False
    
    async def stop(self):
        """Stop monitoring the channel"""
        self.is_running = False
        if self.client:
            await self.client.disconnect()
        self._update_channel_status("stopped", None)
        logger.info(f"✓ Stopped monitoring {self.channel_name}")
    
    async def process_message(self, event):
        """Process a new message"""
        try:
            message = event.message
            signal = None
            
            # Check for media (images)
            if message.media:
                logger.info(f"[{self.channel_name}] Analyzing image message...")
                media_bytes = await self.client.download_media(message.media, file=bytes)
                if media_bytes:
                    signal = self.image_analyzer.analyze_image(media_bytes)
            
            # Check for text
            if not signal and message.text:
                signal = self.text_parser.parse_message(message.text)
            
            # Save valid signals
            if signal and self.text_parser.validate_signal(signal):
                signal['message_id'] = message.id
                signal['message_date'] = message.date.isoformat()
                signal['channel_id'] = self.channel_id
                signal['channel_name'] = self.channel_name
                
                self._save_signal(signal)
                logger.info(f"✓ [{self.channel_name}] Found signal: {signal['action']} {signal['instrument']}")
        
        except Exception as e:
            logger.error(f"✗ Error processing message from {self.channel_name}: {str(e)}")
    
    async def process_recent_messages(self, limit=10):
        """Process recent messages on startup"""
        try:
            messages = await self.client.get_messages(self.group_entity, limit=limit)
            logger.info(f"Processing {len(messages)} recent messages from {self.channel_name}")
            
            for message in reversed(messages):
                event_like = type('obj', (object,), {'message': message})()
                await self.process_message(event_like)
        
        except Exception as e:
            logger.error(f"Error processing recent messages: {str(e)}")
    
    def _save_signal(self, signal: dict):
        """Save signal to local database and Supabase"""
        try:
            # Save to local database
            db = SessionLocal()
            db_signal = TradingSignal(
                channel_id=self.channel_id,
                channel_name=self.channel_name,
                action=signal['action'],
                instrument=signal['instrument'],
                entry_price=str(signal.get('entry_price', '')),
                stop_loss=str(signal.get('stop_loss', '')),
                take_profits=signal.get('take_profits', []),
                signal_type=signal.get('signal_type', 'unknown'),
                raw_text=signal.get('raw_text', ''),
                message_id=signal.get('message_id'),
                message_date=datetime.fromisoformat(signal.get('message_date')) if signal.get('message_date') else None
            )
            db.add(db_signal)
            db.commit()
            
            # Update channel signal count
            channel = db.query(TelegramChannel).filter(TelegramChannel.id == self.channel_id).first()
            if channel:
                channel.total_signals += 1
                channel.last_checked = datetime.utcnow()
                db.commit()
            
            db.close()
            
            # Save to Supabase
            try:
                self.supabase_client.insert_signal(signal)
            except Exception as e:
                logger.warning(f"Failed to sync to Supabase: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error saving signal: {str(e)}")
    
    def _update_channel_status(self, status: str, error_message: Optional[str]):
        """Update channel status in database"""
        try:
            db = SessionLocal()
            channel = db.query(TelegramChannel).filter(TelegramChannel.id == self.channel_id).first()
            if channel:
                channel.status = status
                channel.is_active = (status == "running")
                channel.error_message = error_message
                channel.last_checked = datetime.utcnow()
                db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Error updating channel status: {str(e)}")


class ChannelManager:
    """Manages multiple channel monitors"""
    
    def __init__(self):
        self.monitors: Dict[int, ChannelMonitor] = {}
        self.tasks: Dict[int, asyncio.Task] = {}
    
    async def start_channel(self, channel_id: int, channel_username: str, channel_name: str):
        """Start monitoring a channel"""
        if channel_id in self.monitors:
            logger.warning(f"Channel {channel_name} is already being monitored")
            return
        
        monitor = ChannelMonitor(channel_id, channel_username, channel_name)
        self.monitors[channel_id] = monitor
        
        # Create and store the task
        task = asyncio.create_task(monitor.start())
        self.tasks[channel_id] = task
        
        logger.info(f"Started monitoring channel: {channel_name}")
    
    async def stop_channel(self, channel_id: int):
        """Stop monitoring a channel"""
        if channel_id not in self.monitors:
            logger.warning(f"Channel {channel_id} is not being monitored")
            return
        
        monitor = self.monitors[channel_id]
        await monitor.stop()
        
        # Cancel the task
        if channel_id in self.tasks:
            self.tasks[channel_id].cancel()
            del self.tasks[channel_id]
        
        del self.monitors[channel_id]
        logger.info(f"Stopped monitoring channel: {channel_id}")
    
    async def stop_all(self):
        """Stop all channel monitors"""
        for channel_id in list(self.monitors.keys()):
            await self.stop_channel(channel_id)

# Global channel manager instance
channel_manager = ChannelManager()

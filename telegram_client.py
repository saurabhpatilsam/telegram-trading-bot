from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from typing import Optional, Callable
import asyncio

class TelegramGroupMonitor:
    """Monitor a Telegram group for trading signals"""
    
    def __init__(self, api_id: str, api_hash: str, phone: str):
        """
        Initialize Telegram client
        
        Args:
            api_id: Telegram API ID
            api_hash: Telegram API Hash
            phone: Phone number for authentication
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = TelegramClient('trading_bot_session', api_id, api_hash)
        self.group_entity = None
    
    async def start(self):
        """Start the Telegram client"""
        await self.client.start(phone=self.phone)
        print("✓ Telegram client started successfully")
        
        # Check if we're authorized
        if await self.client.is_user_authorized():
            me = await self.client.get_me()
            print(f"✓ Logged in as: {me.first_name} ({me.phone})")
        else:
            print("✗ Not authorized. Please check your credentials.")
    
    async def join_group(self, group_username: str):
        """
        Join and get the group entity
        
        Args:
            group_username: Username or invite link of the group
        """
        try:
            # Remove @ if present
            if group_username.startswith('@'):
                group_username = group_username[1:]
            
            # Get the group entity
            self.group_entity = await self.client.get_entity(group_username)
            print(f"✓ Connected to group: {self.group_entity.title}")
            
        except Exception as e:
            print(f"✗ Error joining group: {str(e)}")
            raise
    
    async def download_media(self, message) -> Optional[bytes]:
        """
        Download media from a message
        
        Args:
            message: Telegram message object
            
        Returns:
            Media file as bytes or None
        """
        try:
            if message.media:
                # Download to bytes
                media_bytes = await self.client.download_media(message.media, file=bytes)
                return media_bytes
        except Exception as e:
            print(f"✗ Error downloading media: {str(e)}")
        return None
    
    def register_message_handler(self, handler: Callable):
        """
        Register a handler for new messages
        
        Args:
            handler: Async function to handle new messages
        """
        @self.client.on(events.NewMessage(chats=self.group_entity))
        async def message_handler(event):
            await handler(event)
    
    async def get_recent_messages(self, limit: int = 100):
        """
        Get recent messages from the group
        
        Args:
            limit: Number of messages to retrieve
            
        Returns:
            List of messages
        """
        try:
            messages = await self.client.get_messages(self.group_entity, limit=limit)
            print(f"✓ Retrieved {len(messages)} recent messages")
            return messages
        except Exception as e:
            print(f"✗ Error retrieving messages: {str(e)}")
            return []
    
    async def run_until_disconnected(self):
        """Keep the client running"""
        print("\n✓ Bot is now monitoring the group for trading signals...")
        print("Press Ctrl+C to stop\n")
        await self.client.run_until_disconnected()
    
    async def disconnect(self):
        """Disconnect the client"""
        await self.client.disconnect()
        print("✓ Telegram client disconnected")

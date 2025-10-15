#!/usr/bin/env python3
"""
Telegram to Supabase Trading Bot
Monitors a Telegram group for trading signals and stores them in Supabase
"""

import asyncio
from datetime import datetime
from config import Config
from telegram_client import TelegramGroupMonitor
from text_parser import TradingSignalParser
from image_analyzer import ImageAnalyzer
from supabase_client import SupabaseClient

class TradingSignalBot:
    """Main bot class that coordinates all components"""
    
    def __init__(self):
        # Validate configuration
        Config.validate()
        
        # Initialize components
        self.telegram_monitor = TelegramGroupMonitor(
            api_id=Config.TELEGRAM_API_ID,
            api_hash=Config.TELEGRAM_API_HASH,
            phone=Config.TELEGRAM_PHONE
        )
        
        self.text_parser = TradingSignalParser()
        self.image_analyzer = ImageAnalyzer(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            azure_api_key=Config.AZURE_OPENAI_KEY,
            azure_deployment=Config.AZURE_OPENAI_DEPLOYMENT
        )
        
        self.supabase_client = SupabaseClient(
            url=Config.SUPABASE_URL,
            key=Config.SUPABASE_KEY,
            table_name=Config.SUPABASE_TABLE
        )
        
        print("\n" + "="*60)
        print("TELEGRAM TO SUPABASE TRADING BOT")
        print("="*60 + "\n")
    
    async def process_message(self, event):
        """
        Process a new message from the Telegram group
        
        Args:
            event: Telegram message event
        """
        message = event.message
        
        print(f"\n{'='*60}")
        print(f"New message received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        signal = None
        
        # Check if message has media (image)
        if message.media:
            print("📷 Message contains media, analyzing image...")
            
            # Download the media
            media_bytes = await self.telegram_monitor.download_media(message)
            
            if media_bytes:
                # Analyze the image
                signal = self.image_analyzer.analyze_image(media_bytes)
                
                if signal:
                    print(f"✓ Signal extracted from image")
        
        # If no signal from image, try to parse text
        if not signal and message.text:
            print("📝 Analyzing text message...")
            signal = self.text_parser.parse_message(message.text)
            
            if signal:
                print(f"✓ Signal extracted from text")
        
        # If we have a valid signal, store it in Supabase
        if signal and self.text_parser.validate_signal(signal):
            # Add message metadata
            signal['message_id'] = message.id
            signal['message_date'] = message.date.isoformat()
            
            # Print signal details
            print(f"\n📊 Trading Signal Details:")
            print(f"   Action: {signal.get('action')}")
            print(f"   Instrument: {signal.get('instrument')}")
            print(f"   Entry Price: {signal.get('entry_price')}")
            print(f"   Stop Loss: {signal.get('stop_loss')}")
            print(f"   Take Profits: {signal.get('take_profits')}")
            
            # Insert into Supabase
            result = self.supabase_client.insert_signal(signal)
            
            if result:
                print(f"✓ Signal stored in Supabase (ID: {result.get('id')})")
            else:
                print("✗ Failed to store signal in Supabase")
        else:
            print("ℹ️  No valid trading signal found in this message")
        
        print(f"{'='*60}\n")
    
    async def process_historical_messages(self, limit: int = 100):
        """
        Process historical messages from the group
        
        Args:
            limit: Number of recent messages to process
        """
        print(f"\n📚 Processing {limit} recent messages from the group...")
        print("="*60)
        
        messages = await self.telegram_monitor.get_recent_messages(limit=limit)
        
        processed_count = 0
        signal_count = 0
        
        for message in reversed(messages):  # Process oldest first
            signal = None
            
            # Check for media
            if message.media:
                media_bytes = await self.telegram_monitor.download_media(message)
                if media_bytes:
                    signal = self.image_analyzer.analyze_image(media_bytes)
            
            # Check for text
            if not signal and message.text:
                signal = self.text_parser.parse_message(message.text)
            
            # Store valid signals
            if signal and self.text_parser.validate_signal(signal):
                signal['message_id'] = message.id
                signal['message_date'] = message.date.isoformat()
                
                result = self.supabase_client.insert_signal(signal)
                if result:
                    signal_count += 1
                    print(f"✓ Signal {signal_count}: {signal.get('action')} {signal.get('instrument')}")
            
            processed_count += 1
        
        print(f"\n{'='*60}")
        print(f"✓ Processed {processed_count} messages")
        print(f"✓ Found {signal_count} trading signals")
        print(f"{'='*60}\n")
    
    async def start(self, process_history: bool = True, history_limit: int = 100):
        """
        Start the bot
        
        Args:
            process_history: Whether to process historical messages
            history_limit: Number of historical messages to process
        """
        try:
            # Print table creation SQL
            self.supabase_client.create_table_if_not_exists()
            
            # Start Telegram client
            await self.telegram_monitor.start()
            
            # Join the group
            await self.telegram_monitor.join_group(Config.TELEGRAM_GROUP_USERNAME)
            
            # Process historical messages if requested
            if process_history:
                await self.process_historical_messages(limit=history_limit)
            
            # Register message handler for new messages
            self.telegram_monitor.register_message_handler(self.process_message)
            
            # Run until disconnected
            await self.telegram_monitor.run_until_disconnected()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Stopping bot...")
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
        finally:
            await self.telegram_monitor.disconnect()

async def main():
    """Main entry point"""
    bot = TradingSignalBot()
    
    # Start the bot
    # Set process_history=True to process existing messages
    # Set process_history=False to only monitor new messages
    await bot.start(process_history=True, history_limit=50)

if __name__ == "__main__":
    asyncio.run(main())

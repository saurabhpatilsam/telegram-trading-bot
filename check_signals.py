#!/usr/bin/env python3
"""
Quick script to check and display signals from Telegram group
"""

import asyncio
from config import Config
from telegram_client import TelegramGroupMonitor
from text_parser import TradingSignalParser
from image_analyzer import ImageAnalyzer

async def check_signals():
    # Validate configuration
    Config.validate()
    
    # Initialize components
    telegram_monitor = TelegramGroupMonitor(
        api_id=Config.TELEGRAM_API_ID,
        api_hash=Config.TELEGRAM_API_HASH,
        phone=Config.TELEGRAM_PHONE
    )
    
    text_parser = TradingSignalParser()
    image_analyzer = ImageAnalyzer(
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
        azure_api_key=Config.AZURE_OPENAI_KEY,
        azure_deployment=Config.AZURE_OPENAI_DEPLOYMENT
    )
    
    print("\n" + "="*60)
    print("CHECKING TELEGRAM SIGNALS")
    print("="*60 + "\n")
    
    # Start Telegram client
    await telegram_monitor.start()
    
    # Join the group
    await telegram_monitor.join_group(Config.TELEGRAM_GROUP_USERNAME)
    
    # Get recent messages
    messages = await telegram_monitor.get_recent_messages(limit=100)
    
    signals_found = []
    processed = 0
    
    for message in reversed(messages):
        processed += 1
        signal = None
        
        # Check for media (images/screenshots)
        if message.media:
            print(f"Processing message {processed}/100: Found image, analyzing with AI...")
            media_bytes = await telegram_monitor.download_media(message)
            if media_bytes:
                signal = image_analyzer.analyze_image(media_bytes)
                if signal:
                    print(f"  ✓ Found signal in image: {signal.get('action')} {signal.get('instrument')}")
        
        # Check for text
        if not signal and message.text:
            signal = text_parser.parse_message(message.text)
            if signal:
                print(f"Processing message {processed}/100: Found signal in text: {signal.get('action')} {signal.get('instrument')}")
        
        # Store valid signals
        if signal and text_parser.validate_signal(signal):
            signal['message_id'] = message.id
            signal['message_date'] = message.date.isoformat()
            signals_found.append(signal)
    
    # Display all found signals
    print(f"\n{'='*60}")
    print(f"FOUND {len(signals_found)} TRADING SIGNALS")
    print(f"{'='*60}\n")
    
    for i, signal in enumerate(signals_found, 1):
        print(f"Signal #{i}")
        print(f"  Action:        {signal.get('action')}")
        print(f"  Instrument:    {signal.get('instrument')}")
        print(f"  Entry Price:   {signal.get('entry_price')}")
        print(f"  Stop Loss:     {signal.get('stop_loss')}")
        print(f"  Take Profits:  {signal.get('take_profits')}")
        print(f"  Signal Type:   {signal.get('signal_type')}")
        print(f"  Message Date:  {signal.get('message_date')}")
        print(f"  Raw Text:      {signal.get('raw_text', 'N/A')[:100]}...")
        print(f"{'-'*60}\n")
    
    await telegram_monitor.disconnect()

if __name__ == "__main__":
    asyncio.run(check_signals())

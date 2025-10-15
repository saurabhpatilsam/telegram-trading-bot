# Telegram to Supabase Trading Bot 📊

**Automated 24/7 Trading Signal Monitor with Beautiful Dashboard**

A complete full-stack application that monitors multiple Telegram channels for trading signals, analyzes them with AI, and provides a beautiful React dashboard for management. Never miss a trading signal again!

## Features ✨

### Backend (Python + FastAPI)
- 📱 **Multi-Channel Support**: Monitor unlimited Telegram channels simultaneously
- 🤖 **AI-Powered Analysis**: Uses Azure OpenAI GPT-4o Vision to analyze screenshots
- 📝 **Smart Text Parsing**: Extracts signals from text messages automatically
- 🗄️ **Dual Storage**: Local SQLite + Supabase cloud backup
- 🔄 **24/7 Operation**: Background workers for continuous monitoring
- 🎯 **Signal Intelligence**: Distinguishes trade signals from trade results

### Frontend (React + Tailwind)
- 🎨 **Beautiful Dashboard**: Modern, responsive UI with gradient themes
- ⚡ **Real-Time Updates**: Auto-refresh every 5 seconds
- 📊 **Live Statistics**: Total channels, active monitors, signal counts
- 🎮 **Easy Controls**: One-click start/stop for each channel
- 🔍 **Filter & Search**: View signals by channel or all together
- 📱 **Mobile Friendly**: Works on all devices

## Prerequisites 📋

1. **Telegram API Credentials**
   - Go to https://my.telegram.org/apps
   - Create a new application
   - Note down your `API ID` and `API Hash`

2. **Supabase Account**
   - Create a project at https://supabase.com
   - Get your project URL and anon/service key

3. **Optional: OpenAI API Key** (for advanced image analysis)
   - Get your API key from https://platform.openai.com/api-keys

4. **Tesseract OCR** (optional, for image text extraction)
   - macOS: `brew install tesseract`
   - Ubuntu: `sudo apt-get install tesseract-ocr`
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

## 🚀 Quick Start (3 Steps!)

### 1. Start the Backend
```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo
./start_backend.sh
```

### 2. Start the Frontend (New Terminal)
```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo
./start_frontend.sh
```

### 3. Open Dashboard
Go to: **http://localhost:3000**

✨ **That's it!** Add channels and start monitoring.

---

## 📖 Full Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions

## 💻 Installation Details

### Backend Dependencies
```bash
pip install -r backend_requirements.txt
```

### Frontend Dependencies
```bash
cd frontend
npm install
```

### Environment Variables
Your `.env` file is already configured with:
- Telegram API credentials ✓
- Azure OpenAI (GPT-4o) ✓
- Supabase credentials ✓

4. **Create Supabase table**
   
   Run the bot once to see the SQL, or use this SQL in your Supabase SQL Editor:
   
   ```sql
   CREATE TABLE IF NOT EXISTS trading_signals (
       id BIGSERIAL PRIMARY KEY,
       action TEXT NOT NULL,
       instrument TEXT NOT NULL,
       entry_price NUMERIC,
       stop_loss NUMERIC,
       take_profits JSONB,
       signal_type TEXT,
       raw_text TEXT,
       message_id BIGINT,
       message_date TIMESTAMP,
       created_at TIMESTAMP DEFAULT NOW(),
       processed BOOLEAN DEFAULT FALSE
   );
   
   CREATE INDEX IF NOT EXISTS idx_created_at ON trading_signals(created_at DESC);
   CREATE INDEX IF NOT EXISTS idx_processed ON trading_signals(processed);
   CREATE INDEX IF NOT EXISTS idx_instrument ON trading_signals(instrument);
   ```

## Usage 🎯

1. **Run the bot**
   ```bash
   python main.py
   ```

2. **First-time authentication**
   - On first run, you'll receive a code on your Telegram app
   - Enter the code when prompted
   - The session will be saved for future runs

3. **The bot will:**
   - Process the last 50 messages from the group (configurable)
   - Start monitoring for new messages in real-time
   - Extract trading signals from text and images
   - Store valid signals in your Supabase database

## Configuration ⚙️

### Processing Historical Messages

Edit `main.py` to configure historical message processing:

```python
await bot.start(
    process_history=True,  # Set to False to skip historical messages
    history_limit=50       # Number of messages to process
)
```

### Signal Parsing Patterns

The bot recognizes various formats:

**Text Examples:**
```
BUY BTCUSDT
ENTRY: 45000
SL: 44000
TP: 46000, 47000, 48000
```

```
SELL EURUSD @ 1.0850
STOP LOSS: 1.0900
TARGET: 1.0800
```

**Image Support:**
- Screenshots of trading signals
- Chart images with annotations
- Signal cards from trading groups

## Database Schema 🗃️

The `trading_signals` table stores:

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `action` | TEXT | BUY or SELL |
| `instrument` | TEXT | Trading symbol (e.g., BTCUSDT) |
| `entry_price` | NUMERIC | Entry price |
| `stop_loss` | NUMERIC | Stop loss level |
| `take_profits` | JSONB | Array of take profit targets |
| `signal_type` | TEXT | 'text' or 'image' |
| `raw_text` | TEXT | Original message text |
| `message_id` | BIGINT | Telegram message ID |
| `message_date` | TIMESTAMP | When message was sent |
| `created_at` | TIMESTAMP | When stored in DB |
| `processed` | BOOLEAN | Processing status |

## Integrating with Trading APIs 🔌

Once signals are in Supabase, you can:

1. **Create a Supabase Function** to trigger trading API calls
2. **Use Webhooks** to notify your trading system
3. **Query the API** from your trading bot:

```python
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Get unprocessed signals
signals = supabase.table('trading_signals')\
    .select('*')\
    .eq('processed', False)\
    .execute()

# Process each signal
for signal in signals.data:
    # Call your trading API
    execute_trade(signal)
    
    # Mark as processed
    supabase.table('trading_signals')\
        .update({'processed': True})\
        .eq('id', signal['id'])\
        .execute()
```

## Troubleshooting 🔧

### "Could not find the input entity for..."
- Make sure the group username is correct
- Ensure you're a member of the group
- Try using the group's invite link instead

### OCR not working
- Install Tesseract: `brew install tesseract` (macOS)
- Or enable OpenAI Vision by adding your `OPENAI_API_KEY`

### Rate limiting
- Telegram has rate limits for API calls
- The bot includes delays to prevent hitting limits
- For large message histories, process in batches

## Security Notes 🔒

- Never commit your `.env` file
- Keep your API keys secure
- Use Supabase RLS (Row Level Security) for production
- Consider using a service role key for server deployments

## Project Structure 📁

```
telegram-supabase-trading-bot/
├── main.py                 # Main application entry point
├── telegram_client.py      # Telegram API integration
├── text_parser.py          # Text message parsing
├── image_analyzer.py       # Image analysis (OCR + AI)
├── supabase_client.py      # Supabase database client
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## License 📄

This project is provided as-is for educational purposes. Use at your own risk.

## Support 💬

For issues or questions, please check the code comments or modify the parsing patterns to match your specific trading signal format.

---

**Note**: This bot is for educational purposes. Always verify trading signals manually before executing trades. Automated trading carries significant risk.

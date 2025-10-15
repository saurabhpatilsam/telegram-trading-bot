# Telegram Trading Bot - Setup Guide

## 🚀 Complete Automated Trading Bot with React Dashboard

This system allows you to monitor multiple Telegram channels 24/7, detect trading signals using AI, and manage everything from a beautiful web interface.

## 📋 Features

- ✅ **Multi-Channel Support**: Add and monitor multiple Telegram channels
- ✅ **Start/Stop Controls**: Control each channel individually
- ✅ **AI-Powered Analysis**: Uses Azure OpenAI to analyze screenshots
- ✅ **Real-Time Dashboard**: Beautiful React + Tailwind UI
- ✅ **Automatic Signal Detection**: Detects BUY/SELL signals from text and images
- ✅ **Supabase Integration**: All signals saved to your database
- ✅ **24/7 Operation**: Runs continuously in the background

## 🛠️ Installation

### Backend Setup

1. **Install Python dependencies:**
```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo
pip3 install -r backend_requirements.txt
```

2. **Your `.env` file is already configured** with:
   - Telegram API credentials
   - Azure OpenAI (GPT-4o)
   - Supabase credentials

3. **Start the backend API server:**
```bash
python3 api_server.py
```

The API will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install Node.js dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm run dev
```

The React app will open at `http://localhost:3000`

## 🎯 How to Use

### 1. Access the Dashboard
Open your browser and go to `http://localhost:3000`

### 2. Add a Telegram Channel
- Click the **"+ Add Channel"** button
- Enter a channel name (e.g., "Trading Signals Pro")
- Enter the channel username or link:
  - `@channel_name` OR
  - `https://t.me/channel_name`
- Click "Add Channel"

### 3. Start Monitoring
- Find your channel in the list
- Click the **green "Start" button**
- The bot will:
  - Connect to Telegram
  - Process recent messages
  - Monitor for new signals 24/7

### 4. View Signals
- All detected signals appear in the right panel
- Click on a channel to filter signals
- Signals show:
  - BUY/SELL action
  - Instrument (EURUSD, XAUUSD, etc.)
  - Entry price
  - Stop loss
  - Take profit levels

### 5. Stop/Restart
- Click the **red "Stop" button** to pause monitoring
- Click "Start" again to resume

### 6. Delete Channels
- Click the trash icon to remove a channel
- This stops monitoring and removes it from the list

## 📊 Dashboard Features

### Stats Cards
- **Total Channels**: Number of channels added
- **Active Channels**: Currently running monitors
- **Total Signals**: All-time signal count
- **Signals Today**: Signals detected in the last 24 hours

### Channel Management
- See all channels in one place
- Status indicators (Running/Stopped/Error)
- Signal count per channel
- One-click start/stop

### Signal Display
- Real-time signal feed
- Color-coded by action (Green=BUY, Red=SELL)
- Signal type badges (text/image)
- Complete trade details
- Timestamps

## 🔧 Technical Architecture

### Backend (Python + FastAPI)
- **`api_server.py`**: REST API endpoints
- **`channel_monitor.py`**: Background workers for each channel
- **`database.py`**: SQLite database for local storage
- **`telegram_client.py`**: Telegram API integration
- **`image_analyzer.py`**: Azure OpenAI Vision for image analysis
- **`text_parser.py`**: Text parsing for trading signals

### Frontend (React + Tailwind)
- **`App.jsx`**: Main application component
- **`ChannelList.jsx`**: Channel management UI
- **`SignalList.jsx`**: Signal display
- **`AddChannelModal.jsx`**: Add channel form
- **`Stats.jsx`**: Dashboard statistics

### Database
- **Local SQLite**: Stores channels and signals
- **Supabase**: Cloud backup for signals

## 🔒 Security Notes

- All credentials are in `.env` (never commit this)
- Telegram session files are created per channel
- API runs on localhost by default
- For production, add authentication

## 🚨 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>
```

### Frontend won't start
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Channel won't start
- Check if the channel username is correct
- Make sure you're a member of the channel
- Check the error message in the dashboard

### No signals detected
- Wait a few minutes for new messages
- Check if the channel has trading signals
- Review the AI prompt in `image_analyzer.py`

## 📱 Production Deployment

### Backend
```bash
# Use gunicorn or uvicorn with systemd
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
# Build for production
npm run build

# Serve with nginx or deploy to Vercel/Netlify
```

## 🎨 Customization

### Change Colors
Edit `frontend/tailwind.config.js` to customize the theme

### Modify AI Prompt
Edit the prompt in `image_analyzer.py` line 93-132

### Add New Features
- Backend: Add endpoints in `api_server.py`
- Frontend: Create new components in `frontend/src/components/`

## 📞 Support

For issues or questions:
1. Check the error messages in the dashboard
2. Review the backend logs in the terminal
3. Check browser console for frontend errors

## 🎉 You're All Set!

Your automated trading bot is ready to:
- Monitor multiple Telegram channels 24/7
- Detect trading signals using AI
- Save all signals to Supabase
- Provide a beautiful dashboard for management

**Start the backend, start the frontend, add channels, and let it run!**

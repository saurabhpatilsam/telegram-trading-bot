# 🚀 Quick Start Guide

## Get Started in 5 Minutes!

### Step 1: Start the Backend (Terminal 1)

```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo
./start_backend.sh
```

Wait for the message: `✅ Starting API server on http://localhost:8000`

### Step 2: Start the Frontend (Terminal 2)

Open a **new terminal** window and run:

```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo
./start_frontend.sh
```

Wait for the message: `✅ Starting React app on http://localhost:3000`

### Step 3: Open the Dashboard

Your browser should automatically open to **http://localhost:3000**

If not, manually open: http://localhost:3000

### Step 4: Add Your First Channel

1. Click **"+ Add Channel"** button in the top right
2. Enter channel details:
   - **Name**: `Fx Tejas Community` (or any name you want)
   - **Username**: `https://t.me/Fxtejascommuinity` (or any channel)
3. Click **"Add Channel"**

### Step 5: Start Monitoring

1. Find your channel in the list
2. Click the **green "Start" button**
3. Wait for the first-time Telegram authentication (if needed)
4. Watch signals appear in real-time! 🎉

## 🎯 What Happens Next?

- ✅ Bot connects to Telegram
- ✅ Analyzes the last 10 messages
- ✅ Monitors for new messages 24/7
- ✅ Detects trading signals using AI
- ✅ Saves everything to your database

## 🔧 Managing Channels

### Add More Channels
- Click "+ Add Channel" anytime
- Add multiple channels
- Each runs independently

### Start/Stop
- **Green "Start" button**: Begin monitoring
- **Red "Stop" button**: Pause monitoring
- Channels remember their state

### Delete Channels
- Click the trash icon
- Confirms before deleting

## 📊 Viewing Signals

### All Signals
- Right panel shows all detected signals
- Auto-refreshes every 5 seconds

### Filter by Channel
- Click on a channel name
- See only signals from that channel
- Click again to show all

## 🎨 Dashboard Features

### Stats Cards (Top)
- Total Channels
- Active Channels
- Total Signals
- Signals Today

### Channel List (Left)
- All your channels
- Status indicators
- Quick controls

### Signal Feed (Right)
- Real-time signals
- BUY/SELL indicators
- Entry, SL, TP details

## ⚡ Tips

1. **Keep Both Terminals Running**
   - Backend must stay running
   - Frontend must stay running

2. **First-Time Setup**
   - You may need to enter Telegram code
   - Check your Telegram app
   - Enter the code in the backend terminal

3. **Check Logs**
   - Backend terminal shows all activity
   - Useful for debugging

4. **Restart Anytime**
   - Press Ctrl+C in terminals
   - Run start scripts again

## 🚨 Troubleshooting

### "Port already in use"
```bash
# Kill existing processes
pkill -f api_server
pkill -f "npm run dev"
```

### "Channel won't start"
- Check channel username is correct
- Make sure you're a member
- Check error message in dashboard

### "No signals detected"
- Wait a few minutes for messages
- Check if channel has trading content
- Review backend terminal logs

## 📱 Next Steps

1. **Add your other trading channels**
2. **Let it run 24/7**
3. **Check the dashboard regularly**
4. **All signals are in Supabase too!**

## 🎉 You're Ready!

The bot is now running and monitoring your Telegram channels. All signals will be detected automatically and saved to your database.

---

**Need help?** Check SETUP_GUIDE.md for detailed documentation.

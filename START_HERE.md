# 🚀 START HERE - Your Automated Trading Bot

## ⚡ Quick Start (Copy & Paste)

### Step 1️⃣: Start Backend (Terminal 1)
```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo && ./start_backend.sh
```

### Step 2️⃣: Start Frontend (Terminal 2 - New Window)
```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo && ./start_frontend.sh
```

### Step 3️⃣: Open Your Browser
```
http://localhost:3000
```

---

## 🎯 What You'll See

### Dashboard Overview
```
┌─────────────────────────────────────────────────────────────────┐
│  Telegram Trading Bot                        [+ Add Channel]    │
├─────────────────────────────────────────────────────────────────┤
│  📊 Stats Cards                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Total    │  │ Active   │  │ Total    │  │ Signals  │      │
│  │ Channels │  │ Channels │  │ Signals  │  │ Today    │      │
│  │    0     │  │    0     │  │    0     │  │    0     │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
├─────────────────────────────────────────────────────────────────┤
│  📱 Channels          │  📈 Trading Signals                     │
│  ┌────────────────┐  │  ┌─────────────────────────────────┐   │
│  │ No channels    │  │  │ No signals yet.                 │   │
│  │ added yet.     │  │  │ Add and start a channel.        │   │
│  │                │  │  │                                 │   │
│  │ Click +Add     │  │  │                                 │   │
│  │ Channel        │  │  │                                 │   │
│  └────────────────┘  │  └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 Example Usage

### 1. Add Your First Channel

Click **"+ Add Channel"** and enter:

```
Name: Fx Tejas Community
Username: https://t.me/Fxtejascommuinity
```

Or use the @username format:
```
Name: Trading Signals Pro
Username: @trading_channel
```

### 2. Start Monitoring

After adding, you'll see:

```
┌─────────────────────────────────────────┐
│ 🟢 Fx Tejas Community                  │
│ @Fxtejascommuinity                      │
│ Signals: 0 | Status: stopped            │
│ ┌─────────┐ ┌────┐                     │
│ │ ▶ Start │ │ 🗑️ │                     │
│ └─────────┘ └────┘                     │
└─────────────────────────────────────────┘
```

Click the **green "▶ Start"** button.

### 3. First-Time Telegram Authentication

**Check Terminal 1 (Backend)** - you'll see:
```
Please enter the code you received:
```

1. Check your Telegram app (phone with +447405502859)
2. You'll receive a login code (e.g., 12345)
3. Type the code in Terminal 1
4. Press Enter

### 4. Watch Signals Appear!

Once authenticated:
```
┌─────────────────────────────────────────┐
│ 🟢 Fx Tejas Community                  │
│ @Fxtejascommuinity                      │
│ Signals: 15 | Status: running           │
│ ┌─────────┐ ┌────┐                     │
│ │ ⏹ Stop  │ │ 🗑️ │                     │
│ └─────────┘ └────┘                     │
└─────────────────────────────────────────┘

Right Panel Shows:
┌─────────────────────────────────────────┐
│ 🟢 BUY XAUUSD                           │
│ Fx Tejas Community                      │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│ │Entry    │ │Stop Loss│ │TP       │   │
│ │4075.00  │ │4067.50  │ │4095.00  │   │
│ └─────────┘ └─────────┘ └─────────┘   │
│ 🕐 2 minutes ago                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 🔴 SELL USDJPY                          │
│ Fx Tejas Community                      │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│ │Entry    │ │Stop Loss│ │TP       │   │
│ │152.10   │ │152.30   │ │151.30   │   │
│ └─────────┘ └─────────┘ └─────────┘   │
│ 🕐 15 minutes ago                       │
└─────────────────────────────────────────┘
```

---

## 🎮 Controls

### Channel Controls
- **▶ Start** - Begin monitoring this channel
- **⏹ Stop** - Pause monitoring
- **🗑️ Delete** - Remove channel completely

### Signal Filtering
- Click on a **channel name** to filter signals
- Click again to show **all signals**

### Auto-Refresh
Dashboard automatically updates every **5 seconds**

---

## 💡 Tips

1. **Keep Both Terminals Running**
   - Don't close Terminal 1 (Backend)
   - Don't close Terminal 2 (Frontend)

2. **First Time Setup**
   - Only need Telegram code once per channel
   - Session is saved for future runs

3. **Multiple Channels**
   - Add as many as you want
   - Each runs independently
   - Start/stop each one individually

4. **View Logs**
   - Backend Terminal shows all activity
   - Useful for debugging

5. **Restart Anytime**
   - Ctrl+C in both terminals
   - Run start scripts again
   - All data is saved in database

---

## 📱 Your Configuration

✅ **Already Configured:**
- Telegram API ID: 20831057
- Telegram Phone: +447405502859
- Azure OpenAI: GPT-4o
- Supabase: Connected

✅ **Ready to Monitor:**
- Fx Tejas Community (https://t.me/Fxtejascommuinity)
- Any other public Telegram channel

---

## 🆘 Need Help?

### Port Already in Use?
```bash
# Kill backend
pkill -f api_server

# Kill frontend  
pkill -f "npm run dev"

# Try again
./start_backend.sh
./start_frontend.sh
```

### Can't Connect to Telegram?
- Check username is correct
- Make sure you're a member
- Try with @ prefix or full link

### No Signals?
- Wait a few minutes for new messages
- Check if channel has trading signals
- Look at backend terminal for errors

---

## 📚 More Documentation

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete overview
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design

---

## 🎉 You're Ready!

**Copy the commands above and start monitoring your Telegram channels now!** 🚀

The bot will automatically:
- ✅ Read all messages from your channels
- ✅ Analyze screenshots with AI
- ✅ Extract BUY/SELL signals
- ✅ Save everything to your database
- ✅ Display in beautiful dashboard
- ✅ Run 24/7 in the background

**Just start the two scripts and add your channels!**

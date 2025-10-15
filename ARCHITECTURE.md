# System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │     React + Tailwind Dashboard (Port 3000)                │ │
│  │  - Channel Management UI                                  │ │
│  │  - Real-time Signal Display                               │ │
│  │  - Statistics Dashboard                                   │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND SERVER                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │     FastAPI Server (Port 8000)                            │ │
│  │  - REST API Endpoints                                     │ │
│  │  - Channel Management                                     │ │
│  │  - Signal Retrieval                                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │     Channel Manager                                       │ │
│  │  - Creates/Manages Multiple Workers                       │ │
│  │  - Handles Start/Stop/Delete                              │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│              ┌───────────────┴───────────────┐                 │
│              ▼               ▼               ▼                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  Worker 1   │  │  Worker 2   │  │  Worker N   │           │
│  │ (Channel 1) │  │ (Channel 2) │  │ (Channel N) │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────────┘
         │                │                │
         │                │                │ Telegram API
         ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     TELEGRAM CHANNELS                           │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐             │
│  │ Channel 1  │   │ Channel 2  │   │ Channel N  │             │
│  │ Messages   │   │ Messages   │   │ Messages   │             │
│  └────────────┘   └────────────┘   └────────────┘             │
└─────────────────────────────────────────────────────────────────┘
         │
         │ New Messages
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SIGNAL PROCESSING                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Image Analyzer                                           │ │
│  │  - Azure OpenAI GPT-4o Vision                             │ │
│  │  - Analyzes Screenshots                                   │ │
│  │  - Extracts Trading Signals                               │ │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Text Parser                                              │ │
│  │  - Regex Pattern Matching                                │ │
│  │  - Extracts BUY/SELL/Entry/SL/TP                          │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
         │
         │ Validated Signals
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE                               │
│  ┌───────────────────┐         ┌───────────────────┐           │
│  │  SQLite Database  │         │  Supabase Cloud   │           │
│  │  (Local)          │────────▶│  (Backup)         │           │
│  │  - Channels       │         │  - trading_signals│           │
│  │  - Signals        │         │                   │           │
│  │  - Fast Access    │         │  - Cloud Backup   │           │
│  └───────────────────┘         └───────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (React)
- **Technology**: React 18, Vite, Tailwind CSS
- **Port**: 3000
- **Features**:
  - Real-time dashboard updates (5s refresh)
  - Channel CRUD operations
  - Signal filtering and display
  - Statistics visualization

### Backend (Python)
- **Technology**: FastAPI, SQLAlchemy, Telethon
- **Port**: 8000
- **Features**:
  - RESTful API
  - Async background workers
  - Multi-channel monitoring
  - Signal processing pipeline

### Signal Processing
- **Image Analysis**: Azure OpenAI GPT-4o Vision API
- **Text Parsing**: Regex-based pattern matching
- **Validation**: Ensures signals have required fields

### Data Storage
- **Local**: SQLite for fast access and reliability
- **Cloud**: Supabase for backup and external access
- **Sync**: Automatic sync to both databases

## Data Flow

1. **User Action** → Frontend sends request to Backend API
2. **Backend** → Creates/Manages Channel Monitor Worker
3. **Worker** → Connects to Telegram via Telethon
4. **Telegram** → Sends new messages to Worker
5. **Worker** → Processes message (text/image)
6. **AI/Parser** → Extracts trading signal
7. **Worker** → Validates signal
8. **Worker** → Saves to SQLite + Supabase
9. **Frontend** → Polls API for updates
10. **User** → Sees signals in dashboard

## Scalability

- ✅ Each channel runs in separate async worker
- ✅ Independent start/stop/restart
- ✅ Fault-tolerant (errors don't affect other channels)
- ✅ Can monitor dozens of channels simultaneously
- ✅ Local database for fast queries
- ✅ Cloud backup for redundancy

## Security

- 🔒 API keys in environment variables
- 🔒 Telegram sessions stored locally
- 🔒 CORS enabled for frontend only
- 🔒 No credentials in codebase
- 🔒 Supabase RLS can be enabled

## Performance

- ⚡ Async I/O for all operations
- ⚡ Background workers don't block API
- ⚡ SQLite for fast local queries
- ⚡ Efficient Telegram polling
- ⚡ Image analysis only when needed

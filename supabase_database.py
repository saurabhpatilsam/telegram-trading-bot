"""
Supabase database configuration and models
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Supabase connection details
SUPABASE_URL = "https://mfxrghawkoiemxgxfzti.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1meHJnaGF3a29pZW14Z3hmenRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxOTY1OTcsImV4cCI6MjA3NTc3MjU5N30.WmISPMi9nUvrpPnWoRigpG-woX_f4h4LC074_szLP5I"

# For PostgreSQL connection (Supabase uses PostgreSQL)
DATABASE_URL = f"postgresql://postgres.mfxrghawkoiemxgxfzti:{os.getenv('SUPABASE_DB_PASSWORD', 'your_db_password')}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

# Fallback to SQLite if Supabase connection fails
try:
    engine = create_engine(DATABASE_URL, echo=False)
    # Test connection
    engine.connect().close()
    print("✅ Connected to Supabase PostgreSQL database")
except Exception as e:
    print(f"⚠️ Could not connect to Supabase: {e}")
    print("📦 Falling back to SQLite database")
    DATABASE_URL = "sqlite:///./trading_bot.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Channel(Base):
    """Model for Telegram channels being monitored"""
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    signal_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Signal(Base):
    """Model for trading signals detected"""
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, nullable=True)  # Can be null for compatibility
    raw_text = Column(Text, nullable=False)
    action = Column(String(50), nullable=True)
    instrument = Column(String(100), nullable=True)
    entry_price = Column(String(50), nullable=True)
    stop_loss = Column(String(50), nullable=True)
    take_profits = Column(ARRAY(String), nullable=True)  # Array of strings for PostgreSQL
    message_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
def init_supabase_db():
    """Initialize Supabase database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

# Get DB session
def get_supabase_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Supabase client for direct API access
class SupabaseDirectClient:
    """Direct Supabase client using REST API"""
    
    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json'
        }
    
    async def get_channels(self):
        """Get all channels using Supabase REST API"""
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.url}/rest/v1/channels?select=*&order=created_at.desc",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return []
        except Exception as e:
            print(f"Error fetching channels: {e}")
            return []
    
    async def create_channel(self, name: str, username: str):
        """Create a new channel using Supabase REST API"""
        import aiohttp
        try:
            data = {
                "name": name,
                "username": username,
                "is_active": False,
                "signal_count": 0
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.url}/rest/v1/channels",
                    headers=self.headers,
                    json=data
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        return result[0] if result else None
                    else:
                        error_text = await response.text()
                        print(f"Error creating channel: {response.status} - {error_text}")
                        return None
        except Exception as e:
            print(f"Error creating channel: {e}")
            return None
    
    async def get_signals(self, limit: int = 20):
        """Get recent signals using Supabase REST API"""
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.url}/rest/v1/signals?select=*&order=created_at.desc&limit={limit}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return []
        except Exception as e:
            print(f"Error fetching signals: {e}")
            return []

# Global Supabase client instance
supabase_client = SupabaseDirectClient()

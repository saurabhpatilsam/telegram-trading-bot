from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Client for interacting with Supabase database"""
    
    def __init__(self, url: str, key: str, table_name: str = 'trading_signals'):
        """
        Initialize Supabase client
        
        Args:
            url: Supabase project URL
            key: Supabase anon/service key
            table_name: Name of the table to store signals
        """
        self.url = url
        self.key = key
        self.table_name = table_name
        self.client = None
        
        try:
            from supabase import create_client
            self.client = create_client(url, key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.warning(f"Could not initialize Supabase client: {str(e)}")
            logger.warning("Signals will only be stored locally")
    
    def insert_signal(self, signal: Dict) -> Optional[Dict]:
        """
        Insert a trading signal into Supabase
        
        Args:
            signal: Dictionary containing trading signal data
            
        Returns:
            Inserted record or None if failed
        """
        if not self.client:
            logger.debug("Supabase client not available, skipping cloud sync")
            return None
            
        try:
            # Prepare the record
            record = {
                'action': signal.get('action'),
                'instrument': signal.get('instrument'),
                'entry_price': signal.get('entry_price'),
                'stop_loss': signal.get('stop_loss'),
                'take_profits': signal.get('take_profits', []),
                'signal_type': signal.get('signal_type', 'unknown'),
                'raw_text': signal.get('raw_text', ''),
                'message_id': signal.get('message_id'),
                'message_date': signal.get('message_date'),
                'created_at': datetime.utcnow().isoformat(),
                'processed': False
            }
            
            # Insert into Supabase
            response = self.client.table(self.table_name).insert(record).execute()
            
            logger.info(f"✓ Signal synced to Supabase: {signal.get('action')} {signal.get('instrument')}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Error syncing signal to Supabase: {str(e)}")
            return None
    
    def get_recent_signals(self, limit: int = 10) -> list:
        """
        Retrieve recent trading signals
        
        Args:
            limit: Number of signals to retrieve
            
        Returns:
            List of signal records
        """
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error retrieving signals: {str(e)}")
            return []
    
    def update_signal_status(self, signal_id: int, processed: bool = True) -> bool:
        """
        Update the processed status of a signal
        
        Args:
            signal_id: ID of the signal to update
            processed: New processed status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table(self.table_name)\
                .update({'processed': processed})\
                .eq('id', signal_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Error updating signal status: {str(e)}")
            return False
    
    def create_table_if_not_exists(self):
        """
        Print SQL to create the trading_signals table
        Note: You need to run this SQL in your Supabase SQL editor
        """
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
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
        
        -- Create index for faster queries
        CREATE INDEX IF NOT EXISTS idx_created_at ON {self.table_name}(created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_processed ON {self.table_name}(processed);
        CREATE INDEX IF NOT EXISTS idx_instrument ON {self.table_name}(instrument);
        """
        
        print("\n" + "="*60)
        print("SUPABASE TABLE CREATION SQL")
        print("="*60)
        print("Run this SQL in your Supabase SQL Editor:")
        print(sql)
        print("="*60 + "\n")

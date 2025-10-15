import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Telegram to Supabase Trading Bot"""
    
    # Telegram Configuration
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE')
    TELEGRAM_GROUP_USERNAME = os.getenv('TELEGRAM_GROUP_USERNAME')
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_TABLE = os.getenv('SUPABASE_TABLE', 'trading_signals')
    
    # Azure OpenAI Configuration (optional)
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        required_fields = [
            ('TELEGRAM_API_ID', cls.TELEGRAM_API_ID),
            ('TELEGRAM_API_HASH', cls.TELEGRAM_API_HASH),
            ('TELEGRAM_PHONE', cls.TELEGRAM_PHONE),
            ('TELEGRAM_GROUP_USERNAME', cls.TELEGRAM_GROUP_USERNAME),
            ('SUPABASE_URL', cls.SUPABASE_URL),
            ('SUPABASE_KEY', cls.SUPABASE_KEY),
        ]
        
        missing = [field for field, value in required_fields if not value]
        
        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}. "
                "Please check your .env file."
            )
        
        return True

import re
from typing import Dict, Optional, List

class TradingSignalParser:
    """Parse trading signals from text messages"""
    
    def __init__(self):
        # Common patterns for trading signals
        self.patterns = {
            'action': r'\b(BUY|SELL|LONG|SHORT)\b',
            'instrument': r'\b([A-Z]{3,6}(?:USD|USDT|BTC|ETH)?)\b',
            'entry': r'(?:ENTRY|ENTER|BUY AT|SELL AT)[:\s]+([0-9]+\.?[0-9]*)',
            'stop_loss': r'(?:SL|STOP LOSS|STOPLOSS)[:\s]+([0-9]+\.?[0-9]*)',
            'take_profit': r'(?:TP|TAKE PROFIT|TARGET)[:\s]*([0-9]+\.?[0-9]*)',
            'price': r'(?:PRICE|@)[:\s]+([0-9]+\.?[0-9]*)',
        }
    
    def parse_message(self, text: str) -> Optional[Dict]:
        """
        Parse a text message and extract trading signal information
        
        Args:
            text: The message text to parse
            
        Returns:
            Dictionary with trading signal data or None if no signal found
        """
        if not text:
            return None
        
        # Convert to uppercase for easier matching
        text_upper = text.upper()
        
        # Extract action (BUY/SELL)
        action_match = re.search(self.patterns['action'], text_upper)
        if not action_match:
            return None  # Not a trading signal
        
        action = action_match.group(1)
        # Normalize LONG to BUY and SHORT to SELL
        if action == 'LONG':
            action = 'BUY'
        elif action == 'SHORT':
            action = 'SELL'
        
        # Extract instrument/symbol
        instrument_match = re.search(self.patterns['instrument'], text_upper)
        instrument = instrument_match.group(1) if instrument_match else None
        
        # Extract entry price
        entry_match = re.search(self.patterns['entry'], text_upper)
        if not entry_match:
            # Try to find price pattern
            entry_match = re.search(self.patterns['price'], text_upper)
        entry_price = float(entry_match.group(1)) if entry_match else None
        
        # Extract stop loss
        sl_match = re.search(self.patterns['stop_loss'], text_upper)
        stop_loss = float(sl_match.group(1)) if sl_match else None
        
        # Extract take profit targets
        tp_matches = re.findall(self.patterns['take_profit'], text_upper)
        take_profits = [float(tp) for tp in tp_matches] if tp_matches else []
        
        # Build the signal dictionary
        signal = {
            'action': action,
            'instrument': instrument,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'raw_text': text,
            'signal_type': 'text'
        }
        
        return signal
    
    def parse_multiple_targets(self, text: str) -> List[Dict]:
        """
        Parse messages that might contain multiple TP levels
        Returns a list of signals with different TP targets
        """
        base_signal = self.parse_message(text)
        if not base_signal:
            return []
        
        # If multiple TPs, create separate entries or combine them
        return [base_signal]
    
    def validate_signal(self, signal: Dict) -> bool:
        """
        Validate that a signal has the minimum required information
        
        Args:
            signal: The signal dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['action', 'instrument']
        return all(signal.get(field) for field in required_fields)

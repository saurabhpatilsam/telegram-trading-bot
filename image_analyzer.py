import os
from typing import Dict, Optional
from PIL import Image
import io

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    from openai import AzureOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from text_parser import TradingSignalParser

class ImageAnalyzer:
    """Analyze images to extract trading signals"""
    
    def __init__(self, azure_endpoint: Optional[str] = None, azure_api_key: Optional[str] = None, azure_deployment: Optional[str] = None):
        self.text_parser = TradingSignalParser()
        self.azure_endpoint = azure_endpoint
        self.azure_api_key = azure_api_key
        self.azure_deployment = azure_deployment
        
        if azure_endpoint and azure_api_key and OPENAI_AVAILABLE:
            self.openai_client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                api_version="2025-01-01-preview"
            )
            self.use_openai = True
        else:
            self.openai_client = None
            self.use_openai = False
    
    def analyze_image_with_ocr(self, image_bytes: bytes) -> Optional[str]:
        """
        Extract text from image using OCR (Tesseract)
        
        Args:
            image_bytes: The image file as bytes
            
        Returns:
            Extracted text or None if OCR fails
        """
        if not TESSERACT_AVAILABLE:
            print("Warning: pytesseract not available. Install it for OCR support.")
            return None
        
        try:
            # Open image from bytes
            image = Image.open(io.BytesIO(image_bytes))
            
            # Extract text using OCR
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"OCR extraction failed: {str(e)}")
            return None
    
    def analyze_image_with_openai(self, image_bytes: bytes) -> Optional[Dict]:
        """
        Analyze image using OpenAI Vision API to extract trading signals
        
        Args:
            image_bytes: The image file as bytes
            
        Returns:
            Trading signal dictionary or None
        """
        if not self.use_openai:
            return None
        
        try:
            import base64
            
            # Encode image to base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            # Call Azure OpenAI Vision API
            response = self.openai_client.chat.completions.create(
                model=self.azure_deployment,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """You are a trading signal analyzer. Carefully examine this image and determine:

1. **INTENT**: Is this a TRADING SIGNAL (future trade setup) or a TRADE RESULT (past trade outcome)?
   - Trading signals have: entry zones, pending orders, future setup indicators, "wait for", "looking for"
   - Trade results have: profit/loss amounts, "closed", "hit TP", equity changes, completed trades
   
2. **ONLY extract signals if this is a TRADING SIGNAL (pre-trade setup)**. Ignore trade results.

3. If this IS a trading signal, extract:
   - Action: BUY/SELL/LONG/SHORT (look at text, arrows, or chart patterns)
   - Instrument: The trading pair/symbol (EURUSD, XAUUSD, BTCUSDT, etc.)
   - Entry Price: The exact entry price or zone (look for "Entry", "Buy at", "Sell at", price levels)
   - Stop Loss (SL): The stop loss level (may be marked with red line, "SL:", or below entry for buy/above for sell)
   - Take Profit (TP): All target levels (TP1, TP2, TP3, or marked zones on chart)

4. **Look at drawings/annotations**: 
   - Lines, arrows, boxes indicating entry zones
   - Red lines often = Stop Loss
   - Green lines often = Take Profit
   - Horizontal lines with prices
   - Text annotations

5. **Respond ONLY if this is a trading signal**. Use this exact format:

SIGNAL_TYPE: [TRADE_SIGNAL or TRADE_RESULT]
ACTION: [BUY/SELL/LONG/SHORT or N/A]
INSTRUMENT: [exact symbol like EURUSD, XAUUSD, etc. or N/A]
ENTRY: [exact price number or N/A]
SL: [exact price number or N/A]
TP: [comma-separated prices like 1.2000, 1.2100 or N/A]

If SIGNAL_TYPE is TRADE_RESULT, respond with:
SIGNAL_TYPE: TRADE_RESULT
ACTION: N/A
INSTRUMENT: N/A
ENTRY: N/A
SL: N/A
TP: N/A

Be precise with numbers. Extract exact prices from the image."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=800
            )
            
            # Parse the response
            content = response.choices[0].message.content
            return self.text_parser.parse_message(content)
            
        except Exception as e:
            print(f"OpenAI Vision analysis failed: {str(e)}")
            return None
    
    def analyze_image(self, image_bytes: bytes) -> Optional[Dict]:
        """
        Analyze an image to extract trading signals
        Tries OpenAI first, then falls back to OCR
        
        Args:
            image_bytes: The image file as bytes
            
        Returns:
            Trading signal dictionary or None
        """
        # Try OpenAI Vision first if available
        if self.use_openai:
            signal = self.analyze_image_with_openai(image_bytes)
            if signal and self.text_parser.validate_signal(signal):
                return signal
        
        # Fall back to OCR
        extracted_text = self.analyze_image_with_ocr(image_bytes)
        if extracted_text:
            signal = self.text_parser.parse_message(extracted_text)
            if signal and self.text_parser.validate_signal(signal):
                return signal
        
        return None

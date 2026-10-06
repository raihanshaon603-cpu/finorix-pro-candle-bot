import pandas as pd
from strategy import evaluate_signal
from logger import log_signal
from playsound import playsound
import os

class CandleBot:
    def __init__(self, config):
        self.config = config
        self.df = pd.DataFrame(columns=["open", "high", "low", "close", "time"])
        self.last_signal = None
        self.last_pattern = None
    
    def add_candle(self, candle: dict):
        """Add a new candle to the data"""
        row = {
            "time": candle.get("time"),
            "open": float(candle["open"]),
            "high": float(candle["high"]),
            "low": float(candle["low"]),
            "close": float(candle["close"]),
        }
        self.df = pd.concat([self.df, pd.DataFrame([row])], ignore_index=True)
    
    def update(self) -> dict:
        """Process latest candle and generate signal"""
        if len(self.df) < self.config.min_candles:
            return {"signal": "WAIT", "reason": "Loading data..."}
        
        result = evaluate_signal(self.df, self.config)
        
        # Only alert on new signals (not repeats)
        if result["signal"] != "WAIT" and result["signal"] != self.last_signal:
            self.last_signal = result["signal"]
            
            if self.config.log_signals:
                log_signal(result, self.config.symbol)
            
            if self.config.alert_sound:
                self.play_alert(result["signal"])
        
        return result
    
    def play_alert(self, signal: str):
        """Play alert sound"""
        try:
            if signal == "BUY":
                # You can replace this with any .wav file path
                # For now, we'll just print
                print(f"\n🔔 ALERT: {signal} Signal Generated!")
            elif signal == "SELL":
                print(f"\n🔔 ALERT: {signal} Signal Generated!")
        except Exception as e:
            print(f"Alert error: {e}")
    
    def get_stats(self) -> dict:
        """Get bot statistics"""
        if len(self.df) == 0:
            return {"candles": 0, "last_price": 0}
        
        return {
            "candles": len(self.df),
            "last_price": float(self.df["close"].iloc[-1]),
            "high_52": float(self.df["high"].tail(52).max()),
            "low_52": float(self.df["low"].tail(52).min()),
        }

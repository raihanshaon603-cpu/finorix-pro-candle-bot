import pandas as pd
from config import BotConfig
from bot import CandleBot
import time

def load_sample_data():
    """Load sample candle data for testing"""
    data = [
        {"time": "2024-01-01 00:00", "open": 1.1000, "high": 1.1010, "low": 1.0990, "close": 1.1005},
        {"time": "2024-01-01 00:01", "open": 1.1005, "high": 1.1015, "low": 1.0995, "close": 1.1010},
        {"time": "2024-01-01 00:02", "open": 1.1010, "high": 1.1020, "low": 1.1000, "close": 1.1002},
        {"time": "2024-01-01 00:03", "open": 1.1002, "high": 1.1012, "low": 1.0998, "close": 1.0999},
        {"time": "2024-01-01 00:04", "open": 1.0999, "high": 1.1008, "low": 1.0992, "close": 1.1006},
        {"time": "2024-01-01 00:05", "open": 1.1006, "high": 1.1018, "low": 1.1000, "close": 1.1015},
        {"time": "2024-01-01 00:06", "open": 1.1015, "high": 1.1025, "low": 1.1010, "close": 1.1008},
        {"time": "2024-01-01 00:07", "open": 1.1008, "high": 1.1020, "low": 1.1005, "close": 1.1018},
        {"time": "2024-01-01 00:08", "open": 1.1018, "high": 1.1030, "low": 1.1015, "close": 1.1025},
        {"time": "2024-01-01 00:09", "open": 1.1025, "high": 1.1035, "low": 1.1020, "close": 1.1032},
    ]
    return data

def main():
    print("="*60)
    print(" FINORIX PRO - Advanced Candlestick Pattern Bot")
    print("="*60)
    print()
    
    # Initialize bot
    config = BotConfig(
        symbol="EURUSD",
        timeframe="M1",
        trend_confirmation=True,
        require_rsi_filter=True,
        alert_sound=True
    )
    
    bot = CandleBot(config)
    
    # Load sample data
    print("Loading sample data...")
    sample_data = load_sample_data()
    
    for candle in sample_data:
        bot.add_candle(candle)
    
    print(f"Loaded {len(sample_data)} candles\n")
    
    # Run bot
    print("Running bot analysis...\n")
    
    for i in range(len(bot.df)):
        signal = bot.update()
        
        if signal["signal"] != "WAIT":
            print(f"\n{'='*60}")
            print(f"Signal: {signal['signal']}")
            print(f"Confidence: {signal['confidence']:.2%}")
            print(f"Pattern: {signal.get('pattern', 'N/A')}")
            print(f"Reason: {signal['reason']}")
            if 'entry' in signal:
                print(f"Entry Price: {signal['entry']:.5f}")
            if 'support' in signal and signal['support']:
                print(f"Support Level: {signal['support']:.5f}")
            if 'resistance' in signal and signal['resistance']:
                print(f"Resistance Level: {signal['resistance']:.5f}")
            print(f"{'='*60}")
        else:
            print(f"Candle {i+1}: {signal['reason']}")
    
    print("\n" + "="*60)
    print("Bot Statistics:")
    stats = bot.get_stats()
    print(f"Total Candles Processed: {stats['candles']}")
    print(f"Current Price: {stats['last_price']:.5f}")
    print(f"52-Candle High: {stats['high_52']:.5f}")
    print(f"52-Candle Low: {stats['low_52']:.5f}")
    print("="*60)

if __name__ == "__main__":
    main()

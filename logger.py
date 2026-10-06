import csv
from datetime import datetime
import os

def ensure_log_file():
    """Create log file with headers if it doesn't exist"""
    if not os.path.exists("trade_signals.csv"):
        with open("trade_signals.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp",
                "Symbol",
                "Signal",
                "Confidence",
                "Pattern",
                "Reason",
                "Entry_Price",
                "Support",
                "Resistance"
            ])

def log_signal(signal_data: dict, symbol: str):
    """Log a trading signal to CSV"""
    ensure_log_file()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("trade_signals.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            symbol,
            signal_data.get("signal", "WAIT"),
            f"{signal_data.get('confidence', 0):.2f}",
            signal_data.get("pattern", "-"),
            signal_data.get("reason", "-"),
            f"{signal_data.get('entry', 0):.5f}",
            f"{signal_data.get('support', 0):.5f}" if signal_data.get('support') else "-",
            f"{signal_data.get('resistance', 0):.5f}" if signal_data.get('resistance') else "-"
        ])

def get_recent_signals(limit: int = 10) -> list:
    """Get recent signals from log"""
    if not os.path.exists("trade_signals.csv"):
        return []
    
    signals = []
    with open("trade_signals.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            signals.append(row)
    
    return signals[-limit:]

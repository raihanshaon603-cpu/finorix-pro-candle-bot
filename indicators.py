import pandas as pd
import numpy as np

def ema(series: pd.Series, period: int) -> pd.Series:
    """Exponential Moving Average"""
    return series.ewm(span=period, adjust=False).mean()

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index"""
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    
    rolling_up = up.ewm(com=period - 1, adjust=False).mean()
    rolling_down = down.ewm(com=period - 1, adjust=False).mean()
    
    rs = rolling_up / rolling_down.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))

def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range"""
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift(1)).abs()
    low_close = (df["low"] - df["close"].shift(1)).abs()
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.rolling(window=period).mean()

def support_resistance(df: pd.DataFrame, window: int = 20):
    """Calculate support and resistance levels"""
    if len(df) < window:
        return None, None
    recent = df.tail(window)
    support = recent["low"].min()
    resistance = recent["high"].max()
    return support, resistance

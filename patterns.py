import pandas as pd

def is_bullish_engulfing(df: pd.DataFrame, idx: int) -> bool:
    """Two-candle bullish pattern: second candle engulfs first"""
    if idx == 0:
        return False
    
    prev = df.iloc[idx - 1]
    curr = df.iloc[idx]
    
    prev_body = abs(prev["close"] - prev["open"])
    curr_body = abs(curr["close"] - curr["open"])
    
    return (
        prev["close"] < prev["open"] and  # Prev candle is red
        curr["close"] > curr["open"] and  # Curr candle is green
        curr["open"] <= prev["close"] and  # Opens below prev close
        curr["close"] >= prev["open"] and  # Closes above prev open
        curr_body > prev_body  # Larger body
    )

def is_bearish_engulfing(df: pd.DataFrame, idx: int) -> bool:
    """Two-candle bearish pattern: second candle engulfs first"""
    if idx == 0:
        return False
    
    prev = df.iloc[idx - 1]
    curr = df.iloc[idx]
    
    prev_body = abs(prev["close"] - prev["open"])
    curr_body = abs(curr["close"] - curr["open"])
    
    return (
        prev["close"] > prev["open"] and  # Prev candle is green
        curr["close"] < curr["open"] and  # Curr candle is red
        curr["open"] >= prev["close"] and  # Opens above prev close
        curr["close"] <= prev["open"] and  # Closes below prev open
        curr_body > prev_body  # Larger body
    )

def is_doji(df: pd.DataFrame, idx: int, body_threshold: float = 0.08) -> bool:
    """Doji pattern: open and close are very close"""
    candle = df.iloc[idx]
    body = abs(candle["close"] - candle["open"])
    range_size = candle["high"] - candle["low"]
    
    if range_size == 0:
        return False
    
    return body <= range_size * body_threshold

def is_hammer(df: pd.DataFrame, idx: int) -> bool:
    """Hammer pattern: small body with long lower wick"""
    candle = df.iloc[idx]
    body = abs(candle["close"] - candle["open"])
    range_size = candle["high"] - candle["low"]
    
    if range_size == 0:
        return False
    
    lower_wick = candle["open"] - candle["low"] if candle["close"] > candle["open"] else candle["close"] - candle["low"]
    
    return (
        candle["close"] > candle["open"] and
        body < range_size * 0.4 and
        lower_wick > range_size * 0.5
    )

def is_shooting_star(df: pd.DataFrame, idx: int) -> bool:
    """Shooting star pattern: small body with long upper wick"""
    candle = df.iloc[idx]
    body = abs(candle["close"] - candle["open"])
    range_size = candle["high"] - candle["low"]
    
    if range_size == 0:
        return False
    
    upper_wick = candle["high"] - (candle["open"] if candle["close"] < candle["open"] else candle["close"])
    
    return (
        candle["close"] < candle["open"] and
        body < range_size * 0.4 and
        upper_wick > range_size * 0.5
    )

def is_morning_star(df: pd.DataFrame, idx: int) -> bool:
    """Three-candle bullish pattern: down, small, up"""
    if idx < 2:
        return False
    
    prev1 = df.iloc[idx - 2]
    prev2 = df.iloc[idx - 1]
    curr = df.iloc[idx]
    
    down1 = prev1["close"] < prev1["open"]
    small_body = abs(prev2["close"] - prev2["open"]) < abs(prev1["high"] - prev1["low"]) * 0.3
    up_curr = curr["close"] > curr["open"]
    
    return down1 and small_body and up_curr and curr["close"] > prev1["open"]

def is_evening_star(df: pd.DataFrame, idx: int) -> bool:
    """Three-candle bearish pattern: up, small, down"""
    if idx < 2:
        return False
    
    prev1 = df.iloc[idx - 2]
    prev2 = df.iloc[idx - 1]
    curr = df.iloc[idx]
    
    up1 = prev1["close"] > prev1["open"]
    small_body = abs(prev2["close"] - prev2["open"]) < abs(prev1["high"] - prev1["low"]) * 0.3
    down_curr = curr["close"] < curr["open"]
    
    return up1 and small_body and down_curr and curr["close"] < prev1["open"]

def get_pattern_name(pattern: str) -> str:
    """Return readable pattern name"""
    names = {
        "bullish_engulfing": "Bullish Engulfing",
        "bearish_engulfing": "Bearish Engulfing",
        "hammer": "Hammer",
        "shooting_star": "Shooting Star",
        "morning_star": "Morning Star",
        "evening_star": "Evening Star",
        "doji": "Doji",
    }
    return names.get(pattern, pattern)

def detect_patterns(df: pd.DataFrame, idx: int) -> dict:
    """Detect all patterns at given index"""
    patterns = {}
    
    patterns["bullish_engulfing"] = is_bullish_engulfing(df, idx)
    patterns["bearish_engulfing"] = is_bearish_engulfing(df, idx)
    patterns["hammer"] = is_hammer(df, idx)
    patterns["shooting_star"] = is_shooting_star(df, idx)
    patterns["morning_star"] = is_morning_star(df, idx)
    patterns["evening_star"] = is_evening_star(df, idx)
    patterns["doji"] = is_doji(df, idx)
    
    return patterns

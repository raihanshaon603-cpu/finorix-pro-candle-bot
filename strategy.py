import pandas as pd
from indicators import ema, rsi, support_resistance
from patterns import detect_patterns

def evaluate_signal(df: pd.DataFrame, config) -> dict:
    """Main strategy logic - generates BUY/SELL signals"""
    if len(df) < config.min_candles:
        return {
            "signal": "WAIT",
            "reason": f"Not enough candles ({len(df)}/{config.min_candles})",
            "confidence": 0.0,
            "pattern": None
        }
    
    # Calculate indicators
    close = df["close"]
    fast = ema(close, config.ema_fast)
    slow = ema(close, config.ema_slow)
    rsi_values = rsi(close, config.rsi_period)
    
    last_idx = len(df) - 1
    last_close = close.iloc[last_idx]
    fast_ema = fast.iloc[last_idx]
    slow_ema = slow.iloc[last_idx]
    rsi_last = rsi_values.iloc[last_idx]
    
    # Trend detection
    trend_bullish = fast_ema > slow_ema
    trend_bearish = fast_ema < slow_ema
    trend_neutral = abs(fast_ema - slow_ema) < (slow_ema * 0.001)
    
    # Support/Resistance
    support, resistance = support_resistance(df, window=20)
    
    # Pattern detection
    patterns = detect_patterns(df, last_idx)
    detected_pattern = None
    for pattern, detected in patterns.items():
        if detected:
            detected_pattern = pattern
            break
    
    # Signal generation
    confidence = 0.0
    
    # Bullish signals
    if patterns["bullish_engulfing"] or patterns["hammer"] or patterns["morning_star"]:
        if trend_bullish:
            confidence = 0.9
            pattern_name = detected_pattern
        elif trend_neutral:
            confidence = 0.7
            pattern_name = detected_pattern
        else:
            confidence = 0.4
            pattern_name = detected_pattern
        
        if config.require_rsi_filter:
            if rsi_last > config.rsi_overbought:
                confidence *= 0.5
                return {
                    "signal": "WAIT",
                    "reason": f"Bullish pattern but RSI overbought ({rsi_last:.1f})",
                    "confidence": confidence,
                    "pattern": pattern_name
                }
        
        if confidence >= 0.6:
            return {
                "signal": "BUY",
                "reason": f"{pattern_name} + Bullish Trend (RSI: {rsi_last:.1f})",
                "confidence": confidence,
                "pattern": pattern_name,
                "entry": last_close,
                "support": support,
                "resistance": resistance
            }
    
    # Bearish signals
    if patterns["bearish_engulfing"] or patterns["shooting_star"] or patterns["evening_star"]:
        if trend_bearish:
            confidence = 0.9
            pattern_name = detected_pattern
        elif trend_neutral:
            confidence = 0.7
            pattern_name = detected_pattern
        else:
            confidence = 0.4
            pattern_name = detected_pattern
        
        if config.require_rsi_filter:
            if rsi_last < config.rsi_oversold:
                confidence *= 0.5
                return {
                    "signal": "WAIT",
                    "reason": f"Bearish pattern but RSI oversold ({rsi_last:.1f})",
                    "confidence": confidence,
                    "pattern": pattern_name
                }
        
        if confidence >= 0.6:
            return {
                "signal": "SELL",
                "reason": f"{pattern_name} + Bearish Trend (RSI: {rsi_last:.1f})",
                "confidence": confidence,
                "pattern": pattern_name,
                "entry": last_close,
                "support": support,
                "resistance": resistance
            }
    
    # Reversal signals based on RSI extremes
    if rsi_last < config.rsi_oversold and trend_bullish:
        return {
            "signal": "BUY",
            "reason": f"Oversold Bounce (RSI: {rsi_last:.1f})",
            "confidence": 0.65,
            "pattern": "RSI_Oversold",
            "entry": last_close,
            "support": support,
            "resistance": resistance
        }
    
    if rsi_last > config.rsi_overbought and trend_bearish:
        return {
            "signal": "SELL",
            "reason": f"Overbought Reversal (RSI: {rsi_last:.1f})",
            "confidence": 0.65,
            "pattern": "RSI_Overbought",
            "entry": last_close,
            "support": support,
            "resistance": resistance
        }
    
    return {
        "signal": "WAIT",
        "reason": "No valid signal",
        "confidence": 0.0,
        "pattern": None
    }

from dataclasses import dataclass

@dataclass
class BotConfig:
    symbol: str = "EURUSD"
    timeframe: str = "M1"
    
    # Indicators
    ema_fast: int = 9
    ema_slow: int = 21
    rsi_period: int = 14
    rsi_overbought: int = 70
    rsi_oversold: int = 30
    atr_period: int = 14
    
    # Risk Management
    risk_percent: float = 0.02
    stop_loss_pips: float = 15
    take_profit_pips: float = 30
    
    # Strategy
    min_candles: int = 50
    trend_confirmation: bool = True
    require_rsi_filter: bool = True
    
    # Display
    alert_sound: bool = True
    desktop_notification: bool = True
    log_signals: bool = True

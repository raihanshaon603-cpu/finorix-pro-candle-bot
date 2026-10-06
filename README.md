# Finorix Pro - Advanced Candlestick Pattern Recognition Bot

A professional-grade Python desktop bot for detecting candlestick patterns and generating trading signals for Quotex and other markets.

## Features

✅ **Advanced Candlestick Pattern Recognition**
- Bullish Engulfing
- Bearish Engulfing
- Hammer & Shooting Star
- Morning Star & Evening Star
- Doji Pattern Detection

✅ **Technical Indicators**
- Exponential Moving Average (EMA)
- Relative Strength Index (RSI)
- Average True Range (ATR)
- Support & Resistance Levels

✅ **Smart Signal Generation**
- Trend confirmation
- RSI filter for overbought/oversold
- Confidence scoring (0-100%)
- Risk management rules

✅ **Signal Logging & Alerts**
- CSV export of all signals
- Desktop notifications
- Alert sound system
- Trade history tracking

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/raihanshaon603-cpu/finorix-pro-candle-bot.git
cd finorix-pro-candle-bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
python main.py
```

This will:
1. Load sample candle data
2. Analyze each candle for patterns
3. Generate BUY/SELL signals
4. Log signals to `trade_signals.csv`
5. Display statistics

### Configuration

Edit `config.py` to customize:

```python
config = BotConfig(
    symbol="EURUSD",
    timeframe="M1",
    ema_fast=9,          # Fast moving average
    ema_slow=21,         # Slow moving average
    rsi_period=14,       # RSI period
    rsi_overbought=70,   # Overbought threshold
    rsi_oversold=30,     # Oversold threshold
    trend_confirmation=True,  # Require trend match
    require_rsi_filter=True,  # Use RSI filter
    alert_sound=True,         # Enable alerts
    log_signals=True          # Log to CSV
)
```

## How to Use with Quotex

### Without API (Recommended)

1. **Run the bot** with your candle data
2. **Monitor signals** in the terminal or CSV
3. **Check `trade_signals.csv`** for recommended trades
4. **Manually place trades** on Quotex based on signals
5. **Track performance** and refine parameters

### Signal Interpretation

**BUY Signal:**
- High confidence (60%+)
- Bullish candlestick pattern detected
- Trend aligned
- RSI not overbought

**SELL Signal:**
- High confidence (60%+)
- Bearish candlestick pattern detected
- Trend aligned
- RSI not oversold

## File Structure

```
finorix-pro-candle-bot/
├── main.py              # Entry point
├── config.py            # Configuration
├── bot.py               # Main bot class
├── indicators.py        # Technical indicators
├── patterns.py          # Pattern recognition
├── strategy.py          # Signal logic
├── logger.py            # Signal logging
├── requirements.txt     # Dependencies
├── README.md            # This file
└── trade_signals.csv    # Signal log (auto-generated)
```

## Signal CSV Format

`trade_signals.csv` contains:

| Column | Description |
|--------|-------------|
| Timestamp | When signal was generated |
| Symbol | Trading pair (e.g., EURUSD) |
| Signal | BUY, SELL, or WAIT |
| Confidence | Signal confidence (0.0-1.0) |
| Pattern | Detected pattern name |
| Reason | Detailed reason for signal |
| Entry_Price | Current price at signal |
| Support | Support level |
| Resistance | Resistance level |

## Candlestick Patterns Explained

### Bullish Patterns (BUY Signals)

**Bullish Engulfing**
- Red candle followed by green candle
- Green candle completely engulfs red
- Indicates uptrend reversal

**Hammer**
- Small body with long lower wick
- Suggests rejection of lower prices
- Bullish reversal signal

**Morning Star**
- Three-candle pattern: down → small → up
- Signals trend reversal to upside
- Strong bullish signal

### Bearish Patterns (SELL Signals)

**Bearish Engulfing**
- Green candle followed by red candle
- Red candle completely engulfs green
- Indicates downtrend reversal

**Shooting Star**
- Small body with long upper wick
- Suggests rejection of higher prices
- Bearish reversal signal

**Evening Star**
- Three-candle pattern: up → small → down
- Signals trend reversal to downside
- Strong bearish signal

**Doji**
- Open and close are nearly identical
- Signals indecision
- Needs trend confirmation

## Risk Management

The bot includes:
- Stop-loss recommendations (15 pips default)
- Take-profit targets (30 pips default)
- Risk-per-trade limits (2% default)
- Support/Resistance levels

## Backtesting

To backtest with historical data:

1. Prepare CSV with columns: `time`, `open`, `high`, `low`, `close`
2. Load in `main.py`:
```python
df = pd.read_csv('your_data.csv')
for _, row in df.iterrows():
    bot.add_candle(row.to_dict())
    bot.update()
```

## Performance Tips

1. **Adjust parameters** for different market conditions
2. **Test on demo** before live trading
3. **Use trend confirmation** for higher accuracy
4. **Monitor RSI filter** to avoid false signals
5. **Track performance** in the CSV log
6. **Refine** based on results

## Limitations

- Signal-based only (no auto-trading without API)
- Requires manual trade placement on Quotex
- Past patterns don't guarantee future results
- No guaranteed profit

## Disclaimer

This bot is for educational and informational purposes only. Trading and investing involve substantial risk of loss. Past performance does not guarantee future results. Always trade responsibly and at your own risk.

## Future Enhancements

- [ ] Desktop GUI with PySide6
- [ ] Real-time chart display
- [ ] Backtesting engine
- [ ] Multiple timeframe analysis
- [ ] Discord/Telegram alerts
- [ ] Performance dashboard

## Support

For issues or questions, create an issue on GitHub.

## License

MIT License - Feel free to use and modify

---

**Made with ❤️ for traders by traders**

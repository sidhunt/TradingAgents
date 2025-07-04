# Live Trading with SnapTrade Integration

This module provides live trading capabilities for your personal TradingAgents system using SnapTrade's unified API to connect with 20+ brokerages.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Run the setup script
chmod +x setup_snaptrade.sh
./setup_snaptrade.sh

# Or install manually
pip install snaptrade-python-sdk>=11.0.110 python-dotenv pytz
```

### 2. Set Up SnapTrade Account

1. **Create Account**: Visit [SnapTrade Dashboard](https://dashboard.snaptrade.com/)
2. **Get API Keys**: Generate your Client ID and Consumer Key
3. **Connect Brokerage**: Link your brokerage account through SnapTrade

### 3. Configure Environment Variables

```bash
export SNAPTRADE_CLIENT_ID="your_client_id_here"
export SNAPTRADE_CONSUMER_KEY="your_consumer_key_here"
export ENABLE_LIVE_TRADING="false"  # Set to "true" for live trading
```

### 4. Test Your Setup

```bash
# Check connection status
python -m cli.main live status

# Start paper trading
python -m cli.main live start --paper

# For live trading (REAL MONEY - BE CAREFUL!)
python -m cli.main live start --no-paper
```

## 🔧 CLI Commands

### `live setup`
Display setup instructions for SnapTrade integration.

### `live status`
Check your SnapTrade connection and environment configuration.

### `live start`
Start the continuous trading agent.

**Options:**
- `--balance, -b`: Initial trading balance (default: $100)
- `--paper, -p`: Use paper trading mode (default: true)
- `--yes, -y`: Skip confirmation prompts

**Examples:**
```bash
# Start paper trading with $500
python -m cli.main live start --balance 500 --paper

# Start live trading (requires confirmation)
python -m cli.main live start --no-paper

# Start live trading with auto-confirmation (DANGEROUS!)
python -m cli.main live start --no-paper --yes
```

### `live install`
Install the SnapTrade SDK and dependencies.

## 🤖 How It Works

### Agent Workflow

The live trading system follows this continuous workflow:

1. **Market Hours Check** (every 5 minutes when closed)
   - Only trades during market hours (9:30 AM - 4:00 PM ET)
   - Waits during weekends and holidays

2. **Market Analysis** (every 15 minutes during market hours)
   - Market Analyst: Overall market conditions
   - News Analyst: Breaking news impact
   - Fundamentals Analyst: Technical indicators

3. **Research & Debate** (every 30 minutes)
   - Bull Researcher: Bullish opportunities
   - Bear Researcher: Risk warnings
   - Research Manager: Final recommendations

4. **Trading Decisions** (continuous)
   - Trader Agent: Execute based on consensus
   - Risk Manager: Position sizing and limits
   - Portfolio Manager: Final approval

5. **Position Management** (continuous)
   - Stop loss monitoring (-5% default)
   - Take profit targets (+10% default)
   - End-of-day position closing

### Risk Management

**Daily Limits:**
- Maximum daily loss: 20% of starting balance
- Maximum daily trades: 10
- Pause after 3 consecutive losses
- Resume after 1-hour cooldown

**Position Sizing:**
- Never risk more than 10% on a single trade
- Keep 20% cash reserve
- Maximum 3 concurrent positions
- Scale positions based on account size

**Safety Features:**
- If balance < $50: Reduce position sizes by 50%
- If balance < $25: Switch to paper trading mode
- If balance > $200: Increase position sizes by 25%
- Emergency stop if balance reaches $0

## 📊 Supported Brokerages

SnapTrade supports 20+ major brokerages:

**US Brokerages:**
- Alpaca
- TD Ameritrade
- E*TRADE
- Robinhood
- Charles Schwab
- Fidelity
- Interactive Brokers
- Webull

**Canadian Brokerages:**
- Questrade
- Wealthica
- National Bank
- Disnat

**And many more...**

## 🔍 Monitoring & Logging

### Real-time Monitoring

The system provides real-time updates on:
- Current balance and positions
- Agent decisions and reasoning
- Trade execution status
- Risk metrics and limits

### Logging

All activities are logged to:
- `live_trading.log`: Main system log
- `daily_summary_YYYYMMDD.json`: Daily performance summary
- Terminal output: Real-time status updates

### Performance Tracking

The system tracks:
- Win rate and average gains/losses
- Total trades and P&L
- Maximum drawdown
- Agent agreement rates

## ⚠️ Important Warnings

### For Live Trading

**BEFORE USING REAL MONEY:**

1. **Test Thoroughly**: Use paper trading extensively first
2. **Start Small**: Begin with small amounts you can afford to lose
3. **Understand Risks**: Day trading is extremely risky
4. **Regulatory Compliance**: Ensure you comply with trading regulations
5. **Pattern Day Trading**: US accounts need $25,000 minimum for day trading
6. **Experimental Software**: This is research software - use at your own risk

### Risk Factors

- **Market Risk**: Prices can move against you rapidly
- **Technical Risk**: Software bugs or connection issues
- **Regulatory Risk**: Trading violations or account restrictions
- **Liquidity Risk**: Inability to exit positions quickly
- **Slippage**: Execution prices may differ from expected

## 🔧 Configuration

### Environment Variables

```bash
# SnapTrade API (Required for live trading)
SNAPTRADE_CLIENT_ID="your_client_id"
SNAPTRADE_CONSUMER_KEY="your_consumer_key"

# Trading Mode
ENABLE_LIVE_TRADING="false"  # Set to "true" for live trading

# API Keys (Required for analysis)
OPENAI_API_KEY="your_openai_key"
FINNHUB_API_KEY="your_finnhub_key"

# Optional
GOOGLE_API_KEY="your_google_key"
```

### Trading Parameters

You can modify trading parameters in `live_trading_plan.py`:

```python
self.config = {
    "max_daily_loss_pct": 0.20,        # Stop if 20% daily loss
    "max_position_size_pct": 0.10,     # Max 10% per trade
    "cash_reserve_pct": 0.20,          # Keep 20% cash
    "stop_loss_pct": 0.05,             # 5% stop loss
    "take_profit_pct": 0.10,           # 10% take profit
    "max_daily_trades": 10,            # Max 10 trades per day
    "max_concurrent_positions": 3,     # Max 3 positions
    "consecutive_loss_limit": 3,       # Pause after 3 losses
    "analysis_interval": 900,          # 15 minutes
    "risk_check_interval": 300,        # 5 minutes
}
```

## 🚨 Emergency Procedures

### Stopping the System

**Graceful Stop:**
```bash
# Send SIGINT (Ctrl+C) to the running process
# The system will close all positions before stopping
```

**Emergency Stop:**
```bash
# If system is unresponsive, you can manually close positions
# through your broker's platform or SnapTrade dashboard
```

### Troubleshooting

**Connection Issues:**
1. Check internet connection
2. Verify SnapTrade API credentials
3. Ensure brokerage account is connected
4. Check for any SnapTrade service issues

**Trading Issues:**
1. Verify sufficient account balance
2. Check market hours
3. Ensure positions don't exceed limits
4. Review recent error logs

## 📞 Support

**SnapTrade Support:**
- Documentation: https://docs.snaptrade.com/
- Discord: https://discord.gg/rkYWBxb8Qu

**TradingAgents:**
- GitHub: https://github.com/TauricResearch/TradingAgents
- Issues: Report bugs and feature requests

## 📝 Legal Disclaimer

This software is provided for educational and research purposes only. The authors and contributors are not responsible for any financial losses incurred through the use of this software. 

Trading involves substantial risk of loss and is not suitable for all investors. Past performance is not indicative of future results. Please consult with a qualified financial advisor before making investment decisions.

By using this software with real money, you acknowledge that you understand the risks and are solely responsible for your trading decisions and their consequences.

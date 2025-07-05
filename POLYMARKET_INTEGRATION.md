# Polymarket Integration for TradingAgents

## Overview

The TradingAgents framework has been extended to support prediction markets, specifically integrating with Polymarket. This allows the multi-agent trading system to analyze and trade binary outcome events alongside traditional financial instruments.

## What's New

### 🔮 Prediction Market Support
- **Market Data Integration**: Fetch events, prices, and analytics from Polymarket
- **Specialized Analyst**: Dedicated prediction market analyst agent
- **Risk Management**: Adapted risk controls for binary outcome trading
- **Portfolio Allocation**: Separate allocation strategy for prediction markets

### 📊 New Data Sources
- **Polymarket Events**: Get trending prediction markets by category
- **Market Analytics**: Historical prices, volume, and volatility analysis
- **Trending Markets**: Identify high-volume, high-uncertainty opportunities

## How It Works

### 1. Data Flow Integration

The system now includes three new data utilities:

```python
# Get events by category
from tradingagents.dataflows import get_polymarket_events
events = get_polymarket_events('crypto', limit=10)

# Analyze specific markets
from tradingagents.dataflows import get_polymarket_market_analysis
analysis = get_polymarket_market_analysis('market_001_yes')

# Find trending opportunities
from tradingagents.dataflows import get_trending_prediction_markets
trending = get_trending_prediction_markets(limit=5)
```

### 2. Agent Integration

A new **Prediction Market Analyst** agent has been added to the agent ecosystem:

```python
from tradingagents.agents import create_prediction_market_analyst

# Create the analyst
analyst = create_prediction_market_analyst(llm, toolkit)

# The analyst specializes in:
# - Probability assessment vs. market prices
# - Volume and liquidity analysis
# - Event fundamental analysis
# - Binary outcome risk evaluation
```

### 3. Live Trading Integration

The live trading system now supports prediction markets:

```python
class PersonalTradingAgent:
    def __init__(self):
        self.config = {
            "enable_prediction_markets": True,
            "prediction_market_allocation": 0.30,  # 30% of portfolio
            "prediction_market_max_position": 0.05,  # 5% per position
        }
    
    async def get_market_opportunities(self):
        # Returns both stocks and prediction markets
        # Prediction markets prefixed with "PM:"
        return ["AAPL", "TSLA", "PM:market_001_yes"]
```

## Key Features

### 🎯 Prediction Market Analysis
- **Probability Assessment**: Compare market prices to estimated true probabilities
- **Volume Analysis**: Identify liquid markets suitable for trading
- **Event Evaluation**: Analyze underlying events and their likelihood
- **Market Inefficiencies**: Spot mispriced markets due to sentiment or bias

### ⚠️ Risk Management
- **Binary Outcome Risk**: 100% loss if wrong (vs. partial losses in traditional markets)
- **Time Decay**: Value approaches 0 or 1 as resolution date approaches
- **Liquidity Risk**: May be difficult to exit positions in smaller markets
- **Resolution Risk**: Depends on oracle/resolution mechanism accuracy

### 💰 Portfolio Allocation
- **Separate Allocation**: Prediction markets get their own allocation (default 30%)
- **Position Sizing**: Smaller positions due to binary risk (default max 5%)
- **Diversification**: Spread across multiple uncorrelated events

## Usage Examples

### Basic Market Analysis

```python
# Test the integration
python test_polymarket_integration.py
```

### Demo Trading Workflow

```python
# See how prediction markets integrate with traditional trading
python demo_polymarket_trading.py
```

### Live Trading with Prediction Markets

```python
# Enable prediction markets in live trading
from live_trading_plan import PersonalTradingAgent

agent = PersonalTradingAgent()
agent.config["enable_prediction_markets"] = True
agent.config["prediction_market_allocation"] = 0.20  # 20% of portfolio

# The agent will now analyze both stocks and prediction markets
```

## Configuration Options

### Prediction Market Settings

```python
config = {
    "enable_prediction_markets": True,           # Enable/disable prediction market trading
    "prediction_market_allocation": 0.30,       # Max % of portfolio for prediction markets
    "prediction_market_max_position": 0.05,     # Max % per individual position
    "prediction_market_categories": ["crypto", "economics", "politics"],  # Categories to analyze
    "prediction_market_min_volume": 50000,      # Minimum volume for consideration
    "prediction_market_max_time_to_resolution": 90,  # Max days to resolution
}
```

## Market Categories Supported

- **Crypto**: Bitcoin price predictions, protocol upgrades, adoption metrics
- **Economics**: Fed rate decisions, GDP growth, inflation outcomes
- **Politics**: Election results, policy outcomes, regulatory decisions
- **Sports**: Game outcomes, season results, performance metrics
- **Technology**: Product launches, company milestones, adoption rates

## Trading Strategies

### 1. Value-Based Trading
- Identify markets where price ≠ true probability
- Look for information asymmetries
- Focus on your areas of expertise

### 2. Volume-Based Trading
- Trade high-volume markets for better liquidity
- Avoid thin markets with wide spreads
- Monitor volume trends for market sentiment

### 3. Time-Based Trading
- Consider time decay as resolution approaches
- Early positions for long-term events
- Last-minute trading on breaking news

## Risk Considerations

### Unique Risks of Prediction Markets
1. **Binary Outcomes**: Either 0% or 100% return
2. **Time Decay**: Value erosion as resolution approaches
3. **Liquidity**: May be difficult to exit positions
4. **Resolution**: Depends on oracle accuracy
5. **Regulatory**: Legal status varies by jurisdiction

### Risk Mitigation
- **Position Sizing**: Keep positions small (1-5% of portfolio)
- **Diversification**: Multiple uncorrelated events
- **Time Management**: Avoid positions close to resolution
- **Liquidity Checks**: Ensure adequate market depth

## Future Enhancements

### Planned Features
- **Real API Integration**: Connect to actual Polymarket API
- **Advanced Analytics**: Machine learning probability estimation
- **Cross-Market Arbitrage**: Between prediction markets and traditional markets
- **Social Sentiment**: Integrate social media sentiment analysis
- **Event Calendars**: Automated tracking of resolution dates

### Integration Opportunities
- **News Analysis**: Use news sentiment to predict market movements
- **Traditional Market Correlation**: Identify relationships with stocks/crypto
- **Options Markets**: Compare prediction market implied probabilities with options

## Getting Started

1. **Install Dependencies**
   ```bash
   pip install beautifulsoup4 tenacity yfinance pandas stockstats tqdm openai
   ```

2. **Test the Integration**
   ```bash
   python test_polymarket_integration.py
   ```

3. **Run the Demo**
   ```bash
   python demo_polymarket_trading.py
   ```

4. **Enable in Live Trading**
   ```python
   agent.config["enable_prediction_markets"] = True
   ```

## Support

For questions or issues with the Polymarket integration:
- Check the test scripts for examples
- Review the demo for workflow understanding
- Examine the source code in `tradingagents/dataflows/polymarket_utils.py`

---

**Disclaimer**: This implementation uses mock data for demonstration. For production use, integrate with the actual Polymarket API and implement proper risk management controls. Prediction market trading involves significant risk and may not be legal in all jurisdictions.
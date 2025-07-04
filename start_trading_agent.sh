#!/bin/bash

# Personal Trading Agent Launcher
# For personal research purposes only

set -e

echo "🤖 Personal Trading Agent Launcher"
echo "=================================="
echo "⚠️  FOR PERSONAL RESEARCH USE ONLY"
echo ""

# Check current directory
if [ ! -f "live_trading_plan.py" ]; then
    echo "❌ Please run this script from the TradingAgents directory"
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d ".venv" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
    PYTHON_CMD=".venv/bin/python"
else
    echo "⚠️  No virtual environment found, using system Python"
    PYTHON_CMD="python"
fi

# Check if it's a weekday and market might be open
DAY_OF_WEEK=$(date +%u)
HOUR=$(date +%H)

if [ $DAY_OF_WEEK -gt 5 ]; then
    echo "❌ Markets are closed (weekend)"
    echo "💡 Next trading session: Monday 9:30 AM ET"
    echo ""
    echo "Would you like to run in simulation mode? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
    echo "🎮 Running in simulation mode..."
fi

# Check for required API keys
echo "🔧 Checking API keys..."
API_KEYS_OK=true

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set"
    API_KEYS_OK=false
fi

if [ -z "$FINNHUB_API_KEY" ]; then
    echo "❌ FINNHUB_API_KEY not set"
    API_KEYS_OK=false
fi

if [ "$API_KEYS_OK" = false ]; then
    echo ""
    echo "Please set your API keys:"
    echo "export OPENAI_API_KEY='your_openai_key'"
    echo "export FINNHUB_API_KEY='your_finnhub_key'"
    echo ""
    echo "You can also create a .env file with these keys."
    exit 1
fi

echo "✅ API keys configured"

# Check Python dependencies
echo "🔧 Checking dependencies..."
$PYTHON_CMD -c "
import sys
try:
    import typer, rich, langchain, langgraph
    print('✅ Core dependencies available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Run: pip install -r requirements.txt')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Create results directory
RESULTS_DIR="results/live_trading/$(date +%Y-%m-%d)"
mkdir -p "$RESULTS_DIR"
echo "📁 Results will be saved to: $RESULTS_DIR"

# Display trading configuration
echo ""
echo "🎯 Trading Configuration:"
echo "  💰 Initial Balance: $100"
echo "  🛑 Stop Loss: 5%"
echo "  🎯 Take Profit: 10%"
echo "  📊 Max Position Size: 10% of balance"
echo "  ⏰ Trading Hours: 9:30 AM - 4:00 PM ET"
echo "  🔄 Analysis Frequency: Every 15 minutes"
echo ""

# Final confirmation
echo "🚨 RISK WARNING:"
echo "This system will make autonomous trading decisions."
echo "You understand this is for research purposes only."
echo ""
echo "Press ENTER to start the trading agent or Ctrl+C to cancel..."
read -r

# Start the trading agent
echo "🚀 Starting Personal Trading Agent..."
echo "📊 Monitor logs in real-time: tail -f live_trading.log"
echo "🛑 Stop with Ctrl+C"
echo ""

# Create a screen session or run directly
if command -v screen >/dev/null 2>&1; then
    echo "🖥️  Starting in screen session 'trading-agent'"
    echo "💡 Reconnect with: screen -r trading-agent"
    screen -dmS trading-agent $PYTHON_CMD live_trading_plan.py
    echo "✅ Trading agent started in background"
    echo "📋 To monitor: screen -r trading-agent"
    echo "📈 To check logs: tail -f live_trading.log"
else
    # Run directly
    $PYTHON_CMD live_trading_plan.py
fi

echo ""
echo "Happy trading! 🚀"

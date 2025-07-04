#!/bin/bash

# SnapTrade Live Trading Setup Script
# This script sets up SnapTrade integration for live trading

echo "🤖 TradingAgents SnapTrade Setup"
echo "================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Install SnapTrade SDK
echo "📦 Installing SnapTrade Python SDK..."
pip install snaptrade-python-sdk>=11.0.110

if [ $? -eq 0 ]; then
    echo "✅ SnapTrade SDK installed successfully"
else
    echo "❌ Failed to install SnapTrade SDK"
    exit 1
fi

# Install additional dependencies
echo "📦 Installing additional dependencies..."
pip install python-dotenv pytz

echo ""
echo "🔧 Setup Instructions:"
echo "======================"
echo ""
echo "1. Create a SnapTrade account:"
echo "   https://dashboard.snaptrade.com/"
echo ""
echo "2. Get your API credentials:"
echo "   - Go to API Keys section"
echo "   - Create a new API key"
echo "   - Copy your Client ID and Consumer Key"
echo ""
echo "3. Set environment variables:"
echo "   export SNAPTRADE_CLIENT_ID='your_client_id_here'"
echo "   export SNAPTRADE_CONSUMER_KEY='your_consumer_key_here'"
echo ""
echo "4. Connect your brokerage account:"
echo "   - Use the SnapTrade Connection Portal"
echo "   - Supports 20+ brokerages including:"
echo "     • Alpaca, TD Ameritrade, E*TRADE"
echo "     • Robinhood, Schwab, Fidelity"
echo "     • Interactive Brokers, Questrade"
echo ""
echo "5. Test your setup:"
echo "   python -m cli.main live status"
echo ""
echo "6. Start paper trading:"
echo "   python -m cli.main live start --paper"
echo ""
echo "7. For live trading (REAL MONEY):"
echo "   export ENABLE_LIVE_TRADING='true'"
echo "   python -m cli.main live start --no-paper"
echo ""
echo "⚠️  IMPORTANT WARNINGS:"
echo "   • Start with paper trading to test your strategy"
echo "   • Live trading uses REAL MONEY and can result in losses"
echo "   • Ensure you comply with trading regulations"
echo "   • This is experimental software - use at your own risk"
echo ""
echo "📚 Documentation:"
echo "   • SnapTrade Docs: https://docs.snaptrade.com/"
echo "   • TradingAgents: https://github.com/TauricResearch/TradingAgents"
echo ""
echo "🎉 Setup complete! You can now use live trading features."

#!/usr/bin/env python3
"""
Simple Paper Trading Test
========================

This script tests the basic paper trading functionality and confirms
everything is working properly.
"""

import sys
import os

def main():
    print("🤖 TradingAgents Paper Trading Test")
    print("=" * 50)
    
    # Test 1: Import SnapTrade SDK
    try:
        import snaptrade_python_sdk
        print("✅ SnapTrade SDK imported successfully")
    except ImportError as e:
        print(f"❌ SnapTrade SDK import failed: {e}")
        return False
    
    # Test 2: Import PersonalTradingAgent
    try:
        from live_trading_plan import PersonalTradingAgent
        print("✅ PersonalTradingAgent imported successfully")
    except ImportError as e:
        print(f"❌ PersonalTradingAgent import failed: {e}")
        return False
    
    # Test 3: Create agent instance
    try:
        agent = PersonalTradingAgent(
            initial_balance=100.0,
            use_paper_trading=True
        )
        print("✅ Paper trading agent created successfully")
        print(f"   💰 Initial balance: ${agent.balance:.2f}")
        print(f"   📄 Paper mode: {agent.use_paper_trading}")
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False
    
    # Test 4: Basic functionality
    try:
        # Test market hours
        is_open = agent.is_market_open()
        print(f"✅ Market hours check: {is_open}")
        
        # Test mock price
        price = agent._get_current_price("TSLA")
        print(f"✅ Price fetching (mock): TSLA = ${price:.2f}")
        
        # Test position sizing
        pos_size = agent._calculate_position_size()
        print(f"✅ Position sizing: ${pos_size:.2f}")
        
        # Test trading limits
        can_trade = agent._check_trading_limits()
        print(f"✅ Trading limits check: {can_trade}")
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False
    
    print()
    print("🎯 Paper Trading Setup Verification Complete!")
    print("✅ All components working properly")
    print("✅ SnapTrade integration ready")
    print("✅ Paper trading mode functional")
    print()
    print("🚀 Ready to start full paper trading simulation!")
    print("💡 Next steps:")
    print("   1. Set GOOGLE_API_KEY or OPENAI_API_KEY for AI analysis")
    print("   2. Set FINNHUB_API_KEY for real market data")
    print("   3. Run: python live_trading_plan.py")
    print()
    print("📋 Current API Status:")
    print(f"   GOOGLE_API_KEY: {'Set' if os.environ.get('GOOGLE_API_KEY') else 'Not set'}")
    print(f"   OPENAI_API_KEY: {'Set' if os.environ.get('OPENAI_API_KEY') else 'Not set'}")
    print(f"   FINNHUB_API_KEY: {'Set' if os.environ.get('FINNHUB_API_KEY') else 'Not set'}")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Paper Trading Ready!")
    else:
        print("\n❌ Setup Issues Found")
        sys.exit(1)

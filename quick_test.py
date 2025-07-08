#!/usr/bin/env python3
"""Simple API Test"""

import os
import sys

print("🔍 Quick API Status Check")
print("=" * 40)

# Check API keys
openrouter_key = os.environ.get('OPENROUTER_API_KEY')
openai_key = os.environ.get('OPENAI_API_KEY') 
finnhub_key = os.environ.get('FINNHUB_API_KEY')

print(f"OPENROUTER_API_KEY: {'✅ Set' if openrouter_key else '❌ Not set'}")
print(f"OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Not set'}")
print(f"FINNHUB_API_KEY: {'✅ Set' if finnhub_key else '❌ Not set'}")

# Test simple import
try:
    from live_trading_plan import PersonalTradingAgent
    print("✅ PersonalTradingAgent import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")

print("\n🚀 Ready to test full integration!")

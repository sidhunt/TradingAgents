#!/usr/bin/env python3
"""
Validation script to check if TradingAgents setup is working correctly.
"""

import sys
import os

def check_imports():
    """Check if required modules can be imported."""
    required_modules = [
        'typer', 'rich', 'pandas', 'langchain', 'langgraph', 
        'questionary', 'yfinance', 'feedparser', 'finnhub'
    ]
    
    success = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module}: {e}")
            success = False
    
    return success

def check_tradingagents():
    """Check if TradingAgents can be imported."""
    try:
        import tradingagents
        print("✅ tradingagents package imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import tradingagents: {e}")
        return False

def check_cli():
    """Check if CLI is accessible."""
    try:
        import cli.main
        print("✅ CLI module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import CLI: {e}")
        return False

def check_env_vars():
    """Check environment variables."""
    print("\n🔧 Environment Variables:")
    api_keys = ['FINNHUB_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY']
    
    for key in api_keys:
        value = os.getenv(key)
        if value:
            print(f"✅ {key} is set")
        else:
            print(f"⚠️  {key} is not set (you'll need to set this to use the full functionality)")

def check_directories():
    """Check if required directories exist."""
    print("\n📁 Directory Structure:")
    dirs_to_check = ['results', 'tradingagents', 'cli']
    
    for dir_name in dirs_to_check:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"⚠️  {dir_name}/ directory missing")

def main():
    """Main validation function."""
    print("🔍 Validating TradingAgents setup...\n")
    
    success = True
    
    # Check imports
    print("📦 Checking package imports:")
    if not check_imports():
        success = False
    
    print("\n📦 Checking TradingAgents package:")
    if not check_tradingagents():
        success = False
    
    print("\n📦 Checking CLI:")
    if not check_cli():
        success = False
    
    # Check environment variables
    check_env_vars()
    
    # Check directories
    check_directories()
    
    # Final status
    print("\n" + "="*50)
    if success:
        print("🎉 Setup validation completed successfully!")
        print("💡 To get started:")
        print("   1. Set your API keys (FINNHUB_API_KEY, OPENAI_API_KEY)")
        print("   2. Run: python -m cli.main analyze")
        print("   3. Or import tradingagents in your Python code")
    else:
        print("❌ Setup validation failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
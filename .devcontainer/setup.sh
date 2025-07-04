#!/bin/bash

# TradingAgents Development Environment Setup Script
echo "🚀 Setting up TradingAgents development environment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update -y

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    nano \
    htop \
    tree

# Upgrade pip and install pip-tools
echo "🐍 Upgrading pip and installing tools..."
python -m pip install --upgrade pip
python -m pip install pip-tools wheel setuptools

# Install Python dependencies
echo "📚 Installing Python dependencies..."
python -m pip install -r requirements.txt

# Install the package in development mode
echo "🔨 Installing TradingAgents in development mode..."
python -m pip install -e .

# Create results directory
echo "📁 Creating results directory..."
mkdir -p results

# Create a simple validation script
cat > validate_setup.py << 'EOF'
#!/usr/bin/env python3
"""
Validation script to check if TradingAgents setup is working correctly.
"""

import sys
import os

def check_imports():
    """Check if required modules can be imported."""
    try:
        import typer
        print("✅ typer imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import typer: {e}")
        return False
    
    try:
        import rich
        print("✅ rich imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import rich: {e}")
        return False
    
    try:
        import pandas
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pandas: {e}")
        return False
    
    try:
        import langchain
        print("✅ langchain imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain: {e}")
        return False
    
    try:
        import langgraph
        print("✅ langgraph imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langgraph: {e}")
        return False
    
    return True

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
EOF

chmod +x validate_setup.py

echo "✨ Setup complete! Run 'python validate_setup.py' to validate the installation."
echo "🔑 Remember to set your API keys:"
echo "   - FINNHUB_API_KEY"
echo "   - OPENAI_API_KEY"
echo "   - GOOGLE_API_KEY (optional)"
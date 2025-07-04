#!/usr/bin/env python3
"""
Demo script to show TradingAgents CLI usage.
This script demonstrates how to use the command-line interface.
"""

import os
import subprocess
import sys

def check_dependencies():
    """Check if CLI dependencies are available."""
    try:
        import typer
        import rich
        return True
    except ImportError:
        return False

def run_cli_help():
    """Run the CLI help command."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "cli.main", "--help"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print("✅ CLI help command successful:")
            print(result.stdout)
            return True
        else:
            print("❌ CLI help command failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running CLI: {e}")
        return False

def main():
    """Main demo function."""
    print("🎬 TradingAgents CLI Demo\n")
    
    # Check dependencies
    if not check_dependencies():
        print("❌ CLI dependencies not available. Please install:")
        print("  pip install -r requirements.txt")
        return False
    
    # Check API keys
    api_keys = ['OPENAI_API_KEY', 'FINNHUB_API_KEY']
    missing_keys = [key for key in api_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"⚠️  Missing API keys: {', '.join(missing_keys)}")
        print("Set them with:")
        for key in missing_keys:
            print(f"  export {key}='your_key_here'")
        print()
    
    # Run CLI help
    print("🔧 Running CLI help command...")
    if run_cli_help():
        print("\n💡 To run analysis:")
        print("  python -m cli.main analyze")
        print("\n📝 Note: Make sure to set your API keys before running analysis")
        return True
    else:
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
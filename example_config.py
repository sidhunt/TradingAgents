#!/usr/bin/env python3
"""
Example configuration and usage script for TradingAgents.
This demonstrates how to use the framework with custom configurations.
"""

import os
from tradingagents.default_config import DEFAULT_CONFIG

def create_example_config():
    """Create an example configuration for TradingAgents."""
    config = DEFAULT_CONFIG.copy()
    
    # Customize the configuration
    config["online_tools"] = True  # Use online tools for real-time data
    config["max_debate_rounds"] = 2  # Increase debate rounds for more thorough analysis
    config["deep_think_llm"] = "gpt-4o-mini"  # Use cost-effective model for testing
    config["quick_think_llm"] = "gpt-4o-mini"  # Use cost-effective model for testing
    
    return config

def check_api_keys():
    """Check if required API keys are set."""
    required_keys = ['OPENAI_API_KEY', 'FINNHUB_API_KEY']
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"⚠️  Missing API keys: {', '.join(missing_keys)}")
        print("Set them with:")
        for key in missing_keys:
            print(f"  export {key}='your_key_here'")
        return False
    else:
        print("✅ All required API keys are set")
        return True

def main():
    """Main example function."""
    print("🔧 TradingAgents Example Configuration\n")
    
    # Check API keys
    if not check_api_keys():
        print("\n⚠️  Please set your API keys before running the analysis.")
        return False
    
    # Create example configuration
    config = create_example_config()
    print("✅ Example configuration created:")
    print(f"  - Online tools: {config['online_tools']}")
    print(f"  - Max debate rounds: {config['max_debate_rounds']}")
    print(f"  - Deep think LLM: {config['deep_think_llm']}")
    print(f"  - Quick think LLM: {config['quick_think_llm']}")
    
    # Try to import and initialize TradingAgents
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        
        print("\n🚀 Initializing TradingAgents...")
        ta = TradingAgentsGraph(debug=True, config=config)
        print("✅ TradingAgents initialized successfully!")
        
        print("\n💡 Example usage:")
        print("  _, decision = ta.propagate('NVDA', '2024-05-10')")
        print("  print(decision)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import TradingAgents: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error initializing TradingAgents: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
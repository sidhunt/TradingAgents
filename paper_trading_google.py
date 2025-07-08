#!/usr/bin/env python3
"""
Paper Trading Simulation with Google API
=======================================

This script runs a short paper trading simulation using Google's Gemini API
instead of OpenAI to avoid exhausted balance issues.
"""

import asyncio
import os
import signal
from datetime import datetime, time
from live_trading_plan import PersonalTradingAgent
from tradingagents.default_config import DEFAULT_CONFIG

class GooglePaperTradingAgent(PersonalTradingAgent):
    """Paper trading agent configured to use Google API instead of OpenAI."""
    
    def __init__(self, initial_balance: float = 100.0):
        # Override the default config to use Google API
        super().__init__(initial_balance=initial_balance, use_paper_trading=True)
        
        # Update configuration for Google API
        self.ta_config = DEFAULT_CONFIG.copy()
        self.ta_config["online_tools"] = True
        self.ta_config["max_debate_rounds"] = 1  # Quick decisions for testing
        self.ta_config["max_risk_discuss_rounds"] = 1
        self.ta_config["llm_provider"] = "google"
        self.ta_config["quick_think_llm"] = "gemini-1.5-flash"  # Cost-effective
        self.ta_config["deep_think_llm"] = "gemini-1.5-pro"    # High quality
        self.ta_config["backend_url"] = None
        
        # Re-initialize TradingAgents with Google configuration
        try:
            from tradingagents.graph.trading_graph import TradingAgentsGraph
            self.ta = TradingAgentsGraph(
                selected_analysts=["market", "news"],  # Reduced for testing
                debug=False,
                config=self.ta_config
            )
            print("✅ Trading agent configured for Google API")
        except Exception as e:
            print(f"⚠️  Could not initialize Google API agent: {e}")
            print("   Will run in basic simulation mode")
            self.ta = None

async def run_paper_trading_simulation():
    """Run a short paper trading simulation."""
    
    print("🤖 Google API Paper Trading Simulation")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check API key availability
    google_key = os.environ.get('GOOGLE_API_KEY')
    finnhub_key = os.environ.get('FINNHUB_API_KEY')
    
    if not google_key:
        print("⚠️  GOOGLE_API_KEY not set - AI analysis will be limited")
    if not finnhub_key:
        print("⚠️  FINNHUB_API_KEY not set - using mock market data")
    
    print()
    
    # Initialize the agent
    agent = GooglePaperTradingAgent(initial_balance=100.0)
    
    print(f"💰 Initial balance: ${agent.balance:.2f}")
    print(f"📄 Paper trading mode: {agent.use_paper_trading}")
    print(f"🤖 LLM Provider: {agent.ta_config['llm_provider']}")
    print(f"🧠 Quick model: {agent.ta_config['quick_think_llm']}")
    print(f"🎯 Deep model: {agent.ta_config['deep_think_llm']}")
    print(f"📊 Market open: {agent.is_market_open()}")
    print()
    
    # Run simulation loop for a short time
    print("🚀 Starting paper trading simulation...")
    print("   (This will run for a few iterations to test functionality)")
    print("   Press Ctrl+C to stop")
    print()
    
    simulation_count = 0
    max_simulations = 3  # Limit for testing
    
    try:
        while simulation_count < max_simulations and agent.balance > 0:
            print(f"--- Simulation Cycle {simulation_count + 1} ---")
            
            # Get market opportunities
            opportunities = await agent.get_market_opportunities()
            print(f"🔍 Market opportunities: {opportunities[:3]}")
            
            # Test position management
            await agent.manage_positions()
            
            # Mock a simple trading decision (since we may not have API keys)
            if len(opportunities) > 0:
                ticker = opportunities[0]
                if not ticker.startswith("PM:"):  # Skip prediction markets
                    price = agent._get_current_price(ticker)
                    print(f"💹 {ticker} current price: ${price:.2f}")
                    
                    # Simulate a trading decision
                    if simulation_count == 0:  # Buy on first cycle
                        print(f"📈 Simulating BUY decision for {ticker}")
                        # Mock execute buy
                        position_size = agent._calculate_position_size()
                        shares = int(position_size / price)
                        if shares >= 1:
                            agent.positions[ticker] = {
                                "shares": shares,
                                "entry_price": price,
                                "entry_time": datetime.now(),
                                "stop_loss": price * 0.95,
                                "take_profit": price * 1.10,
                                "actual_cost": shares * price
                            }
                            agent.balance -= shares * price
                            print(f"   ✅ Bought {shares} shares at ${price:.2f}")
                    
                    elif len(agent.positions) > 0 and ticker in agent.positions:
                        print(f"📉 Simulating SELL decision for {ticker}")
                        # Mock execute sell
                        position = agent.positions[ticker]
                        proceeds = position["shares"] * price
                        pnl = proceeds - position["actual_cost"]
                        agent.balance += proceeds
                        del agent.positions[ticker]
                        print(f"   ✅ Sold {position['shares']} shares at ${price:.2f}")
                        print(f"   💰 P&L: ${pnl:.2f}")
            
            # Show current status
            print(f"💰 Current balance: ${agent.balance:.2f}")
            print(f"📊 Open positions: {len(agent.positions)}")
            if agent.positions:
                for ticker, pos in agent.positions.items():
                    current_price = agent._get_current_price(ticker)
                    unrealized = (current_price - pos["entry_price"]) * pos["shares"]
                    print(f"   {ticker}: {pos['shares']} shares, P&L: ${unrealized:.2f}")
            
            print()
            
            simulation_count += 1
            
            # Wait a bit between cycles
            await asyncio.sleep(2)
        
        print("🎯 Simulation Complete!")
        print(f"💰 Final balance: ${agent.balance:.2f}")
        print(f"📈 Total change: ${agent.balance - 100:.2f}")
        
        # Close any remaining positions
        for ticker in list(agent.positions.keys()):
            await agent._execute_sell(ticker, {"decision": "END_SIMULATION"})
        
        print(f"💰 Final balance after closing positions: ${agent.balance:.2f}")
        
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user")
        
        # Close any remaining positions
        for ticker in list(agent.positions.keys()):
            await agent._execute_sell(ticker, {"decision": "USER_STOP"})
        
        print(f"💰 Final balance: ${agent.balance:.2f}")

if __name__ == "__main__":
    print("🔍 Prerequisites check:")
    print("   GOOGLE_API_KEY:", "✅ Set" if os.environ.get('GOOGLE_API_KEY') else "❌ Not set")
    print("   FINNHUB_API_KEY:", "✅ Set" if os.environ.get('FINNHUB_API_KEY') else "❌ Not set")
    print()
    
    if not os.environ.get('GOOGLE_API_KEY') and not os.environ.get('FINNHUB_API_KEY'):
        print("⚠️  No API keys detected - running in basic simulation mode")
        print("   Set GOOGLE_API_KEY and FINNHUB_API_KEY for full functionality")
    
    print()
    asyncio.run(run_paper_trading_simulation())

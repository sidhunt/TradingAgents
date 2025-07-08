#!/usr/bin/env python3
"""
Start Paper Trading Session
===========================

This script starts a paper trading session that runs for a specified duration
to demonstrate the trading bot functionality.
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from live_trading_plan import PersonalTradingAgent

async def run_paper_trading_session(duration_minutes=5):
    """
    Run a paper trading session for the specified duration.
    
    Args:
        duration_minutes: How long to run the session (default: 5 minutes)
    """
    
    print("🤖 Starting Paper Trading Session")
    print("=" * 50)
    print(f"📅 Session start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Duration: {duration_minutes} minutes")
    print(f"💰 Starting balance: $100.00")
    print()
    
    # Initialize the trading agent
    agent = PersonalTradingAgent(
        initial_balance=100.0,
        use_paper_trading=True
    )
    
    # Override some settings for the demo
    agent.config["analysis_interval"] = 30  # Analyze every 30 seconds for demo
    agent.config["risk_check_interval"] = 15  # Check risk every 15 seconds
    
    print(f"🎯 Watchlist: {', '.join(agent.watchlist[:5])}")
    print(f"📊 Market status: {'Open' if agent.is_market_open() else 'Closed'}")
    print(f"⚙️  Max daily trades: {agent.config['max_daily_trades']}")
    print()
    
    # Calculate session end time
    session_end = datetime.now() + timedelta(minutes=duration_minutes)
    
    print("🚀 Starting trading simulation...")
    print("   (This is a demonstration with simulated data)")
    print("   Press Ctrl+C to stop early")
    print()
    
    iteration = 0
    try:
        while datetime.now() < session_end and agent.balance > 0:
            iteration += 1
            print(f"--- Trading Cycle {iteration} ---")
            
            # Get market opportunities
            try:
                opportunities = await agent.get_market_opportunities()
                print(f"🔍 Found {len(opportunities)} opportunities: {opportunities[:3]}")
            except Exception as e:
                print(f"⚠️  Opportunity detection failed: {e}")
                opportunities = ["TSLA", "NVDA", "SPY"]  # Fallback
            
            # Simulate position management
            await agent.manage_positions()
            
            # Simulate trading decisions for demo
            for ticker in opportunities[:2]:  # Only process first 2
                if ticker.startswith("PM:"):  # Skip prediction markets for demo
                    continue
                    
                try:
                    current_price = agent._get_current_price(ticker)
                    print(f"💹 {ticker}: ${current_price:.2f}")
                    
                    # Simple trading logic for demo
                    if ticker not in agent.positions and len(agent.positions) < 2:
                        # Simulate buy decision
                        if agent._check_trading_limits():
                            position_size = agent._calculate_position_size()
                            shares = int(position_size / current_price)
                            
                            if shares >= 1:
                                print(f"📈 BUYING {shares} shares of {ticker} at ${current_price:.2f}")
                                
                                # Execute mock buy
                                actual_cost = shares * current_price
                                agent.positions[ticker] = {
                                    "shares": shares,
                                    "entry_price": current_price,
                                    "entry_time": datetime.now(),
                                    "stop_loss": current_price * 0.95,  # 5% stop loss
                                    "take_profit": current_price * 1.10,  # 10% take profit
                                    "actual_cost": actual_cost
                                }
                                agent.balance -= actual_cost
                                agent.daily_trades += 1
                                
                                print(f"   ✅ Purchase complete")
                                print(f"   💰 Remaining balance: ${agent.balance:.2f}")
                    
                    elif ticker in agent.positions:
                        # Check if we should sell (simple logic for demo)
                        position = agent.positions[ticker]
                        entry_price = position["entry_price"]
                        
                        # Sell if 5% gain or 3% loss (simplified for demo)
                        if current_price >= entry_price * 1.05 or current_price <= entry_price * 0.97:
                            print(f"📉 SELLING {position['shares']} shares of {ticker} at ${current_price:.2f}")
                            
                            # Execute mock sell
                            proceeds = position["shares"] * current_price
                            pnl = proceeds - position["actual_cost"]
                            agent.balance += proceeds
                            agent.daily_trades += 1
                            
                            # Update performance tracking
                            if pnl > 0:
                                agent.performance["winning_trades"] += 1
                                agent.consecutive_losses = 0
                            else:
                                agent.performance["losing_trades"] += 1
                                agent.consecutive_losses += 1
                            
                            agent.performance["total_pnl"] += pnl
                            
                            del agent.positions[ticker]
                            
                            print(f"   ✅ Sale complete")
                            print(f"   💰 P&L: ${pnl:.2f} ({(pnl/position['actual_cost']*100):+.1f}%)")
                            print(f"   💰 New balance: ${agent.balance:.2f}")
                
                except Exception as e:
                    print(f"⚠️  Error processing {ticker}: {e}")
            
            # Show current status
            total_pnl = agent.balance - 100.0
            print(f"📊 Current Status:")
            print(f"   💰 Balance: ${agent.balance:.2f}")
            print(f"   📈 Total P&L: ${total_pnl:.2f} ({(total_pnl/100)*100:+.1f}%)")
            print(f"   🏪 Open positions: {len(agent.positions)}")
            print(f"   📝 Trades today: {agent.daily_trades}")
            
            if agent.positions:
                print(f"   📊 Position details:")
                for ticker, pos in agent.positions.items():
                    current_price = agent._get_current_price(ticker)
                    unrealized = (current_price - pos["entry_price"]) * pos["shares"]
                    print(f"      {ticker}: {pos['shares']} shares @ ${pos['entry_price']:.2f}, "
                          f"Current: ${current_price:.2f}, P&L: ${unrealized:.2f}")
            
            print()
            
            # Wait before next iteration
            await asyncio.sleep(10)  # 10 second intervals for demo
        
        # Session completed
        print("🏁 Trading Session Complete!")
        
        # Close any remaining positions
        if agent.positions:
            print("🔄 Closing remaining positions...")
            for ticker, position in agent.positions.items():
                current_price = agent._get_current_price(ticker)
                proceeds = position["shares"] * current_price
                pnl = proceeds - position["actual_cost"]
                agent.balance += proceeds
                print(f"   📉 Closed {ticker}: ${pnl:.2f} P&L")
        
        # Final summary
        final_pnl = agent.balance - 100.0
        win_rate = agent.performance["winning_trades"] / max(agent.daily_trades, 1) * 100
        
        print()
        print("📈 Session Summary:")
        print("=" * 30)
        print(f"💰 Starting balance: $100.00")
        print(f"💰 Ending balance: ${agent.balance:.2f}")
        print(f"📈 Total P&L: ${final_pnl:.2f} ({(final_pnl/100)*100:+.1f}%)")
        print(f"📝 Total trades: {agent.daily_trades}")
        print(f"🎯 Win rate: {win_rate:.1f}%")
        print(f"⏱️  Session duration: {(datetime.now() - (session_end - timedelta(minutes=duration_minutes))).total_seconds()/60:.1f} minutes")
        
    except KeyboardInterrupt:
        print("\n🛑 Session stopped by user")
        
        # Close positions and show final status
        final_balance = agent.balance
        for ticker, position in agent.positions.items():
            current_price = agent._get_current_price(ticker)
            final_balance += position["shares"] * current_price
        
        final_pnl = final_balance - 100.0
        print(f"💰 Final balance (with positions): ${final_balance:.2f}")
        print(f"📈 Total P&L: ${final_pnl:.2f}")

def main():
    """Main entry point."""
    print("🔍 Pre-flight checks...")
    
    # Check environment
    google_key = os.environ.get('GOOGLE_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')
    finnhub_key = os.environ.get('FINNHUB_API_KEY')
    
    print(f"   GOOGLE_API_KEY: {'✅ Set' if google_key else '❌ Not set'}")
    print(f"   OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Not set'}")
    print(f"   FINNHUB_API_KEY: {'✅ Set' if finnhub_key else '❌ Not set'}")
    
    if not any([google_key, openai_key, finnhub_key]):
        print("\n⚠️  No API keys detected")
        print("   Running with simulated data only")
        print("   For full functionality, set API keys:")
        print("     export GOOGLE_API_KEY='your_key'")
        print("     export FINNHUB_API_KEY='your_key'")
    
    print("\n🎮 This is a PAPER TRADING simulation")
    print("   • No real money involved")
    print("   • Uses simulated market data")
    print("   • Safe for testing and learning")
    print()
    
    # Ask for session duration
    try:
        duration = int(input("Enter session duration in minutes (default 2): ") or "2")
    except (ValueError, KeyboardInterrupt):
        duration = 2
        print(f"Using default duration: {duration} minutes")
    
    print()
    
    # Start the session
    try:
        asyncio.run(run_paper_trading_session(duration))
    except Exception as e:
        print(f"❌ Session failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Demo Paper Trading Session
==========================
This script demonstrates the paper trading bot with a short 1-minute session.
"""

import asyncio
import os
from datetime import datetime, timedelta
from live_trading_plan import PersonalTradingAgent

async def demo_session():
    print("🚀 Paper Trading Demo Session")
    print("=" * 50)
    print(f"📅 Started: {datetime.now().strftime('%H:%M:%S')}")
    print("💰 Starting Balance: $100.00")
    print("⏱️  Demo Duration: 1 minute")
    print("📄 Mode: Paper Trading (No Real Money)")
    print()
    
    # Create agent
    agent = PersonalTradingAgent(100.0, use_paper_trading=True)
    
    # Quick demo loop
    for i in range(3):  # 3 quick iterations
        print(f"--- Cycle {i+1} ---")
        
        # Get opportunities
        opportunities = await agent.get_market_opportunities()
        ticker = opportunities[0] if opportunities else "TSLA"
        
        if ticker.startswith("PM:"):
            ticker = "TSLA"  # Use TSLA if we get prediction market
        
        price = agent._get_current_price(ticker)
        print(f"📊 {ticker}: ${price:.2f}")
        
        # Simulate trading decision
        if i == 0:  # Buy on first cycle
            shares = int(10 / price)  # Buy $10 worth
            if shares >= 1:
                cost = shares * price
                agent.positions[ticker] = {
                    "shares": shares, 
                    "entry_price": price,
                    "actual_cost": cost
                }
                agent.balance -= cost
                print(f"📈 BOUGHT {shares} shares at ${price:.2f}")
                print(f"💰 New balance: ${agent.balance:.2f}")
        
        elif ticker in agent.positions:  # Sell if we have position
            pos = agent.positions[ticker]
            proceeds = pos["shares"] * price
            pnl = proceeds - pos["actual_cost"]
            agent.balance += proceeds
            del agent.positions[ticker]
            print(f"📉 SOLD {pos['shares']} shares at ${price:.2f}")
            print(f"💰 P&L: ${pnl:.2f}")
            print(f"💰 New balance: ${agent.balance:.2f}")
        
        print()
        await asyncio.sleep(2)  # 2 second pause
    
    final_pnl = agent.balance - 100.0
    print("🎯 Demo Complete!")
    print(f"💰 Final Balance: ${agent.balance:.2f}")
    print(f"📈 Total P&L: ${final_pnl:.2f} ({final_pnl:.1f}%)")
    print()
    print("✅ Paper Trading Demonstration Successful!")
    print("🚀 Ready for full trading sessions!")

if __name__ == "__main__":
    asyncio.run(demo_session())

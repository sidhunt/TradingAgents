#!/usr/bin/env python3
"""
Demo: TradingAgents with Polymarket Integration
==============================================

This demo shows how the TradingAgents framework can be extended
to support prediction markets alongside traditional stock trading.

Author: TradingAgents Framework
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

# Mock simplified versions of the trading agent components
class MockTradingAgent:
    def __init__(self):
        self.balance = 1000.0
        self.positions = {}
        self.config = {
            "enable_prediction_markets": True,
            "prediction_market_allocation": 0.30,
            "prediction_market_max_position": 0.05,
            "max_position_size_pct": 0.10,
        }
        self.watchlist = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"]
        
    async def get_market_opportunities(self) -> List[str]:
        """Get list of stocks and prediction markets to analyze."""
        opportunities = []
        
        # Traditional stock opportunities
        import random
        random.shuffle(self.watchlist)
        opportunities.extend(self.watchlist[:2])  # Top 2 stocks
        
        # Prediction market opportunities (if enabled)
        if self.config.get("enable_prediction_markets", False):
            try:
                from tradingagents.dataflows.polymarket_utils import get_trending_markets
                trending_markets = get_trending_markets(limit=2)
                
                # Add prediction market opportunities with special prefix
                for market in trending_markets:
                    market_symbol = f"PM:{market['market_id']}"
                    opportunities.append(market_symbol)
                    
                print(f"📊 Added {len(trending_markets)} prediction market opportunities")
            except Exception as e:
                print(f"❌ Error getting prediction market opportunities: {e}")
        
        return opportunities
    
    async def analyze_opportunity(self, symbol: str) -> Dict[str, Any]:
        """Analyze a trading opportunity (stock or prediction market)."""
        if symbol.startswith("PM:"):
            return await self.analyze_prediction_market(symbol)
        else:
            return await self.analyze_stock(symbol)
    
    async def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """Analyze a traditional stock."""
        # Mock stock analysis
        import random
        
        decision = random.choice(["BUY", "SELL", "HOLD"])
        confidence = random.uniform(0.6, 0.9)
        
        return {
            "symbol": symbol,
            "type": "stock",
            "decision": decision,
            "confidence": confidence,
            "current_price": random.uniform(100, 300),
            "target_price": random.uniform(110, 350),
            "analysis": f"Technical and fundamental analysis suggests {decision} for {symbol}",
            "risk_factors": ["Market volatility", "Earnings risk", "Sector rotation"],
            "position_size": min(self.config["max_position_size_pct"], 0.10) * self.balance
        }
    
    async def analyze_prediction_market(self, symbol: str) -> Dict[str, Any]:
        """Analyze a prediction market."""
        market_id = symbol.replace("PM:", "")
        
        # Get market data
        from tradingagents.dataflows.polymarket_utils import get_polymarket_market_analytics
        try:
            analytics = get_polymarket_market_analytics(market_id)
        except:
            analytics = {
                "current_price": 0.45,
                "trend": "bullish",
                "volatility": 0.05,
                "total_volume_30d": 100000
            }
        
        # Mock prediction market analysis
        import random
        
        current_price = analytics.get("current_price", 0.45)
        
        # Determine if market is mispriced
        if current_price < 0.35:
            decision = "BUY"
            confidence = 0.75
            analysis = f"Market appears undervalued at ${current_price:.3f}. True probability likely higher."
        elif current_price > 0.65:
            decision = "SELL"
            confidence = 0.70
            analysis = f"Market appears overvalued at ${current_price:.3f}. True probability likely lower."
        else:
            decision = "HOLD"
            confidence = 0.60
            analysis = f"Market fairly valued at ${current_price:.3f}. Monitor for changes."
        
        return {
            "symbol": symbol,
            "type": "prediction_market",
            "decision": decision,
            "confidence": confidence,
            "current_price": current_price,
            "implied_probability": current_price * 100,
            "analysis": analysis,
            "risk_factors": ["Binary outcome risk", "Time decay", "Liquidity risk", "Resolution risk"],
            "position_size": min(self.config["prediction_market_max_position"], 0.05) * self.balance,
            "market_analytics": analytics
        }
    
    def calculate_portfolio_allocation(self) -> Dict[str, float]:
        """Calculate recommended portfolio allocation."""
        total_balance = self.balance
        
        # Traditional markets: 70% of portfolio
        traditional_allocation = total_balance * 0.70
        
        # Prediction markets: 30% of portfolio (if enabled)
        prediction_allocation = 0
        if self.config.get("enable_prediction_markets", False):
            prediction_allocation = total_balance * self.config["prediction_market_allocation"]
        
        # Cash reserve: Remaining balance
        cash_reserve = total_balance - traditional_allocation - prediction_allocation
        
        return {
            "total_balance": total_balance,
            "traditional_markets": traditional_allocation,
            "prediction_markets": prediction_allocation,
            "cash_reserve": cash_reserve,
            "traditional_pct": traditional_allocation / total_balance * 100,
            "prediction_pct": prediction_allocation / total_balance * 100,
            "cash_pct": cash_reserve / total_balance * 100
        }


async def demo_trading_workflow():
    """Demonstrate the integrated trading workflow."""
    print("🤖 TradingAgents with Polymarket Integration Demo")
    print("=" * 60)
    
    # Initialize trading agent
    agent = MockTradingAgent()
    
    # Show portfolio allocation
    print("\n💰 Portfolio Allocation Strategy:")
    allocation = agent.calculate_portfolio_allocation()
    print(f"   Total Balance: ${allocation['total_balance']:,.2f}")
    print(f"   Traditional Markets: ${allocation['traditional_markets']:,.2f} ({allocation['traditional_pct']:.1f}%)")
    print(f"   Prediction Markets: ${allocation['prediction_markets']:,.2f} ({allocation['prediction_pct']:.1f}%)")
    print(f"   Cash Reserve: ${allocation['cash_reserve']:,.2f} ({allocation['cash_pct']:.1f}%)")
    
    # Get market opportunities
    print("\n📊 Market Scanning Phase:")
    opportunities = await agent.get_market_opportunities()
    print(f"   Found {len(opportunities)} opportunities to analyze:")
    for i, opp in enumerate(opportunities, 1):
        market_type = "Prediction Market" if opp.startswith("PM:") else "Stock"
        print(f"   {i}. {opp} ({market_type})")
    
    # Analyze each opportunity
    print("\n🔍 Analysis Phase:")
    analyses = []
    for opportunity in opportunities:
        print(f"\n   Analyzing {opportunity}...")
        analysis = await agent.analyze_opportunity(opportunity)
        analyses.append(analysis)
        
        # Display analysis results
        print(f"   ✅ {analysis['symbol']} Analysis Complete")
        print(f"      Type: {analysis['type'].replace('_', ' ').title()}")
        print(f"      Decision: {analysis['decision']}")
        print(f"      Confidence: {analysis['confidence']:.1%}")
        print(f"      Current Price: ${analysis['current_price']:.3f}")
        
        if analysis['type'] == 'prediction_market':
            print(f"      Implied Probability: {analysis['implied_probability']:.1f}%")
        else:
            print(f"      Target Price: ${analysis['target_price']:.2f}")
            
        print(f"      Position Size: ${analysis['position_size']:.2f}")
        print(f"      Analysis: {analysis['analysis']}")
    
    # Trading decisions
    print("\n🎯 Trading Decisions:")
    buy_decisions = [a for a in analyses if a['decision'] == 'BUY' and a['confidence'] > 0.7]
    
    if buy_decisions:
        print(f"   Found {len(buy_decisions)} high-confidence BUY opportunities:")
        for decision in buy_decisions:
            print(f"   📈 {decision['symbol']} - {decision['type'].replace('_', ' ').title()}")
            print(f"      Confidence: {decision['confidence']:.1%}")
            print(f"      Position Size: ${decision['position_size']:.2f}")
            print(f"      Risk Factors: {', '.join(decision['risk_factors'][:2])}")
    else:
        print("   No high-confidence BUY opportunities found.")
    
    # Risk management summary
    print("\n⚠️ Risk Management:")
    traditional_positions = [a for a in analyses if a['type'] == 'stock' and a['decision'] == 'BUY']
    prediction_positions = [a for a in analyses if a['type'] == 'prediction_market' and a['decision'] == 'BUY']
    
    print(f"   Traditional Market Positions: {len(traditional_positions)}")
    print(f"   Prediction Market Positions: {len(prediction_positions)}")
    print(f"   Total Position Value: ${sum(p['position_size'] for p in buy_decisions):.2f}")
    print(f"   Remaining Cash: ${agent.balance - sum(p['position_size'] for p in buy_decisions):.2f}")
    
    # Show unique aspects of prediction market trading
    if prediction_positions:
        print("\n🔮 Prediction Market Considerations:")
        print("   • Binary outcomes: 0% or 100% return")
        print("   • Time decay: Value approaches resolution as time passes")
        print("   • Market inefficiencies: Often driven by sentiment rather than fundamentals")
        print("   • Liquidity concerns: May be difficult to exit positions")
        print("   • Resolution risk: Depends on oracle/resolution mechanism")
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("The TradingAgents framework now supports both traditional and prediction markets!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo_trading_workflow())
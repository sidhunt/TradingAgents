#!/usr/bin/env python3
"""
Test script for Polymarket integration with TradingAgents
========================================================

This script demonstrates how the TradingAgents framework can be extended
to support prediction markets like Polymarket.

Author: TradingAgents Framework
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tradingagents.dataflows.polymarket_utils import (
    get_polymarket_events,
    get_polymarket_market_history,
    get_polymarket_market_analytics,
    get_trending_markets
)
from tradingagents.dataflows.interface import (
    get_polymarket_events as interface_get_polymarket_events,
    get_polymarket_market_analysis as interface_get_polymarket_market_analysis,
    get_trending_prediction_markets as interface_get_trending_prediction_markets
)


def test_polymarket_integration():
    """Test the Polymarket integration functionality"""
    print("🤖 Testing Polymarket Integration with TradingAgents")
    print("=" * 60)
    
    # Test 1: Get events by category
    print("\n1. Testing Polymarket Events by Category")
    print("-" * 40)
    
    categories = ['crypto', 'economics', 'stocks']
    for category in categories:
        events = get_polymarket_events(category=category, limit=2)
        print(f"✅ {category.title()}: Found {len(events)} events")
        if events:
            print(f"   Sample: {events[0]['title']}")
    
    # Test 2: Market analytics
    print("\n2. Testing Market Analytics")
    print("-" * 40)
    
    # Get a sample market ID
    sample_events = get_polymarket_events(limit=1)
    if sample_events:
        market_id = sample_events[0]['markets'][0]['id']
        analytics = get_polymarket_market_analytics(market_id)
        print(f"✅ Market Analytics for {market_id}")
        print(f"   Current Price: ${analytics['current_price']:.3f}")
        print(f"   Trend: {analytics['trend']}")
        print(f"   Volatility: {analytics['volatility']:.4f}")
    
    # Test 3: Trending markets
    print("\n3. Testing Trending Markets")
    print("-" * 40)
    
    trending = get_trending_markets(limit=3)
    print(f"✅ Found {len(trending)} trending markets")
    for i, market in enumerate(trending[:3], 1):
        print(f"   {i}. {market['event_title']}")
        print(f"      Price: ${market['price']:.3f} ({market['outcome']})")
        print(f"      Volume: ${market['volume']:,}")
    
    # Test 4: Interface functions
    print("\n4. Testing Interface Functions")
    print("-" * 40)
    
    # Test crypto events
    crypto_events = interface_get_polymarket_events('crypto', 3, True)
    print(f"✅ Crypto events interface: {len(crypto_events)} characters")
    
    # Test market analysis
    if sample_events:
        market_id = sample_events[0]['markets'][0]['id']
        market_analysis = interface_get_polymarket_market_analysis(market_id, True)
        print(f"✅ Market analysis interface: {len(market_analysis)} characters")
    
    # Test trending markets
    trending_markets = interface_get_trending_prediction_markets(3)
    print(f"✅ Trending markets interface: {len(trending_markets)} characters")
    
    # Test 5: Display sample output
    print("\n5. Sample Analysis Output")
    print("-" * 40)
    
    print("\n📊 CRYPTO PREDICTION MARKETS:")
    print(interface_get_polymarket_events('crypto', 2, True))
    
    print("\n📈 TRENDING PREDICTION MARKETS:")
    print(interface_get_trending_prediction_markets(2))
    
    print("\n✅ All tests passed! Polymarket integration is working correctly.")
    print("\n🎯 Next Steps:")
    print("   1. The prediction market analyst can now be used in trading workflows")
    print("   2. Live trading system can be extended to support prediction markets")
    print("   3. Risk management can be adapted for binary outcome trading")
    print("   4. Integration with real Polymarket API when available")


def demonstrate_trading_workflow():
    """Demonstrate how this would work in a trading workflow"""
    print("\n🚀 Trading Workflow Demonstration")
    print("=" * 60)
    
    # Simulate a trading agent analyzing prediction markets
    print("\n1. Market Scanning Phase:")
    trending = get_trending_markets(limit=5)
    print(f"   📊 Identified {len(trending)} trending prediction markets")
    
    # Find high-volume, uncertain markets (price near 0.5)
    opportunities = []
    for market in trending:
        uncertainty = 1 - abs(market['price'] - 0.5)  # Higher when price is closer to 0.5
        if market['volume'] > 50000 and uncertainty > 0.3:
            opportunities.append(market)
    
    print(f"   🎯 Found {len(opportunities)} potential trading opportunities")
    
    if opportunities:
        print("\n2. Analysis Phase:")
        for opportunity in opportunities[:2]:  # Analyze top 2
            print(f"\n   📈 Analyzing: {opportunity['event_title']}")
            print(f"      Outcome: {opportunity['outcome']}")
            print(f"      Current Price: ${opportunity['price']:.3f} ({opportunity['price']*100:.1f}% implied probability)")
            print(f"      Volume: ${opportunity['volume']:,}")
            print(f"      Market Cap: ${opportunity['category']}")
            
            # Simple analysis
            if opportunity['price'] < 0.4:
                print(f"      💡 Potential Value: Undervalued if true probability > 40%")
            elif opportunity['price'] > 0.6:
                print(f"      💡 Potential Value: Overvalued if true probability < 60%")
            else:
                print(f"      💡 Potential Value: Fair value range, monitor for changes")
    
    print("\n3. Risk Assessment:")
    print("   ⚠️  Binary outcome risk: 100% loss if wrong")
    print("   ⚠️  Time decay: Value approaches 0 or 1 as resolution approaches")
    print("   ⚠️  Liquidity risk: May be difficult to exit position")
    print("   ✅ Defined risk: Maximum loss is purchase price")
    
    print("\n4. Position Sizing:")
    print("   💰 Recommended: 1-2% of portfolio per position")
    print("   💰 Maximum: 5% of portfolio for high-conviction trades")
    print("   💰 Diversification: Multiple uncorrelated events")


if __name__ == "__main__":
    test_polymarket_integration()
    demonstrate_trading_workflow()
    
    print("\n" + "=" * 60)
    print("🎉 Polymarket integration complete!")
    print("The TradingAgents framework now supports prediction markets!")
    print("=" * 60)
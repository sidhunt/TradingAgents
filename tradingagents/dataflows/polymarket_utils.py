"""
Polymarket Data Utility
=====================

This module provides utilities for fetching and processing prediction market data
from Polymarket. It follows the same pattern as other data utilities in the framework.

Author: TradingAgents Framework
"""

import json
import requests
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result,
)


def is_rate_limited(response):
    """Check if the response indicates rate limiting"""
    if response is None:
        return False
    return response.status_code == 429


@retry(
    retry=(retry_if_result(is_rate_limited)),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
)
def make_request(url: str, headers: Dict[str, str]) -> requests.Response:
    """Make a request with retry logic for rate limiting"""
    try:
        response = requests.get(url, headers=headers, timeout=30)
        time.sleep(random.uniform(1, 3))  # Random delay to avoid rate limiting
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def get_polymarket_events(
    category: Optional[str] = None,
    active_only: bool = True,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Fetch prediction market events from Polymarket.
    
    Args:
        category: Filter by category (e.g., 'politics', 'sports', 'crypto')
        active_only: Only return active markets
        limit: Maximum number of events to return
        
    Returns:
        List of event dictionaries
    """
    # Mock implementation since we can't access the actual API
    # In a real implementation, this would call the Polymarket API
    
    mock_events = [
        {
            "id": "event_001",
            "title": "Will Bitcoin reach $100,000 by end of 2024?",
            "category": "crypto",
            "description": "Market resolves YES if Bitcoin (BTC) reaches $100,000 USD at any point before January 1, 2025",
            "end_date": "2024-12-31T23:59:59Z",
            "markets": [
                {
                    "id": "market_001_yes",
                    "outcome": "YES",
                    "price": 0.35,
                    "volume": 125000,
                    "liquidity": 50000
                },
                {
                    "id": "market_001_no", 
                    "outcome": "NO",
                    "price": 0.65,
                    "volume": 125000,
                    "liquidity": 50000
                }
            ],
            "total_volume": 250000,
            "active": True,
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "event_002",
            "title": "Will the Fed cut interest rates in Q1 2024?",
            "category": "economics",
            "description": "Market resolves YES if the Federal Reserve reduces the federal funds rate by at least 0.25% during Q1 2024",
            "end_date": "2024-03-31T23:59:59Z",
            "markets": [
                {
                    "id": "market_002_yes",
                    "outcome": "YES",
                    "price": 0.72,
                    "volume": 89000,
                    "liquidity": 35000
                },
                {
                    "id": "market_002_no",
                    "outcome": "NO", 
                    "price": 0.28,
                    "volume": 89000,
                    "liquidity": 35000
                }
            ],
            "total_volume": 178000,
            "active": True,
            "created_at": "2023-12-01T00:00:00Z"
        },
        {
            "id": "event_003",
            "title": "Will Tesla stock reach $300 by end of 2024?",
            "category": "stocks",
            "description": "Market resolves YES if Tesla (TSLA) stock price reaches $300 per share at any point before January 1, 2025",
            "end_date": "2024-12-31T23:59:59Z",
            "markets": [
                {
                    "id": "market_003_yes",
                    "outcome": "YES",
                    "price": 0.45,
                    "volume": 67000,
                    "liquidity": 28000
                },
                {
                    "id": "market_003_no",
                    "outcome": "NO",
                    "price": 0.55,
                    "volume": 67000,
                    "liquidity": 28000
                }
            ],
            "total_volume": 134000,
            "active": True,
            "created_at": "2024-01-15T00:00:00Z"
        }
    ]
    
    # Filter by category if specified
    if category:
        mock_events = [e for e in mock_events if e["category"].lower() == category.lower()]
    
    # Filter by active status
    if active_only:
        mock_events = [e for e in mock_events if e["active"]]
    
    # Apply limit
    return mock_events[:limit]


def get_polymarket_market_history(
    market_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Fetch historical price data for a specific market.
    
    Args:
        market_id: The market ID to fetch history for
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        List of historical price points
    """
    # Mock implementation
    mock_history = []
    
    # Generate mock price history
    base_date = datetime.now() - timedelta(days=30)
    base_price = 0.50
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        # Random walk for price
        price_change = random.uniform(-0.05, 0.05)
        base_price = max(0.01, min(0.99, base_price + price_change))
        
        mock_history.append({
            "date": date.strftime("%Y-%m-%d"),
            "price": round(base_price, 3),
            "volume": random.randint(1000, 10000),
            "market_id": market_id
        })
    
    return mock_history


def get_polymarket_market_analytics(market_id: str) -> Dict[str, Any]:
    """
    Get analytics for a specific market.
    
    Args:
        market_id: The market ID to analyze
        
    Returns:
        Dictionary containing market analytics
    """
    # Mock implementation
    history = get_polymarket_market_history(market_id)
    
    if not history:
        return {}
    
    prices = [h["price"] for h in history]
    volumes = [h["volume"] for h in history]
    
    return {
        "market_id": market_id,
        "current_price": prices[-1] if prices else 0,
        "price_change_24h": prices[-1] - prices[-2] if len(prices) >= 2 else 0,
        "price_change_7d": prices[-1] - prices[-8] if len(prices) >= 8 else 0,
        "avg_price_30d": sum(prices) / len(prices) if prices else 0,
        "total_volume_30d": sum(volumes) if volumes else 0,
        "avg_volume_30d": sum(volumes) / len(volumes) if volumes else 0,
        "volatility": calculate_volatility(prices) if len(prices) > 1 else 0,
        "trend": determine_trend(prices) if len(prices) > 5 else "neutral"
    }


def calculate_volatility(prices: List[float]) -> float:
    """Calculate price volatility"""
    if len(prices) < 2:
        return 0.0
    
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] != 0:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    
    if not returns:
        return 0.0
    
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    return variance ** 0.5


def determine_trend(prices: List[float]) -> str:
    """Determine price trend"""
    if len(prices) < 6:
        return "neutral"
    
    recent_prices = prices[-5:]
    older_prices = prices[-10:-5] if len(prices) >= 10 else prices[:-5]
    
    if not older_prices:
        return "neutral"
    
    recent_avg = sum(recent_prices) / len(recent_prices)
    older_avg = sum(older_prices) / len(older_prices)
    
    change = (recent_avg - older_avg) / older_avg if older_avg != 0 else 0
    
    if change > 0.05:
        return "bullish"
    elif change < -0.05:
        return "bearish"
    else:
        return "neutral"


def get_trending_markets(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get trending prediction markets based on volume and activity.
    
    Args:
        limit: Maximum number of markets to return
        
    Returns:
        List of trending markets
    """
    events = get_polymarket_events(limit=limit * 2)  # Get more to filter
    
    # Sort by volume and activity metrics
    trending = []
    for event in events:
        for market in event["markets"]:
            market_data = {
                "event_id": event["id"],
                "event_title": event["title"],
                "market_id": market["id"],
                "outcome": market["outcome"],
                "price": market["price"],
                "volume": market["volume"],
                "category": event["category"],
                "end_date": event["end_date"],
                "trend_score": market["volume"] * (1 - abs(market["price"] - 0.5))  # Volume weighted by uncertainty
            }
            trending.append(market_data)
    
    # Sort by trend score and return top markets
    trending.sort(key=lambda x: x["trend_score"], reverse=True)
    return trending[:limit]
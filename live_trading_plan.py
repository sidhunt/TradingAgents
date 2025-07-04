"""
Personal Trading Agent Continuous Operation Plan
================================================

This module implements a continuous trading system using the existing TradingAgents
multi-agent framework for personal research purposes.

Key Features:
- Runs during market hours (9:30 AM - 4:00 PM ET)
- Uses existing analyst, research, and risk management teams
- Implements position sizing and risk controls
- Stops when balance reaches $0
- Logs all decisions for analysis

Author: Personal Research
"""

import asyncio
import signal
import sys
import json
import logging
from datetime import datetime, time
from pathlib import Path
from typing import Dict, List, Optional, Any
import pytz
import os
from decimal import Decimal


# SnapTrade SDK for broker integration
try:
    from snaptrade_python_sdk import SnapTrade
    SNAPTRADE_AVAILABLE = True
except ImportError:
    SNAPTRADE_AVAILABLE = False
    print("⚠️ SnapTrade SDK not installed. Install with: pip install snaptrade-python-sdk")

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('live_trading.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class PersonalTradingAgent:
    """
    Personal Trading Agent for continuous autonomous trading using SnapTrade.
    
    This agent implements the following workflow:
    1. Market Analysis (every 15 minutes)
    2. Research & Debate (every 30 minutes) 
    3. Trading Decisions (continuous)
    4. Risk Management (continuous)
    5. Position Monitoring (continuous)
    
    Integrates with SnapTrade API for real broker execution across 20+ brokerages.
    """
    
    def __init__(self, initial_balance: float = 100.0, use_paper_trading: bool = True):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.positions = {}
        self.daily_trades = 0
        self.consecutive_losses = 0
        self.is_running = True
        self.last_analysis_time = None
        self.use_paper_trading = use_paper_trading
        
        # Initialize SnapTrade client
        self.snaptrade_client = None
        self.user_id = None
        self.user_secret = None
        self.connected_accounts = []
        self.primary_account_id = None
        
        if SNAPTRADE_AVAILABLE and not use_paper_trading:
            self._initialize_snaptrade()
        else:
            logger.info("📄 Running in paper trading mode")
        
        # Trading Configuration
        self.config = {
            "max_daily_loss_pct": 0.20,        # Stop if 20% daily loss
            "max_position_size_pct": 0.10,     # Max 10% per trade
            "cash_reserve_pct": 0.20,          # Keep 20% cash
            "stop_loss_pct": 0.05,             # 5% stop loss
            "take_profit_pct": 0.10,           # 10% take profit
            "max_daily_trades": 10,            # Max 10 trades per day
            "max_concurrent_positions": 3,     # Max 3 positions
            "consecutive_loss_limit": 3,       # Pause after 3 losses
            "analysis_interval": 900,          # 15 minutes
            "enable_prediction_markets": True,  # Enable prediction market trading
            "prediction_market_allocation": 0.30, # Max 30% of portfolio for prediction markets
            "prediction_market_max_position": 0.05, # Max 5% per prediction market position
        }
            "risk_check_interval": 300,        # 5 minutes
        }
        
        # Initialize TradingAgents with optimized settings
        self.ta_config = DEFAULT_CONFIG.copy()
        self.ta_config["online_tools"] = True
        self.ta_config["max_debate_rounds"] = 1  # Quick decisions
        self.ta_config["max_risk_discuss_rounds"] = 1
        self.ta_config["quick_think_llm"] = "gpt-4o-mini"  # Cost-effective
        self.ta_config["deep_think_llm"] = "gpt-4o"
        
        # Initialize with core analysts for efficiency
        self.ta = TradingAgentsGraph(
            selected_analysts=["market", "news", "fundamentals"],
            debug=False,
            config=self.ta_config
        )
        
        # Performance tracking
        self.performance = {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_pnl": 0.0,
            "win_rate": 0.0,
            "avg_gain": 0.0,
            "avg_loss": 0.0,
            "max_drawdown": 0.0,
            "decisions_log": []
        }
        
        # Market data
        self.watchlist = ["TSLA", "NVDA", "SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "AMZN"]
        
    def _initialize_snaptrade(self):
        """Initialize SnapTrade client and user."""
        try:
            # Get API credentials from environment
            client_id = os.getenv('SNAPTRADE_CLIENT_ID')
            consumer_key = os.getenv('SNAPTRADE_CONSUMER_KEY')
            
            if not client_id or not consumer_key:
                logger.error("❌ SnapTrade credentials not found. Set SNAPTRADE_CLIENT_ID and SNAPTRADE_CONSUMER_KEY")
                return
                
            # Initialize SnapTrade client
            self.snaptrade_client = SnapTrade(
                client_id=client_id,
                consumer_key=consumer_key
            )
            
            # Check API status
            status = self.snaptrade_client.api_status.check()
            logger.info(f"✅ SnapTrade API online: {status.data}")
            
            # Set up user (use a consistent user ID for your personal trading)
            self.user_id = "personal_trader_001"  # Your personal user ID
            
            # Get or create user
            try:
                # Try to get existing user
                users = self.snaptrade_client.authentication.list_snap_trade_users()
                existing_user = None
                for user in users.data:
                    if user['userId'] == self.user_id:
                        existing_user = user
                        break
                        
                if existing_user:
                    self.user_secret = existing_user['userSecret']
                    logger.info("✅ Using existing SnapTrade user")
                else:
                    # Create new user
                    user_response = self.snaptrade_client.authentication.register_snap_trade_user(
                        body={"userId": self.user_id}
                    )
                    self.user_secret = user_response.data['userSecret']
                    logger.info("✅ Created new SnapTrade user")
                    
            except Exception as e:
                logger.error(f"❌ Error setting up SnapTrade user: {e}")
                return
                
            # Get connected accounts
            self._refresh_accounts()
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize SnapTrade: {e}")
            self.snaptrade_client = None
            
    def _refresh_accounts(self):
        """Refresh list of connected brokerage accounts."""
        if not self.snaptrade_client or not self.user_secret:
            return
            
        try:
            accounts = self.snaptrade_client.account_information.list_user_accounts(
                user_id=self.user_id,
                user_secret=self.user_secret
            )
            
            self.connected_accounts = accounts.data
            if self.connected_accounts:
                # Use first account as primary
                self.primary_account_id = self.connected_accounts[0]['id']
                logger.info(f"✅ Found {len(self.connected_accounts)} connected accounts")
                logger.info(f"📊 Primary account: {self.connected_accounts[0]['name']}")
            else:
                logger.warning("⚠️ No connected brokerage accounts found")
                logger.info("👉 You need to connect a brokerage account through SnapTrade")
                
        except Exception as e:
            logger.error(f"❌ Error refreshing accounts: {e}")
    
    def _get_account_balance(self) -> float:
        """Get current account balance from broker."""
        if not self.snaptrade_client or not self.primary_account_id:
            return self.balance  # Return simulated balance
            
        try:
            balances = self.snaptrade_client.account_information.get_user_account_balance(
                user_id=self.user_id,
                user_secret=self.user_secret,
                account_id=self.primary_account_id
            )
            
            # Get total cash + market value
            total_value = 0
            for balance in balances.data:
                if balance.get('cash'):
                    total_value += float(balance['cash'])
                if balance.get('marketValue'):
                    total_value += float(balance['marketValue'])
                    
            return total_value
            
        except Exception as e:
            logger.error(f"❌ Error getting account balance: {e}")
            return self.balance
    
    def _get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol."""
        if not self.snaptrade_client:
            # Return mock price for paper trading
            import random
            return round(random.uniform(50, 500), 2)
            
        try:
            # Get symbol ID first
            symbols = self.snaptrade_client.reference_data.get_symbols(
                body={"substring": symbol}
            )
            
            if not symbols.data:
                logger.error(f"❌ Symbol {symbol} not found")
                return None
                
            symbol_id = symbols.data[0]['id']
            
            # Get quote
            quotes = self.snaptrade_client.trading.get_user_account_quotes(
                user_id=self.user_id,
                user_secret=self.user_secret,
                account_id=self.primary_account_id,
                body={"symbols": symbol_id}
            )
            
            if quotes.data and len(quotes.data) > 0:
                return float(quotes.data[0]['last'])
                
        except Exception as e:
            logger.error(f"❌ Error getting price for {symbol}: {e}")
            
        return None
        
    def is_market_open(self) -> bool:
        """Check if US market is currently open."""
        ny_tz = pytz.timezone('America/New_York')
        now = datetime.now(ny_tz)
        
        # Check if weekday
        if now.weekday() > 4:  # Saturday = 5, Sunday = 6
            return False
            
        # Check market hours (9:30 AM - 4:00 PM ET)
        market_open = time(9, 30)
        market_close = time(16, 0)
        
        return market_open <= now.time() <= market_close
    
    def should_analyze(self) -> bool:
        """Check if it's time for new analysis."""
        if not self.last_analysis_time:
            return True
            
        time_since_analysis = datetime.now() - self.last_analysis_time
        return time_since_analysis.total_seconds() >= self.config["analysis_interval"]
    
    async def get_market_opportunities(self) -> List[str]:
        """Get list of stocks and prediction markets to analyze based on market conditions."""
        opportunities = []
        
        # Traditional stock opportunities
        import random
        random.shuffle(self.watchlist)
        opportunities.extend(self.watchlist[:3])  # Analyze top 3 stock opportunities
        
        # Prediction market opportunities (if enabled)
        if self.config.get("enable_prediction_markets", False):
            try:
                from tradingagents.dataflows.polymarket_utils import get_trending_markets
                trending_markets = get_trending_markets(limit=2)
                
                # Add prediction market opportunities with special prefix
                for market in trending_markets:
                    market_symbol = f"PM:{market['market_id']}"
                    opportunities.append(market_symbol)
                    
                logger.info(f"📊 Added {len(trending_markets)} prediction market opportunities")
            except Exception as e:
                logger.error(f"❌ Error getting prediction market opportunities: {e}")
        
        return opportunities
    
    async def analyze_opportunity(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Run comprehensive analysis on a ticker using TradingAgents.
        
        Returns:
            Dictionary with analysis results or None if analysis fails
        """
        try:
            trade_date = datetime.now().strftime("%Y-%m-%d")
            
            logger.info(f"🔍 Analyzing {ticker} for {trade_date}")
            
            # Run the multi-agent analysis
            final_state, decision = self.ta.propagate(ticker, trade_date)
            
            # Extract confidence from agent consensus
            confidence = self._calculate_confidence(final_state)
            
            # Extract key insights
            analysis_summary = self._extract_insights(final_state)
            
            result = {
                "ticker": ticker,
                "decision": decision.upper() if decision else "HOLD",
                "confidence": confidence,
                "analysis_date": trade_date,
                "analysis_time": datetime.now().isoformat(),
                "insights": analysis_summary,
                "raw_state": final_state
            }
            
            # Log the decision
            self.performance["decisions_log"].append(result)
            
            logger.info(f"✅ Analysis complete for {ticker}: {decision} (confidence: {confidence:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error analyzing {ticker}: {e}")
            return None
    
    def _calculate_confidence(self, state: Dict) -> float:
        """Calculate confidence level from agent consensus."""
        try:
            # Extract debate states
            investment_debate = state.get("investment_debate_state", {})
            risk_debate = state.get("risk_debate_state", {})
            
            # Count bull vs bear positions
            bull_history = investment_debate.get("bull_history", "")
            bear_history = investment_debate.get("bear_history", "")
            
            # Simple heuristic: longer response indicates stronger conviction
            bull_strength = len(bull_history.split()) if bull_history else 0
            bear_strength = len(bear_history.split()) if bear_history else 0
            
            if bull_strength + bear_strength == 0:
                return 0.5
                
            confidence = bull_strength / (bull_strength + bear_strength)
            
            # Adjust based on risk analysis consensus
            if risk_debate.get("judge_decision"):
                # If risk team reached consensus, boost confidence
                confidence = min(confidence + 0.1, 1.0)
                
            return confidence
            
        except Exception as e:
            logger.warning(f"Error calculating confidence: {e}")
            return 0.5
    
    def _extract_insights(self, state: Dict) -> Dict[str, str]:
        """Extract key insights from agent analysis."""
        insights = {}
        
        try:
            # Market analysis
            if "market_report" in state:
                insights["market"] = state["market_report"][:200] + "..."
                
            # News analysis
            if "news_report" in state:
                insights["news"] = state["news_report"][:200] + "..."
                
            # Research summary
            investment_debate = state.get("investment_debate_state", {})
            if investment_debate.get("judge_decision"):
                insights["research"] = investment_debate["judge_decision"][:200] + "..."
                
            # Risk assessment
            risk_debate = state.get("risk_debate_state", {})
            if risk_debate.get("judge_decision"):
                insights["risk"] = risk_debate["judge_decision"][:200] + "..."
                
        except Exception as e:
            logger.warning(f"Error extracting insights: {e}")
            
        return insights
    
    async def execute_trade(self, analysis: Dict[str, Any]) -> bool:
        """
        Execute a trade based on analysis results.
        
        Returns:
            True if trade was executed, False otherwise
        """
        if not analysis or analysis["confidence"] < 0.7:
            logger.info(f"❌ Trade skipped for {analysis['ticker']}: Low confidence ({analysis['confidence']:.2f})")
            return False
            
        ticker = analysis["ticker"]
        decision = analysis["decision"]
        
        # Check trading limits
        if not self._check_trading_limits():
            return False
            
        # Calculate position size
        position_size = self._calculate_position_size()
        
        if decision == "BUY" and ticker not in self.positions:
            return await self._execute_buy(ticker, position_size, analysis)
            
        elif decision == "SELL" and ticker in self.positions:
            return await self._execute_sell(ticker, analysis)
            
        return False
    
    def _check_trading_limits(self) -> bool:
        """Check if we can execute more trades today."""
        # Daily trade limit
        if self.daily_trades >= self.config["max_daily_trades"]:
            logger.info("❌ Daily trade limit reached")
            return False
            
        # Consecutive loss limit
        if self.consecutive_losses >= self.config["consecutive_loss_limit"]:
            logger.info("❌ Consecutive loss limit reached - cooling down")
            return False
            
        # Position limit
        if len(self.positions) >= self.config["max_concurrent_positions"]:
            logger.info("❌ Maximum concurrent positions reached")
            return False
            
        # Daily loss limit
        daily_loss_pct = (self.initial_balance - self.balance) / self.initial_balance
        if daily_loss_pct > self.config["max_daily_loss_pct"]:
            logger.info(f"❌ Daily loss limit reached: {daily_loss_pct:.2%}")
            return False
            
        return True
    
    def _calculate_position_size(self) -> float:
        """Calculate appropriate position size."""
        # Available cash after reserve
        available_cash = self.balance * (1 - self.config["cash_reserve_pct"])
        
        # Position size based on risk per trade
        position_size = self.balance * self.config["max_position_size_pct"]
        
        # Use smaller of the two
        return min(position_size, available_cash)
    
    async def _execute_buy(self, ticker: str, position_size: float, analysis: Dict) -> bool:
        """Execute a buy order through SnapTrade or paper trading."""
        try:
            current_price = self._get_current_price(ticker)
            if not current_price:
                logger.error(f"❌ Could not get price for {ticker}")
                return False
                
            shares = int(position_size / current_price)
            if shares < 1:
                logger.info(f"❌ Position size too small for {ticker}: ${position_size:.2f}")
                return False
            
            actual_cost = shares * current_price
            
            # Execute order through SnapTrade or simulate
            order_id = None
            if not self.use_paper_trading and self.snaptrade_client and self.primary_account_id:
                order_id = await self._place_snaptrade_order(ticker, shares, "BUY")
                if not order_id:
                    return False
            
            # Track position
            self.positions[ticker] = {
                "shares": shares,
                "entry_price": current_price,
                "entry_time": datetime.now(),
                "stop_loss": current_price * (1 - self.config["stop_loss_pct"]),
                "take_profit": current_price * (1 + self.config["take_profit_pct"]),
                "analysis": analysis,
                "order_id": order_id,
                "actual_cost": actual_cost
            }
            
            self.balance -= actual_cost
            self.daily_trades += 1
            self.performance["total_trades"] += 1
            
            mode = "LIVE" if not self.use_paper_trading else "PAPER"
            logger.info(f"✅ {mode} BUY {ticker}: {shares} shares @ ${current_price:.2f} (Cost: ${actual_cost:.2f})")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error executing buy for {ticker}: {e}")
            return False
    
    async def _place_snaptrade_order(self, symbol: str, quantity: int, action: str) -> Optional[str]:
        """Place an order through SnapTrade API."""
        try:
            # Get symbol ID
            symbols = self.snaptrade_client.reference_data.get_symbols(
                body={"substring": symbol}
            )
            
            if not symbols.data:
                logger.error(f"❌ Symbol {symbol} not found in SnapTrade")
                return None
                
            universal_symbol_id = symbols.data[0]['id']
            
            # Check order impact first (recommended by SnapTrade)
            order_impact = self.snaptrade_client.trading.get_order_impact(
                user_id=self.user_id,
                user_secret=self.user_secret,
                body={
                    "account_id": self.primary_account_id,
                    "action": action,
                    "universal_symbol_id": universal_symbol_id,
                    "order_type": "Market",
                    "time_in_force": "Day",
                    "units": quantity
                }
            )
            
            if not order_impact.data:
                logger.error(f"❌ Order impact check failed for {symbol}")
                return None
                
            trade_id = order_impact.data.get('trade_id')
            
            # Place the order
            order_result = self.snaptrade_client.trading.place_order(
                user_id=self.user_id,
                user_secret=self.user_secret,
                trade_id=trade_id,
                body={"wait_to_confirm": True}
            )
            
            if order_result.data and order_result.data.get('status') == 'EXECUTED':
                logger.info(f"✅ SnapTrade order executed: {symbol} {action} {quantity}")
                return order_result.data.get('id')
            else:
                logger.error(f"❌ SnapTrade order failed: {order_result.data}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error placing SnapTrade order: {e}")
            return None
    
    async def _execute_sell(self, ticker: str, analysis: Dict) -> bool:
        """Execute a sell order through SnapTrade or paper trading."""
        try:
            if ticker not in self.positions:
                return False
                
            position = self.positions[ticker]
            current_price = self._get_current_price(ticker)
            
            if not current_price:
                logger.error(f"❌ Could not get price for {ticker}")
                return False
            
            shares = position["shares"]
            
            # Execute sell order through SnapTrade or simulate
            order_id = None
            if not self.use_paper_trading and self.snaptrade_client and self.primary_account_id:
                order_id = await self._place_snaptrade_order(ticker, shares, "SELL")
                if not order_id:
                    return False
            
            # Calculate P&L
            entry_cost = position["actual_cost"] if "actual_cost" in position else (position["entry_price"] * shares)
            proceeds = current_price * shares
            pnl = proceeds - entry_cost
            pnl_pct = pnl / entry_cost
            
            # Update balance and remove position
            self.balance += proceeds
            del self.positions[ticker]
            
            self.daily_trades += 1
            self.performance["total_trades"] += 1
            self.performance["total_pnl"] += pnl
            
            # Track win/loss
            mode = "LIVE" if not self.use_paper_trading else "PAPER"
            if pnl > 0:
                self.performance["winning_trades"] += 1
                self.consecutive_losses = 0
                logger.info(f"✅ {mode} SELL {ticker}: +${pnl:.2f} ({pnl_pct:.2%}) @ ${current_price:.2f}")
            else:
                self.performance["losing_trades"] += 1
                self.consecutive_losses += 1
                logger.info(f"❌ {mode} SELL {ticker}: ${pnl:.2f} ({pnl_pct:.2%}) @ ${current_price:.2f}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error executing sell for {ticker}: {e}")
            return False
    
    async def manage_positions(self):
        """Monitor and manage existing positions."""
        for ticker, position in list(self.positions.items()):
            try:
                current_price = self._get_current_price(ticker)
                if not current_price:
                    continue
                
                # Check stop loss
                if current_price <= position["stop_loss"]:
                    logger.info(f"🛑 Stop loss triggered for {ticker}: ${current_price:.2f} <= ${position['stop_loss']:.2f}")
                    await self._execute_sell(ticker, {"decision": "STOP_LOSS"})
                    continue
                    
                # Check take profit
                if current_price >= position["take_profit"]:
                    logger.info(f"🎯 Take profit triggered for {ticker}: ${current_price:.2f} >= ${position['take_profit']:.2f}")
                    await self._execute_sell(ticker, {"decision": "TAKE_PROFIT"})
                    continue
                    
                # Time-based exit (close before market close)
                if datetime.now().time() > time(15, 45):
                    logger.info(f"🕐 End-of-day close for {ticker}")
                    await self._execute_sell(ticker, {"decision": "EOD_CLOSE"})
                    continue
                    
                # Update real-time balance if using live trading
                if not self.use_paper_trading:
                    self.balance = self._get_account_balance()
                    
            except Exception as e:
                logger.error(f"Error managing position {ticker}: {e}")
    
    def update_performance_metrics(self):
        """Update performance tracking metrics."""
        total_trades = self.performance["total_trades"]
        if total_trades > 0:
            self.performance["win_rate"] = self.performance["winning_trades"] / total_trades
            
        # Calculate drawdown
        current_drawdown = (self.initial_balance - self.balance) / self.initial_balance
        self.performance["max_drawdown"] = max(self.performance["max_drawdown"], current_drawdown)
    
    def log_daily_summary(self):
        """Log daily performance summary."""
        self.update_performance_metrics()
        
        summary = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "balance": self.balance,
            "daily_pnl": self.balance - self.initial_balance,
            "daily_pnl_pct": (self.balance - self.initial_balance) / self.initial_balance,
            "trades_today": self.daily_trades,
            "open_positions": len(self.positions),
            "win_rate": self.performance["win_rate"],
            "max_drawdown": self.performance["max_drawdown"]
        }
        
        logger.info(f"📊 Daily Summary: {json.dumps(summary, indent=2)}")
        
        # Save to file
        with open(f"daily_summary_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
            json.dump(summary, f, indent=2)
    
    async def trading_loop(self):
        """Main trading loop."""
        logger.info(f"🚀 Starting Personal Trading Agent with ${self.balance:.2f}")
        
        while self.is_running and self.balance > 0:
            try:
                # Check if market is open
                if not self.is_market_open():
                    if datetime.now().time() > time(16, 30):
                        # End of day - log summary and reset daily counters
                        self.log_daily_summary()
                        self.daily_trades = 0
                        self.consecutive_losses = 0
                        
                    logger.info("💤 Market closed. Waiting...")
                    await asyncio.sleep(300)  # Wait 5 minutes
                    continue
                
                # Manage existing positions
                await self.manage_positions()
                
                # Check if it's time for new analysis
                if self.should_analyze():
                    # Get market opportunities
                    opportunities = await self.get_market_opportunities()
                    
                    # Analyze each opportunity
                    for ticker in opportunities:
                        if not self.is_running or self.balance <= 0:
                            break
                            
                        analysis = await self.analyze_opportunity(ticker)
                        if analysis:
                            await self.execute_trade(analysis)
                            
                        # Small delay between analyses
                        await asyncio.sleep(10)
                    
                    self.last_analysis_time = datetime.now()
                
                # Log current status
                if len(self.positions) > 0:
                    logger.info(f"💰 Balance: ${self.balance:.2f}, Positions: {list(self.positions.keys())}")
                else:
                    logger.info(f"💰 Balance: ${self.balance:.2f}, No positions")
                
                # Wait before next iteration
                await asyncio.sleep(self.config["risk_check_interval"])
                
            except Exception as e:
                logger.error(f"❌ Error in trading loop: {e}")
                await asyncio.sleep(60)
        
        if self.balance <= 0:
            logger.warning("🛑 Balance depleted. Trading stopped.")
        else:
            logger.info("🛑 Trading stopped by user.")
            
        # Close all positions before exit
        for ticker in list(self.positions.keys()):
            await self._execute_sell(ticker, {"decision": "SHUTDOWN"})
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info("📢 Received shutdown signal. Closing positions...")
        self.is_running = False
    
    async def start(self):
        """Start the trading agent."""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start the main trading loop
        await self.trading_loop()


async def main():
    """Main entry point for the trading agent."""
    print("🤖 Personal Trading Agent with SnapTrade Integration")
    print("=" * 60)
    print("⚠️  FOR PERSONAL RESEARCH USE ONLY")
    print("📈 Starting with $100 balance")
    print("🎯 Target: Continuous profitable trading")
    print("🛑 Stop: When balance reaches $0")
    print("")
    
    # Check for live trading setup
    use_paper = True
    if os.getenv('SNAPTRADE_CLIENT_ID') and os.getenv('SNAPTRADE_CONSUMER_KEY'):
        if os.getenv('ENABLE_LIVE_TRADING', '').lower() == 'true':
            use_paper = False
            print("🔴 LIVE TRADING MODE - REAL MONEY AT RISK")
            print("📊 Connected to real brokerage accounts via SnapTrade")
        else:
            print("📄 Paper trading mode (set ENABLE_LIVE_TRADING=true for live)")
    else:
        print("📄 Paper trading mode (no SnapTrade credentials)")
    
    print("")
    
    # Initialize and start the agent
    agent = PersonalTradingAgent(
        initial_balance=100.0,
        use_paper_trading=use_paper
    )
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        agent.signal_handler(None, None)
        print(f"\n🛑 Trading agent stopped by user")
        print(f"💰 Final balance: ${agent.balance:.2f}")


def setup_snaptrade_connection():
    """Helper function to set up SnapTrade connection."""
    print("🔗 SnapTrade Connection Setup")
    print("=" * 40)
    print("To use live trading, you need:")
    print("1. SnapTrade account: https://dashboard.snaptrade.com/")
    print("2. Connect your brokerage account through SnapTrade")
    print("3. Set environment variables:")
    print("   export SNAPTRADE_CLIENT_ID='your_client_id'")
    print("   export SNAPTRADE_CONSUMER_KEY='your_consumer_key'")
    print("   export ENABLE_LIVE_TRADING='true'")
    print("")
    print("Supported brokerages include:")
    print("• Alpaca, TD Ameritrade, E*TRADE, Robinhood")
    print("• Questrade, Wealthica, Interactive Brokers")
    print("• Schwab, Fidelity, and 10+ more")
    print("")


if __name__ == "__main__":
    # Check if user wants setup help
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_snaptrade_connection()
    else:
        asyncio.run(main())

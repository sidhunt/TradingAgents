"""Utility functions and classes for TradingAgents.

This module provides helper functions, the Toolkit class for data access,
and message management utilities for the multi-agent trading framework.
"""

from __future__ import annotations

import functools
import os
from datetime import date, datetime, timedelta
from typing import Annotated, Any, Dict, List, Optional, Union

import pandas as pd
from dateutil.relativedelta import relativedelta
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    RemoveMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

import tradingagents.dataflows.interface as interface
from tradingagents.default_config import DEFAULT_CONFIG


def create_msg_delete() -> callable:
    """Create a message deletion function for Anthropic compatibility.
    
    Returns a function that clears messages and adds a placeholder,
    which is required for compatibility with Anthropic's Claude models.
    
    Returns:
        A function that takes a state dictionary and returns updated messages.
    """
    def delete_messages(state: Dict[str, Any]) -> Dict[str, List[BaseMessage]]:
        """Clear messages and add placeholder for Anthropic compatibility.
        
        Args:
            state: The current state dictionary containing messages.
            
        Returns:
            Dictionary with removal operations and placeholder message.
        """
        messages = state.get("messages", [])
        
        # Remove all messages
        removal_operations = [RemoveMessage(id=m.id) for m in messages if hasattr(m, 'id')]
        
        # Add a minimal placeholder message
        placeholder = HumanMessage(content="Continue")
        
        return {"messages": removal_operations + [placeholder]}
    
    return delete_messages


def format_analysis_report(analysis_type: str, content: str) -> str:
    """Format an analysis report with proper structure.
    
    Args:
        analysis_type: Type of analysis (e.g., 'market', 'sentiment').
        content: The content of the analysis.
        
    Returns:
        Formatted analysis report string.
    """
    return f"""
=== {analysis_type.upper()} ANALYSIS ===
{content}
=== END {analysis_type.upper()} ANALYSIS ===
"""


def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to a maximum length.
    
    Args:
        text: The text to truncate.
        max_length: Maximum allowed length.
        
    Returns:
        Truncated text with ellipsis if needed.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def validate_ticker(ticker: str) -> bool:
    """Validate a stock ticker symbol.
    
    Args:
        ticker: The ticker symbol to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    if not ticker or not isinstance(ticker, str):
        return False
    
    # Ticker should be 1-5 characters, alphanumeric
    ticker = ticker.strip().upper()
    if len(ticker) < 1 or len(ticker) > 5:
        return False
    
    # Should only contain letters (some tickers have dots for class shares)
    if not all(c.isalpha() or c == '.' for c in ticker):
        return False
    
    return True


class Toolkit:
    """Toolkit for accessing financial data and utilities.
    
    This class provides a unified interface for accessing various data sources
    including Yahoo Finance, Finnhub, Reddit, and more.
    
    Attributes:
        config: Configuration dictionary for the toolkit.
    """
    
    _config: Dict[str, Any] = DEFAULT_CONFIG.copy()

    @classmethod
    def update_config(cls, config: Dict[str, Any]) -> None:
        """Update the class-level configuration.
        
        Args:
            config: Dictionary with configuration updates.
        """
        cls._config.update(config)

    @property
    def config(self) -> Dict[str, Any]:
        """Access the configuration.
        
        Returns:
            The current configuration dictionary.
        """
        return self._config

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the Toolkit.
        
        Args:
            config: Optional configuration dictionary to update.
        """
        if config:
            self.update_config(config)

    @staticmethod
    @tool
    def get_reddit_news(
        curr_date: Annotated[str, "Date you want to get news for in yyyy-mm-dd format"],
    ) -> str:
        """Retrieve global news from Reddit within a specified time frame.
        
        Args:
            curr_date: Date you want to get news for in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing the latest global news from Reddit.
            
        Raises:
            ValueError: If date format is invalid.
            RuntimeError: If Reddit API call fails.
        """
        try:
            global_news_result = interface.get_reddit_global_news(curr_date, 7, 5)
            return global_news_result
        except Exception as e:
            return f"Error retrieving Reddit news: {str(e)}"

    @staticmethod
    @tool
    def get_finnhub_news(
        ticker: Annotated[str, "Search query of a company, e.g. 'AAPL', 'TSM'"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """Retrieve the latest news about a given stock from Finnhub.
        
        Args:
            ticker: Ticker of a company (e.g., AAPL, TSM).
            start_date: Start date in yyyy-mm-dd format.
            end_date: End date in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing news about the company.
            
        Raises:
            ValueError: If date format is invalid.
        """
        try:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            look_back_days = (end_date_obj - start_date_obj).days

            finnhub_news_result = interface.get_finnhub_news(
                ticker, end_date, look_back_days
            )
            return finnhub_news_result
        except ValueError as e:
            return f"Invalid date format: {str(e)}"
        except Exception as e:
            return f"Error retrieving Finnhub news: {str(e)}"

    @staticmethod
    @tool
    def get_reddit_stock_info(
        ticker: Annotated[str, "Ticker of a company, e.g. AAPL, TSM"],
        curr_date: Annotated[str, "Current date you want to get news for"],
    ) -> str:
        """Retrieve the latest news about a given stock from Reddit.
        
        Args:
            ticker: Ticker of a company (e.g., AAPL, TSM).
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing the latest news about the company.
        """
        try:
            stock_news_results = interface.get_reddit_company_news(
                ticker, curr_date, 7, 5
            )
            return stock_news_results
        except Exception as e:
            return f"Error retrieving Reddit stock info: {str(e)}"

    @staticmethod
    @tool
    def get_YFin_data(
        symbol: Annotated[str, "Ticker symbol of the company"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """Retrieve stock price data from Yahoo Finance (cached/offline).
        
        Args:
            symbol: Ticker symbol of the company (e.g., AAPL, TSM).
            start_date: Start date in yyyy-mm-dd format.
            end_date: End date in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing the stock price data.
        """
        try:
            result_data = interface.get_YFin_data(symbol, start_date, end_date)
            return result_data
        except Exception as e:
            return f"Error retrieving Yahoo Finance data: {str(e)}"

    @staticmethod
    @tool
    def get_YFin_data_online(
        symbol: Annotated[str, "Ticker symbol of the company"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """Retrieve stock price data from Yahoo Finance (online/real-time).
        
        Args:
            symbol: Ticker symbol of the company (e.g., AAPL, TSM).
            start_date: Start date in yyyy-mm-dd format.
            end_date: End date in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing the stock price data.
        """
        try:
            result_data = interface.get_YFin_data_online(symbol, start_date, end_date)
            return result_data
        except Exception as e:
            return f"Error retrieving Yahoo Finance online data: {str(e)}"

    @staticmethod
    @tool
    def get_stockstats_indicators_report(
        symbol: Annotated[str, "Ticker symbol of the company"],
        indicator: Annotated[str, "Technical indicator to get the analysis and report of"],
        curr_date: Annotated[str, "The current trading date, YYYY-mm-dd"],
        look_back_days: Annotated[int, "How many days to look back"] = 30,
    ) -> str:
        """Retrieve stock stats indicators for a given ticker (cached/offline).
        
        Args:
            symbol: Ticker symbol of the company.
            indicator: Technical indicator to analyze.
            curr_date: The current trading date in YYYY-mm-dd format.
            look_back_days: Number of days to look back (default: 30).
            
        Returns:
            A formatted string containing the stock stats indicators.
        """
        try:
            result_stockstats = interface.get_stock_stats_indicators_window(
                symbol, indicator, curr_date, look_back_days, False
            )
            return result_stockstats
        except Exception as e:
            return f"Error retrieving stock stats indicators: {str(e)}"

    @staticmethod
    @tool
    def get_stockstats_indicators_report_online(
        symbol: Annotated[str, "Ticker symbol of the company"],
        indicator: Annotated[str, "Technical indicator to get the analysis and report of"],
        curr_date: Annotated[str, "The current trading date, YYYY-mm-dd"],
        look_back_days: Annotated[int, "How many days to look back"] = 30,
    ) -> str:
        """Retrieve stock stats indicators for a given ticker (online/real-time).
        
        Args:
            symbol: Ticker symbol of the company.
            indicator: Technical indicator to analyze.
            curr_date: The current trading date in YYYY-mm-dd format.
            look_back_days: Number of days to look back (default: 30).
            
        Returns:
            A formatted string containing the stock stats indicators.
        """
        try:
            result_stockstats = interface.get_stock_stats_indicators_window(
                symbol, indicator, curr_date, look_back_days, True
            )
            return result_stockstats
        except Exception as e:
            return f"Error retrieving online stock stats indicators: {str(e)}"

    @staticmethod
    @tool
    def get_finnhub_company_insider_sentiment(
        ticker: Annotated[str, "Ticker symbol for the company"],
        curr_date: Annotated[str, "Current date of trading, yyyy-mm-dd"],
    ) -> str:
        """Retrieve insider sentiment information from SEC filings.
        
        Args:
            ticker: Ticker symbol of the company.
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A report of insider sentiment over the past 30 days.
        """
        try:
            data_sentiment = interface.get_finnhub_company_insider_sentiment(
                ticker, curr_date, 30
            )
            return data_sentiment
        except Exception as e:
            return f"Error retrieving insider sentiment: {str(e)}"

    @staticmethod
    @tool
    def get_finnhub_company_insider_transactions(
        ticker: Annotated[str, "Ticker symbol"],
        curr_date: Annotated[str, "Current date of trading, yyyy-mm-dd"],
    ) -> str:
        """Retrieve insider transaction information from SEC filings.
        
        Args:
            ticker: Ticker symbol of the company.
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A report of insider transactions over the past 30 days.
        """
        try:
            data_trans = interface.get_finnhub_company_insider_transactions(
                ticker, curr_date, 30
            )
            return data_trans
        except Exception as e:
            return f"Error retrieving insider transactions: {str(e)}"

    @staticmethod
    @tool
    def get_simfin_balance_sheet(
        ticker: Annotated[str, "Ticker symbol"],
        freq: Annotated[str, "Reporting frequency: annual/quarterly"],
        curr_date: Annotated[str, "Current date of trading, yyyy-mm-dd"],
    ) -> str:
        """Retrieve the most recent balance sheet of a company.
        
        Args:
            ticker: Ticker symbol of the company.
            freq: Reporting frequency ("annual" or "quarterly").
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A report of the company's most recent balance sheet.
        """
        try:
            data_balance_sheet = interface.get_simfin_balance_sheet(
                ticker, freq, curr_date
            )
            return data_balance_sheet
        except Exception as e:
            return f"Error retrieving balance sheet: {str(e)}"

    @staticmethod
    @tool
    def get_simfin_cashflow(
        ticker: Annotated[str, "Ticker symbol"],
        freq: Annotated[str, "Reporting frequency: annual/quarterly"],
        curr_date: Annotated[str, "Current date of trading, yyyy-mm-dd"],
    ) -> str:
        """Retrieve the most recent cash flow statement of a company.
        
        Args:
            ticker: Ticker symbol of the company.
            freq: Reporting frequency ("annual" or "quarterly").
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A report of the company's most recent cash flow statement.
        """
        try:
            data_cashflow = interface.get_simfin_cashflow(ticker, freq, curr_date)
            return data_cashflow
        except Exception as e:
            return f"Error retrieving cash flow: {str(e)}"

    @staticmethod
    @tool
    def get_simfin_income_stmt(
        ticker: Annotated[str, "Ticker symbol"],
        freq: Annotated[str, "Reporting frequency: annual/quarterly"],
        curr_date: Annotated[str, "Current date of trading, yyyy-mm-dd"],
    ) -> str:
        """Retrieve the most recent income statement of a company.
        
        Args:
            ticker: Ticker symbol of the company.
            freq: Reporting frequency ("annual" or "quarterly").
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A report of the company's most recent income statement.
        """
        try:
            data_income_stmt = interface.get_simfin_income_statements(
                ticker, freq, curr_date
            )
            return data_income_stmt
        except Exception as e:
            return f"Error retrieving income statement: {str(e)}"

    @staticmethod
    @tool
    def get_google_news(
        query: Annotated[str, "Query to search with"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ) -> str:
        """Retrieve the latest news from Google News.
        
        Args:
            query: Query to search with.
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing the latest news from Google News.
        """
        try:
            google_news_results = interface.get_google_news(query, curr_date, 7)
            return google_news_results
        except Exception as e:
            return f"Error retrieving Google News: {str(e)}"

    @staticmethod
    @tool
    def get_stock_news_openai(
        ticker: Annotated[str, "The company's ticker"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ) -> str:
        """Retrieve stock news using OpenAI's news tools.
        
        Args:
            ticker: Ticker of a company (e.g., AAPL, TSM).
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing the latest news about the company.
        """
        try:
            openai_news_results = interface.get_stock_news_openai(ticker, curr_date)
            return openai_news_results
        except Exception as e:
            return f"Error retrieving stock news: {str(e)}"

    @staticmethod
    @tool
    def get_global_news_openai(
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ) -> str:
        """Retrieve macroeconomic news using OpenAI's news tools.
        
        Args:
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing macroeconomic news.
        """
        try:
            openai_news_results = interface.get_global_news_openai(curr_date)
            return openai_news_results
        except Exception as e:
            return f"Error retrieving global news: {str(e)}"

    @staticmethod
    @tool
    def get_fundamentals_openai(
        ticker: Annotated[str, "The company's ticker"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ) -> str:
        """Retrieve fundamental information using OpenAI's tools.
        
        Args:
            ticker: Ticker of a company (e.g., AAPL, TSM).
            curr_date: Current date in yyyy-mm-dd format.
            
        Returns:
            A formatted string containing fundamental information.
        """
        try:
            openai_fundamentals_results = interface.get_fundamentals_openai(
                ticker, curr_date
            )
            return openai_fundamentals_results
        except Exception as e:
            return f"Error retrieving fundamentals: {str(e)}"

    @staticmethod
    @tool
    def get_polymarket_events(
        category: Annotated[str, "Category to filter events (e.g., 'politics', 'crypto')"],
        limit: Annotated[int, "Maximum number of events to return"] = 10,
        active_only: Annotated[bool, "Only return active markets"] = True,
    ) -> str:
        """Get prediction market events from Polymarket.
        
        Args:
            category: Category to filter events.
            limit: Maximum number of events to return (default: 10).
            active_only: Only return active markets (default: True).
            
        Returns:
            A formatted string containing event information.
        """
        try:
            return interface.get_polymarket_events(category, limit, active_only)
        except Exception as e:
            return f"Error retrieving Polymarket events: {str(e)}"

    @staticmethod
    @tool
    def get_polymarket_market_analysis(
        market_id: Annotated[str, "Market ID to analyze"],
        include_history: Annotated[bool, "Include historical price data"] = True,
    ) -> str:
        """Get detailed analysis for a specific prediction market.
        
        Args:
            market_id: Market ID to analyze.
            include_history: Include historical price data (default: True).
            
        Returns:
            A formatted string containing market analysis.
        """
        try:
            return interface.get_polymarket_market_analysis(market_id, include_history)
        except Exception as e:
            return f"Error retrieving market analysis: {str(e)}"

    @staticmethod
    @tool
    def get_trending_prediction_markets(
        limit: Annotated[int, "Maximum number of trending markets to return"] = 5,
    ) -> str:
        """Get trending prediction markets based on volume and activity.
        
        Args:
            limit: Maximum number of markets to return (default: 5).
            
        Returns:
            A formatted string containing trending markets.
        """
        try:
            return interface.get_trending_prediction_markets(limit)
        except Exception as e:
            return f"Error retrieving trending markets: {str(e)}"

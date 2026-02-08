"""Tests for agent utilities."""

import pytest
from unittest.mock import Mock, patch

from tradingagents.agents.utils.agent_utils import (
    format_analysis_report,
    truncate_text,
    validate_ticker,
)


class TestAgentUtils:
    """Test cases for agent utility functions."""

    def test_format_analysis_report_with_valid_input(self):
        """Test formatting analysis report with valid input."""
        analysis_type = "market"
        content = "Stock price increased by 5%"
        result = format_analysis_report(analysis_type, content)
        
        assert analysis_type in result
        assert content in result

    def test_truncate_text_short(self):
        """Test truncating short text."""
        text = "Short text"
        result = truncate_text(text, max_length=100)
        assert result == text

    def test_truncate_text_long(self):
        """Test truncating long text."""
        text = "A" * 200
        result = truncate_text(text, max_length=100)
        assert len(result) <= 103  # 100 + "..."
        assert result.endswith("...")

    def test_validate_ticker_valid(self):
        """Test validating valid ticker symbols."""
        valid_tickers = ["AAPL", "GOOGL", "MSFT", "TSLA"]
        for ticker in valid_tickers:
            assert validate_ticker(ticker) is True

    def test_validate_ticker_invalid(self):
        """Test validating invalid ticker symbols."""
        invalid_tickers = ["", "123", "TOOLONGTICKER", "invalid!"]
        for ticker in invalid_tickers:
            assert validate_ticker(ticker) is False

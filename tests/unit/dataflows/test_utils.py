"""Tests for dataflow utilities."""

import pytest
from unittest.mock import Mock, patch
import pandas as pd

from tradingagents.dataflows.utils import (
    clean_dataframe,
    validate_date_format,
    safe_get,
)


class TestDataflowUtils:
    """Test cases for dataflow utility functions."""

    def test_clean_dataframe_removes_nan(self):
        """Test that clean_dataframe removes NaN values."""
        df = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': [5, None, 7, 8]
        })
        result = clean_dataframe(df)
        assert result.isna().sum().sum() == 0

    def test_validate_date_format_valid(self):
        """Test validating correct date formats."""
        valid_dates = ["2024-01-01", "2023-12-31", "2025-06-15"]
        for date in valid_dates:
            assert validate_date_format(date) is True

    def test_validate_date_format_invalid(self):
        """Test validating incorrect date formats."""
        invalid_dates = ["01-01-2024", "2024/01/01", "invalid", ""]
        for date in invalid_dates:
            assert validate_date_format(date) is False

    def test_safe_get_existing_key(self):
        """Test safe_get with existing key."""
        data = {"key": "value", "number": 42}
        assert safe_get(data, "key") == "value"
        assert safe_get(data, "number") == 42

    def test_safe_get_missing_key(self):
        """Test safe_get with missing key."""
        data = {"key": "value"}
        assert safe_get(data, "missing") is None
        assert safe_get(data, "missing", "default") == "default"

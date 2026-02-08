"""Tests for the configuration module."""

import os
import pytest
from unittest.mock import patch

from tradingagents.default_config import DEFAULT_CONFIG


class TestDefaultConfig:
    """Test cases for default configuration."""

    def test_config_is_dict(self):
        """Test that DEFAULT_CONFIG is a dictionary."""
        assert isinstance(DEFAULT_CONFIG, dict)

    def test_config_has_required_keys(self):
        """Test that config has all required keys."""
        required_keys = [
            "project_dir",
            "results_dir",
            "llm_provider",
            "deep_think_llm",
            "quick_think_llm",
            "max_debate_rounds",
            "online_tools",
        ]
        for key in required_keys:
            assert key in DEFAULT_CONFIG, f"Missing required key: {key}"

    def test_llm_provider_is_valid(self):
        """Test that LLM provider is a valid option."""
        valid_providers = ["openai", "anthropic", "google", "openrouter", "ollama"]
        assert DEFAULT_CONFIG["llm_provider"].lower() in valid_providers

    def test_debate_rounds_are_positive(self):
        """Test that debate rounds are positive integers."""
        assert isinstance(DEFAULT_CONFIG["max_debate_rounds"], int)
        assert DEFAULT_CONFIG["max_debate_rounds"] >= 0

    @patch.dict(os.environ, {"TRADINGAGENTS_RESULTS_DIR": "/custom/results"})
    def test_results_dir_from_env(self):
        """Test that results_dir can be set from environment variable."""
        # Re-import to pick up the environment variable
        import importlib
        from tradingagents import default_config
        importlib.reload(default_config)
        
        assert default_config.DEFAULT_CONFIG["results_dir"] == "/custom/results"

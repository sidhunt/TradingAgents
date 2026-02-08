"""Default configuration for TradingAgents.

This module contains the default configuration dictionary used throughout
the TradingAgents framework. Configuration can be customized by copying
and modifying this dictionary.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional


def _get_project_dir() -> str:
    """Get the absolute path to the project directory.
    
    Returns:
        Absolute path to the project directory.
    """
    return os.path.abspath(os.path.dirname(__file__))


def _get_data_cache_dir(project_dir: str) -> str:
    """Get the path to the data cache directory.
    
    Args:
        project_dir: The project directory path.
        
    Returns:
        Path to the data cache directory.
    """
    return os.path.join(project_dir, "dataflows", "data_cache")


def _get_results_dir() -> str:
    """Get the results directory from environment or default.
    
    Returns:
        Path to the results directory.
    """
    return os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results")


# Default configuration dictionary
DEFAULT_CONFIG: Dict[str, Any] = {
    # Directory settings
    "project_dir": _get_project_dir(),
    "results_dir": _get_results_dir(),
    "data_dir": os.getenv(
        "TRADINGAGENTS_DATA_DIR",
        "/Users/yluo/Documents/Code/ScAI/FR1-data"
    ),
    "data_cache_dir": _get_data_cache_dir(_get_project_dir()),
    
    # LLM settings
    "llm_provider": os.getenv("TRADINGAGENTS_LLM_PROVIDER", "openrouter"),
    "deep_think_llm": os.getenv(
        "TRADINGAGENTS_DEEP_THINK_LLM",
        "anthropic/claude-3.5-sonnet"
    ),
    "quick_think_llm": os.getenv(
        "TRADINGAGENTS_QUICK_THINK_LLM",
        "anthropic/claude-3.5-haiku"
    ),
    "backend_url": os.getenv(
        "TRADINGAGENTS_BACKEND_URL",
        "https://openrouter.ai/api/v1"
    ),
    
    # API Keys (loaded from environment)
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
    "google_api_key": os.getenv("GOOGLE_API_KEY"),
    "finnhub_api_key": os.getenv("FINNHUB_API_KEY"),
    "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
    
    # Debate and discussion settings
    "max_debate_rounds": int(os.getenv("TRADINGAGENTS_MAX_DEBATE_ROUNDS", "1")),
    "max_risk_discuss_rounds": int(os.getenv("TRADINGAGENTS_MAX_RISK_ROUNDS", "1")),
    "max_recur_limit": int(os.getenv("TRADINGAGENTS_MAX_RECUR", "100")),
    
    # Tool settings
    "online_tools": os.getenv("TRADINGAGENTS_ONLINE_TOOLS", "true").lower() == "true",
    
    # Logging settings
    "log_level": os.getenv("TRADINGAGENTS_LOG_LEVEL", "INFO"),
    "log_file": os.getenv("TRADINGAGENTS_LOG_FILE", None),
    
    # Trading settings
    "paper_trading_enabled": os.getenv("PAPER_TRADING_ENABLED", "false").lower() == "true",
    "paper_trading_initial_balance": float(os.getenv("PAPER_TRADING_INITIAL_BALANCE", "100000")),
    "max_position_size": int(os.getenv("MAX_POSITION_SIZE", "1000")),
    "risk_tolerance": os.getenv("RISK_TOLERANCE", "moderate"),
    "enable_live_trading": os.getenv("ENABLE_LIVE_TRADING", "false").lower() == "true",
    
    # Redis settings (for caching)
    "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    "redis_enabled": os.getenv("REDIS_ENABLED", "false").lower() == "true",
    
    # Polymarket settings
    "polymarket_enabled": os.getenv("POLYMARKET_ENABLED", "false").lower() == "true",
}


def get_config() -> Dict[str, Any]:
    """Get a copy of the default configuration.
    
    Returns:
        A deep copy of the default configuration dictionary.
    """
    import copy
    return copy.deepcopy(DEFAULT_CONFIG)


def validate_config(config: Dict[str, Any]) -> List[str]:
    """Validate a configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate.
        
    Returns:
        List of validation error messages. Empty list if valid.
    """
    errors = []
    
    # Required keys
    required_keys = [
        "llm_provider",
        "deep_think_llm",
        "quick_think_llm",
    ]
    
    for key in required_keys:
        if key not in config or not config[key]:
            errors.append(f"Missing required configuration key: {key}")
    
    # Validate LLM provider
    valid_providers = ["openai", "anthropic", "google", "openrouter", "ollama"]
    if config.get("llm_provider", "").lower() not in valid_providers:
        errors.append(
            f"Invalid llm_provider. Must be one of: {', '.join(valid_providers)}"
        )
    
    # Validate numeric values
    if config.get("max_debate_rounds", 1) < 0:
        errors.append("max_debate_rounds must be non-negative")
    
    if config.get("max_risk_discuss_rounds", 1) < 0:
        errors.append("max_risk_discuss_rounds must be non-negative")
    
    # Validate API keys based on provider
    provider = config.get("llm_provider", "").lower()
    if provider == "openai" and not config.get("openai_api_key"):
        errors.append("openai_api_key is required when using OpenAI provider")
    elif provider == "anthropic" and not config.get("anthropic_api_key"):
        errors.append("anthropic_api_key is required when using Anthropic provider")
    elif provider == "google" and not config.get("google_api_key"):
        errors.append("google_api_key is required when using Google provider")
    
    return errors


def create_config(
    llm_provider: str = "openrouter",
    deep_think_llm: str = "anthropic/claude-3.5-sonnet",
    quick_think_llm: str = "anthropic/claude-3.5-haiku",
    max_debate_rounds: int = 1,
    online_tools: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """Create a custom configuration dictionary.
    
    Args:
        llm_provider: LLM provider to use.
        deep_think_llm: Model for deep thinking tasks.
        quick_think_llm: Model for quick thinking tasks.
        max_debate_rounds: Maximum debate rounds.
        online_tools: Whether to use online data tools.
        **kwargs: Additional configuration options.
        
    Returns:
        Configuration dictionary.
        
    Example:
        >>> config = create_config(
        ...     llm_provider="openai",
        ...     deep_think_llm="gpt-4",
        ...     max_debate_rounds=2
        ... )
    """
    config = get_config()
    config.update({
        "llm_provider": llm_provider,
        "deep_think_llm": deep_think_llm,
        "quick_think_llm": quick_think_llm,
        "max_debate_rounds": max_debate_rounds,
        "online_tools": online_tools,
    })
    config.update(kwargs)
    
    # Validate the new config
    errors = validate_config(config)
    if errors:
        raise ValueError(f"Invalid configuration: {'; '.join(errors)}")
    
    return config

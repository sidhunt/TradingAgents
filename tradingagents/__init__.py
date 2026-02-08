"""TradingAgents: Multi-Agents LLM Financial Trading Framework

This package provides a comprehensive framework for multi-agent financial trading
using Large Language Models (LLMs).

Example:
    Basic usage of the TradingAgents framework:

    >>> from tradingagents import TradingAgentsGraph, DEFAULT_CONFIG
    >>> ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
    >>> state, decision = ta.propagate("NVDA", "2024-05-10")
    >>> print(decision)

Modules:
    agents: LLM-powered trading agents (analysts, researchers, traders).
    dataflows: Data ingestion and processing utilities.
    graph: LangGraph workflow definitions.
    exceptions: Custom exception classes.

Version:
    0.2.0
"""

__version__ = "0.2.0"
__author__ = "TradingAgents Team"
__email__ = "yijia.xiao@cs.ucla.edu"
__license__ = "Apache-2.0"

# Import main classes for easy access
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    from tradingagents.exceptions import (
        TradingAgentsError,
        ConfigurationError,
        APIError,
        DataError,
        ValidationError,
        AgentError,
        TradingError,
        LLMError,
    )
except ImportError as e:
    # Handle case where dependencies are not yet installed
    import warnings
    warnings.warn(f"Some dependencies not available: {e}", ImportWarning)

__all__ = [
    "TradingAgentsGraph",
    "DEFAULT_CONFIG",
    "TradingAgentsError",
    "ConfigurationError",
    "APIError",
    "DataError",
    "ValidationError",
    "AgentError",
    "TradingError",
    "LLMError",
    "__version__",
]

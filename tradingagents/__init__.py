"""
TradingAgents: Multi-Agents LLM Financial Trading Framework

This package provides a comprehensive framework for multi-agent financial trading
using Large Language Models (LLMs).
"""

__version__ = "0.1.0"
__author__ = "TradingAgents Team"
__email__ = "yijia.xiao@cs.ucla.edu"

# Import main classes for easy access
try:
    from .graph.trading_graph import TradingAgentsGraph
    from .default_config import DEFAULT_CONFIG
except ImportError:
    # Handle case where dependencies are not yet installed
    pass

__all__ = ["TradingAgentsGraph", "DEFAULT_CONFIG"]
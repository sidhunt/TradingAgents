"""CLI package for TradingAgents.

This package provides command-line interface tools for interacting with
the TradingAgents framework.

Modules:
    main: Main CLI entry point and commands.
    models: Data models for CLI operations.
    utils: Utility functions for CLI operations.
    live_trading: Live trading interface and commands.
"""

__version__ = "0.2.0"

# Import main app for easy access
try:
    from cli.main import app
except ImportError:
    pass

__all__ = ["app"]

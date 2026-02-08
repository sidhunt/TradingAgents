"""Custom exceptions for TradingAgents.

This module defines all custom exceptions used throughout the TradingAgents
framework for consistent error handling.
"""


class TradingAgentsError(Exception):
    """Base exception for all TradingAgents errors."""
    
    def __init__(self, message: str = "", details: dict = None):
        """Initialize the exception.
        
        Args:
            message: Error message.
            details: Additional error details.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(TradingAgentsError):
    """Exception raised for configuration-related errors."""
    pass


class APIError(TradingAgentsError):
    """Exception raised for API-related errors."""
    
    def __init__(self, message: str = "", status_code: int = None, details: dict = None):
        """Initialize the API error.
        
        Args:
            message: Error message.
            status_code: HTTP status code if applicable.
            details: Additional error details.
        """
        super().__init__(message, details)
        self.status_code = status_code


class DataError(TradingAgentsError):
    """Exception raised for data-related errors."""
    pass


class ValidationError(TradingAgentsError):
    """Exception raised for validation errors."""
    pass


class AgentError(TradingAgentsError):
    """Exception raised for agent-related errors."""
    pass


class TradingError(TradingAgentsError):
    """Exception raised for trading-related errors."""
    pass


class LLMError(TradingAgentsError):
    """Exception raised for LLM-related errors."""
    pass

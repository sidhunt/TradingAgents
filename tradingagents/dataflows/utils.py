"""Utility functions for dataflows module.

This module provides helper functions for data manipulation,
date handling, and output management.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import pandas as pd


# Type alias for save path parameter
SavePathType = Optional[str]


def save_output(
    data: pd.DataFrame, 
    tag: str, 
    save_path: SavePathType = None
) -> None:
    """Save DataFrame output to CSV file.
    
    Args:
        data: DataFrame to save.
        tag: Tag/label for the data being saved.
        save_path: File path to save data. If None, data is not saved.
        
    Raises:
        IOError: If file cannot be written.
    """
    if save_path:
        try:
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(save_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            
            data.to_csv(save_path, index=False)
            print(f"{tag} saved to {save_path}")
        except IOError as e:
            raise IOError(f"Failed to save {tag} to {save_path}: {e}")


def get_current_date() -> str:
    """Get today's date as a formatted string.
    
    Returns:
        Current date in YYYY-MM-DD format.
    """
    return date.today().strftime("%Y-%m-%d")


def get_current_datetime() -> datetime:
    """Get current datetime.
    
    Returns:
        Current datetime object.
    """
    return datetime.now()


def decorate_all_methods(decorator: callable) -> callable:
    """Class decorator to apply a decorator to all methods.
    
    Args:
        decorator: The decorator function to apply.
        
    Returns:
        A class decorator function.
    """
    def class_decorator(cls: type) -> type:
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                setattr(cls, attr_name, decorator(attr_value))
        return cls
    return class_decorator


def get_next_weekday(input_date: Union[str, datetime]) -> datetime:
    """Get the next weekday (Monday-Friday) from a given date.
    
    If the given date is already a weekday, returns that date.
    If it's a weekend (Saturday or Sunday), returns the following Monday.
    
    Args:
        input_date: Date to check. Can be a string (YYYY-MM-DD) or datetime.
        
    Returns:
        The next weekday as a datetime object.
        
    Raises:
        ValueError: If date string format is invalid.
    """
    if isinstance(input_date, str):
        try:
            date_obj = datetime.strptime(input_date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format. Expected YYYY-MM-DD: {e}")
    elif isinstance(input_date, datetime):
        date_obj = input_date
    else:
        raise TypeError("input_date must be a string (YYYY-MM-DD) or datetime")

    # Check if weekend (Saturday=5, Sunday=6)
    if date_obj.weekday() >= 5:
        days_to_add = 7 - date_obj.weekday()
        return date_obj + timedelta(days=days_to_add)
    else:
        return date_obj


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean a DataFrame by removing NaN values and duplicates.
    
    Args:
        df: DataFrame to clean.
        
    Returns:
        Cleaned DataFrame.
        
    Raises:
        ValueError: If df is not a valid DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    
    # Create a copy to avoid modifying the original
    cleaned = df.copy()
    
    # Remove rows where all values are NaN
    cleaned = cleaned.dropna(how='all')
    
    # Remove duplicate rows
    cleaned = cleaned.drop_duplicates()
    
    return cleaned


def validate_date_format(date_string: str) -> bool:
    """Validate that a string is in YYYY-MM-DD format.
    
    Args:
        date_string: The date string to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    if not date_string or not isinstance(date_string, str):
        return False
    
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_string):
        return False
    
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def safe_get(
    data: Dict[str, Any], 
    key: str, 
    default: Any = None
) -> Any:
    """Safely get a value from a dictionary.
    
    Args:
        data: Dictionary to get value from.
        key: Key to look up.
        default: Default value if key not found.
        
    Returns:
        The value for key if found, otherwise default.
    """
    if not isinstance(data, dict):
        return default
    return data.get(key, default)


def parse_date(date_input: Union[str, datetime, date]) -> datetime:
    """Parse various date formats into a datetime object.
    
    Args:
        date_input: Date in various formats (string, datetime, or date).
        
    Returns:
        Datetime object.
        
    Raises:
        ValueError: If date format cannot be parsed.
    """
    if isinstance(date_input, datetime):
        return date_input
    elif isinstance(date_input, date):
        return datetime.combine(date_input, datetime.min.time())
    elif isinstance(date_input, str):
        formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_input, fmt)
            except ValueError:
                continue
        raise ValueError(f"Cannot parse date: {date_input}")
    else:
        raise TypeError(f"Unsupported date type: {type(date_input)}")


def format_number(
    value: Union[int, float], 
    decimal_places: int = 2, 
    prefix: str = "", 
    suffix: str = ""
) -> str:
    """Format a number with specified decimal places and optional prefix/suffix.
    
    Args:
        value: The number to format.
        decimal_places: Number of decimal places (default: 2).
        prefix: String prefix (e.g., '$').
        suffix: String suffix (e.g., '%').
        
    Returns:
        Formatted string.
    """
    if value is None:
        return f"{prefix}N/A{suffix}"
    
    try:
        formatted = f"{value:,.{decimal_places}f}"
        return f"{prefix}{formatted}{suffix}"
    except (ValueError, TypeError):
        return f"{prefix}{value}{suffix}"


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate a string to a maximum length.
    
    Args:
        text: The text to truncate.
        max_length: Maximum allowed length.
        suffix: Suffix to add if truncated.
        
    Returns:
        Truncated string.
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON data from a file.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        Parsed JSON data as a dictionary.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
        json.JSONDecodeError: If file contains invalid JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {e}")


def save_json_file(
    data: Dict[str, Any], 
    file_path: str, 
    indent: int = 2
) -> None:
    """Save data to a JSON file.
    
    Args:
        data: Data to save.
        file_path: Path to save the file.
        indent: JSON indentation level (default: 2).
        
    Raises:
        IOError: If file cannot be written.
    """
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, default=str)
    except IOError as e:
        raise IOError(f"Failed to save JSON to {file_path}: {e}")

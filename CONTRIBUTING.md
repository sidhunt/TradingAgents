# Contributing to TradingAgents

Thank you for your interest in contributing to TradingAgents! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to:
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior vs actual behavior**
- **Environment details** (OS, Python version, package versions)
- **Code samples** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:

- **Clear use case**
- **Detailed description** of the proposed feature
- **Possible implementation approach**
- **Willingness to implement** (if applicable)

### Pull Requests

1. Fork the repository
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool (venv, conda, or poetry)

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/TradingAgents.git
cd TradingAgents

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Verify setup
make validate
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with the following specifics:

- **Line length**: 88 characters (Black default)
- **Import ordering**: isort with black profile
- **Type hints**: Required for all function signatures
- **Docstrings**: Google style docstrings

### Type Hints

All functions must include type hints:

```python
def process_data(
    data: pd.DataFrame,
    ticker: str,
    max_rows: Optional[int] = None
) -> Dict[str, Any]:
    """Process financial data for analysis.
    
    Args:
        data: Input DataFrame with financial data.
        ticker: Stock ticker symbol.
        max_rows: Maximum rows to process (optional).
        
    Returns:
        Dictionary containing processed results.
        
    Raises:
        ValueError: If data is empty or invalid.
    """
    ...
```

### Documentation

- All modules, classes, and functions must have docstrings
- Use Google style docstrings
- Include type information in docstrings
- Provide usage examples for complex functions

### Testing

- Write tests for all new functionality
- Maintain test coverage above 70%
- Use pytest for testing
- Mock external API calls

```python
def test_process_data_valid_input():
    """Test process_data with valid input."""
    data = pd.DataFrame({'price': [100, 101, 102]})
    result = process_data(data, 'AAPL')
    assert 'processed' in result
    assert result['ticker'] == 'AAPL'
```

## Project Structure

```
tradingagents/
├── agents/           # Agent implementations
├── dataflows/        # Data handling
├── graph/           # LangGraph workflows
├── exceptions.py    # Custom exceptions
└── ...

tests/
├── unit/            # Unit tests
├── integration/     # Integration tests
└── e2e/            # End-to-end tests
```

## Commit Guidelines

We follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/dependency changes

Example:
```
feat: add sentiment analysis caching

- Add Redis cache for sentiment results
- Implement cache invalidation logic
- Add configuration options
```

## Code Review Process

1. All PRs require at least one review
2. CI checks must pass
3. Reviewers will check:
   - Code quality and style
   - Test coverage
   - Documentation
   - Performance implications

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/unit/test_config.py -v

# Run with markers
pytest -m unit
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names
- One assertion per test (when possible)
- Mock external dependencies

## Documentation

### Building Docs

```bash
# Serve documentation locally
make docs-serve

# Build documentation
make docs-build
```

### Docstring Format

```python
def example_function(param1: int, param2: str) -> bool:
    """Short description of the function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: When param1 is negative.
        TypeError: When param2 is not a string.
        
    Example:
        >>> example_function(1, "test")
        True
    """
```

## Release Process

1. Update version in `pyproject.toml` and `tradingagents/__init__.py`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v0.x.x`
4. Push tag: `git push origin v0.x.x`
5. CI will automatically build and publish to PyPI

## Questions?

- Open an issue for questions
- Join our [Discord](https://discord.com/invite/hk9PGKShPK)
- Email: yijia.xiao@cs.ucla.edu

Thank you for contributing! 🎉

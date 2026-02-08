# Changelog

All notable changes to TradingAgents will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Production-ready refactoring with clean architecture principles
- Comprehensive type hints throughout the codebase
- Proper exception hierarchy with custom exception classes
- Configuration validation and environment variable support
- Docker and docker-compose support for containerized deployment
- GitHub Actions CI/CD workflows for automated testing and deployment
- Pre-commit hooks for code quality
- Comprehensive test suite structure (unit, integration, e2e)
- Makefile for common development tasks
- Detailed documentation and contribution guidelines

### Changed
- Refactored `agent_utils.py` with type hints and error handling
- Refactored `dataflows/utils.py` with validation and type safety
- Refactored `agent_states.py` with comprehensive TypedDict documentation
- Updated `default_config.py` with validation functions
- Improved `pyproject.toml` with full project metadata and tool configs
- Updated README with production deployment instructions

### Security
- Added Bandit security scanning to CI pipeline
- Added dependency vulnerability scanning

## [0.1.0] - 2024-XX-XX

### Added
- Initial release of TradingAgents
- Multi-agent trading framework with specialized agents
- CLI interface for interactive trading analysis
- Support for multiple LLM providers (OpenAI, Anthropic, Google, OpenRouter)
- Integration with Yahoo Finance, Finnhub, and other data sources
- Paper trading functionality
- Polymarket prediction market support
- GitHub Codespaces configuration

[Unreleased]: https://github.com/TauricResearch/TradingAgents/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/TauricResearch/TradingAgents/releases/tag/v0.1.0

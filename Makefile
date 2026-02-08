.PHONY: help install install-dev test lint format clean build docker-build docker-run docs

help:  ## Show this help message
	@echo "TradingAgents Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:  ## Run all tests
	pytest tests/ -v --tb=short

test-cov:  ## Run tests with coverage report
	pytest tests/ -v --cov=tradingagents --cov=cli --cov-report=html --cov-report=term-missing

test-unit:  ## Run unit tests only
	pytest tests/unit -v --tb=short

test-integration:  ## Run integration tests only
	pytest tests/integration -v --tb=short -m integration

lint:  ## Run all linters
	flake8 tradingagents cli
	black --check .
	isort --check-only .
	mypy tradingagents cli --ignore-missing-imports

format:  ## Format code with black and isort
	black .
	isort .

fix: format  ## Alias for format

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean  ## Build the package
	python -m build

docker-build:  ## Build Docker image
	docker build -t tradingagents:latest .

docker-run:  ## Run Docker container
	docker run -it --rm --env-file .env tradingagents:latest

docker-compose-up:  ## Start services with docker-compose
	docker-compose up -d

docker-compose-down:  ## Stop services with docker-compose
	docker-compose down

docs-serve:  ## Serve documentation locally
	mkdocs serve

docs-build:  ## Build documentation
	mkdocs build

run-cli:  ## Run the CLI
	python -m cli.main

run-example:  ## Run example script
	python main.py

validate:  ## Validate setup
	python validate_setup.py

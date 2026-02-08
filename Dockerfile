# TradingAgents Production Dockerfile
# Multi-stage build for optimized production image

# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim AS production

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN groupadd -r tradingagents && useradd -r -g tradingagents tradingagents

# Copy application code
COPY --chown=tradingagents:tradingagents tradingagents/ ./tradingagents/
COPY --chown=tradingagents:tradingagents cli/ ./cli/
COPY --chown=tradingagents:tradingagents pyproject.toml .

# Create directories for data and results
RUN mkdir -p /app/data /app/results /app/logs && \
    chown -R tradingagents:tradingagents /app

# Switch to non-root user
USER tradingagents

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import tradingagents; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "cli.main"]

# Labels
LABEL maintainer="TradingAgents Team <yijia.xiao@cs.ucla.edu>" \
      org.opencontainers.image.title="TradingAgents" \
      org.opencontainers.image.description="Multi-Agents LLM Financial Trading Framework" \
      org.opencontainers.image.source="https://github.com/TauricResearch/TradingAgents"

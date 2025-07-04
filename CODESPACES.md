# GitHub Codespaces Quick Start

## 🚀 One-Click Setup

This repository is configured for GitHub Codespaces - just click the button below to get started!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sidhunt/TradingAgents)

## 📋 What You Get

- **Pre-configured Python 3.12 environment**
- **All dependencies pre-installed**
- **VS Code with Python extensions**
- **Ready-to-use CLI tools**

## 🔧 Quick Setup Steps

1. **Launch Codespace** (automatic setup takes ~3-5 minutes)
2. **Set your API keys:**
   ```bash
   export FINNHUB_API_KEY="your_finnhub_key"
   export OPENAI_API_KEY="your_openai_key"
   ```
3. **Validate setup:**
   ```bash
   python validate_setup.py
   ```
4. **Run the CLI:**
   ```bash
   python -m cli.main analyze
   ```

## 📖 Complete Documentation

For detailed setup instructions, troubleshooting, and usage examples, see:
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup guide
- **[.devcontainer/README.md](.devcontainer/README.md)** - Technical documentation
- **[README.md](README.md)** - Main project documentation

## 🔑 Required API Keys

You'll need these API keys to use the full functionality:

- **FINNHUB_API_KEY**: Get from [FinnHub](https://finnhub.io/) (free tier available)
- **OPENAI_API_KEY**: Get from [OpenAI](https://platform.openai.com/) (paid service)
- **GOOGLE_API_KEY**: Optional, for Google AI services

## 🛠️ Testing Your Setup

Run these scripts to test your setup:

```bash
# Test basic setup
python test_codespaces_setup.py

# Validate full installation
python validate_setup.py

# Try example configuration
python example_config.py

# Demo CLI usage
python demo_cli.py
```

---

*This is a fork of [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) configured for easy GitHub Codespaces usage.*
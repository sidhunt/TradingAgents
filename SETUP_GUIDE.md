# TradingAgents GitHub Codespaces Setup Guide

This guide will help you set up the TradingAgents framework using GitHub Codespaces for a seamless development experience.

## 🚀 Quick Start

### Option 1: One-Click Setup (Recommended)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sidhunt/TradingAgents)

1. Click the badge above or go to your GitHub repository
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for the environment to set up (3-5 minutes)
4. Set your API keys and start using TradingAgents!

### Option 2: Manual Setup

If you prefer to set up manually, follow the [Installation instructions](README.md#installation-and-cli) in the main README.

## 📋 What's Included

Your Codespace comes pre-configured with:

- **Python 3.12** environment
- **All dependencies** from requirements.txt
- **VS Code** with Python extensions
- **Environment variables** configured
- **Port forwarding** for web apps
- **Validation scripts** to test setup

## 🔧 Setup Steps

### 1. Launch Codespace

The environment will automatically:
- Install Python dependencies
- Set up the development environment
- Configure VS Code with Python extensions
- Create necessary directories

### 2. Set API Keys

You'll need these API keys to use the full functionality:

```bash
export FINNHUB_API_KEY="your_finnhub_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export GOOGLE_API_KEY="your_google_api_key"  # Optional
```

#### Where to Get API Keys:

- **FINNHUB_API_KEY**: [FinnHub.io](https://finnhub.io/) - Free tier available
- **OPENAI_API_KEY**: [OpenAI Platform](https://platform.openai.com/) - Paid service
- **GOOGLE_API_KEY**: [Google AI Studio](https://makersuite.google.com/) - Optional

### 3. Validate Setup

Run the validation script to check everything is working:

```bash
python validate_setup.py
```

### 4. Test the CLI

```bash
# Get help
python -m cli.main --help

# Run analysis (requires API keys)
python -m cli.main analyze
```

### 5. Test Python Usage

```bash
# Run example configuration
python example_config.py

# Or use interactively
python -c "
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config['online_tools'] = True
ta = TradingAgentsGraph(debug=True, config=config)
print('TradingAgents initialized successfully!')
"
```

## 📁 Project Structure

```
TradingAgents/
├── .devcontainer/          # Codespaces configuration
│   ├── devcontainer.json   # Container configuration
│   ├── setup.sh           # Setup script
│   └── README.md          # Detailed setup docs
├── cli/                   # Command-line interface
│   └── main.py           # CLI entry point
├── tradingagents/         # Main package
│   ├── agents/           # Trading agents
│   ├── dataflows/        # Data processing
│   ├── graph/            # Agent orchestration
│   └── default_config.py # Configuration
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── validate_setup.py     # Setup validation
├── example_config.py     # Example usage
├── demo_cli.py           # CLI demo
└── CODESPACES.md         # This file
```

## 🔧 Configuration

### Environment Variables

The Codespace automatically sets:
- `PYTHONPATH`: Points to the workspace
- `TRADINGAGENTS_RESULTS_DIR`: Points to `./results`

### Port Forwarding

These ports are automatically forwarded:
- **8000**: Web server
- **8501**: Chainlit app

### VS Code Extensions

Pre-installed extensions:
- Python
- Black Formatter
- Flake8 Linter
- isort
- Jupyter
- JSON support

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   pip install -e .
   ```

2. **API Key Errors**
   ```bash
   # Check if keys are set
   echo $FINNHUB_API_KEY
   echo $OPENAI_API_KEY
   
   # Set keys for current session
   export FINNHUB_API_KEY="your_key"
   export OPENAI_API_KEY="your_key"
   ```

3. **Permission Errors**
   ```bash
   # Make scripts executable
   chmod +x .devcontainer/setup.sh
   chmod +x validate_setup.py
   ```

4. **CLI Not Working**
   ```bash
   # Check CLI dependencies
   python -c "import typer, rich; print('CLI dependencies OK')"
   
   # Run CLI help
   python -m cli.main --help
   ```

### Getting Help

- Run `python test_codespaces_setup.py` to test the setup
- Run `python validate_setup.py` to validate installation
- Check the main [README.md](README.md) for usage documentation
- Visit the [original repository](https://github.com/TauricResearch/TradingAgents) for more information

## 🎯 Next Steps

Once your setup is complete:

1. **Set your API keys** as shown above
2. **Run the validation script** to confirm everything works
3. **Try the CLI** with `python -m cli.main analyze`
4. **Explore the Python API** with `example_config.py`
5. **Read the main documentation** in [README.md](README.md)

## 🤝 Contributing

This is a fork of [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents). 

To contribute:
1. Make your changes in the Codespace
2. Test thoroughly
3. Submit pull requests to the main repository

## 📝 Notes

- The setup process may take 3-5 minutes on first launch
- API keys are required for full functionality
- The free tier of FinnHub is sufficient for most use cases
- OpenAI API usage will incur costs based on usage

---

*Happy Trading! 🚀*
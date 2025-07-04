# TradingAgents GitHub Codespaces Setup

This repository has been configured for GitHub Codespaces to provide a ready-to-use development environment.

## Quick Start with GitHub Codespaces

1. **Create a new Codespace:**
   - Go to the GitHub repository page
   - Click the green "Code" button
   - Select "Codespaces" tab
   - Click "Create codespace on main"

2. **Wait for setup to complete:**
   - The environment will automatically install all dependencies
   - This may take a few minutes on first launch

3. **Set up your API keys:**
   ```bash
   # Set environment variables for your session
   export FINNHUB_API_KEY="your_finnhub_api_key_here"
   export OPENAI_API_KEY="your_openai_api_key_here"
   export GOOGLE_API_KEY="your_google_api_key_here"  # Optional
   ```

4. **Validate the setup:**
   ```bash
   python validate_setup.py
   ```

5. **Run the CLI:**
   ```bash
   python -m cli.main analyze
   ```

## Environment Details

### Pre-installed Tools
- Python 3.12
- Git
- VS Code extensions for Python development
- All Python dependencies from requirements.txt

### Available Ports
- Port 8000: Web server
- Port 8501: Chainlit app

### Environment Variables
The following environment variables are automatically configured:
- `PYTHONPATH`: Set to the workspace root
- `TRADINGAGENTS_RESULTS_DIR`: Set to `./results`

### API Keys
The following API keys can be set as environment variables:
- `FINNHUB_API_KEY`: Required for financial data
- `OPENAI_API_KEY`: Required for AI agents
- `GOOGLE_API_KEY`: Optional for Google AI services

## Manual Setup (Alternative)

If you prefer to set up the environment manually:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sidhunt/TradingAgents.git
   cd TradingAgents
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Set environment variables:**
   ```bash
   export FINNHUB_API_KEY="your_key_here"
   export OPENAI_API_KEY="your_key_here"
   ```

5. **Run the application:**
   ```bash
   python -m cli.main analyze
   ```

## Usage Examples

### CLI Usage
```bash
# Run analysis
python -m cli.main analyze

# Get help
python -m cli.main --help
```

### Python Usage
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create custom config
config = DEFAULT_CONFIG.copy()
config["online_tools"] = True

# Initialize
ta = TradingAgentsGraph(debug=True, config=config)

# Run analysis
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

## Troubleshooting

### Common Issues

1. **Import errors:** Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

2. **API key errors:** Ensure your API keys are set correctly
   ```bash
   echo $FINNHUB_API_KEY
   echo $OPENAI_API_KEY
   ```

3. **Permission errors:** Make sure the setup script is executable
   ```bash
   chmod +x .devcontainer/setup.sh
   ```

### Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Visit the [original repository](https://github.com/TauricResearch/TradingAgents) for more information
- Run `python validate_setup.py` to check your setup

## Contributing

This is a fork of [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents). Please refer to the original repository for contribution guidelines.
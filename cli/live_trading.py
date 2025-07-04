"""
CLI commands for live trading with SnapTrade integration.
"""

import typer
import asyncio
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary
from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from live_trading_plan import PersonalTradingAgent, setup_snaptrade_connection
except ImportError:
    PersonalTradingAgent = None
    setup_snaptrade_connection = None

app = typer.Typer(name="live", help="Live trading commands")
console = Console()


@app.command()
def setup():
    """Set up SnapTrade integration for live trading."""
    if setup_snaptrade_connection:
        setup_snaptrade_connection()
    else:
        console.print("[red]❌ Live trading module not available[/red]")


@app.command()
def start(
    balance: float = typer.Option(100.0, "--balance", "-b", help="Initial trading balance"),
    paper: bool = typer.Option(True, "--paper", "-p", help="Use paper trading mode"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Start continuous live trading agent."""
    
    if not PersonalTradingAgent:
        console.print("[red]❌ Live trading module not available[/red]")
        return
    
    # Display configuration
    mode = "Paper Trading" if paper else "LIVE TRADING"
    mode_color = "green" if paper else "red"
    
    console.print(Panel.fit(
        f"[bold]{mode}[/bold]\n\n"
        f"Initial Balance: [bold green]${balance}[/bold green]\n"
        f"Mode: [bold {mode_color}]{mode}[/bold {mode_color}]\n"
        f"Agent: Multi-Agent TradingAgents System\n"
        f"Broker: SnapTrade (20+ supported brokerages)\n\n"
        f"[yellow]For personal research use only[/yellow]",
        title="🤖 Personal Trading Agent"
    ))
    
    # Safety checks for live trading
    if not paper:
        console.print(Panel.fit(
            "[bold red]⚠️  LIVE TRADING WARNINGS ⚠️[/bold red]\n\n"
            "• This will use REAL MONEY\n"
            "• You can lose your entire investment\n"
            "• Algorithmic trading involves significant risks\n"
            "• Ensure you comply with trading regulations\n"
            "• This is experimental software\n\n"
            "[bold yellow]USE AT YOUR OWN RISK[/bold yellow]",
            title="⚠️ Risk Warning"
        ))
        
        if not confirm:
            proceed = questionary.confirm(
                "Do you understand the risks and want to proceed with LIVE trading?"
            ).ask()
            
            if not proceed:
                console.print("[yellow]Live trading cancelled.[/yellow]")
                return
                
            # Double confirmation
            safety_check = questionary.text(
                "Type 'START LIVE TRADING' to confirm (case sensitive):"
            ).ask()
            
            if safety_check != "START LIVE TRADING":
                console.print("[yellow]Live trading cancelled.[/yellow]")
                return
    
    # Check environment setup
    if not paper:
        missing_vars = []
        if not os.getenv('SNAPTRADE_CLIENT_ID'):
            missing_vars.append('SNAPTRADE_CLIENT_ID')
        if not os.getenv('SNAPTRADE_CONSUMER_KEY'):
            missing_vars.append('SNAPTRADE_CONSUMER_KEY')
            
        if missing_vars:
            console.print(f"[red]❌ Missing environment variables: {', '.join(missing_vars)}[/red]")
            console.print("Run [bold]tradingagents live setup[/bold] for instructions")
            return
    
    console.print(f"[bold green]🚀 Starting trading agent...[/bold green]")
    
    # Override paper mode based on environment
    if not paper:
        os.environ['ENABLE_LIVE_TRADING'] = 'true'
    
    # Run the trading agent
    async def run_agent():
        agent = PersonalTradingAgent(
            initial_balance=balance,
            use_paper_trading=paper
        )
        
        try:
            await agent.start()
        except KeyboardInterrupt:
            agent.signal_handler(None, None)
            console.print(f"\n🛑 Trading agent stopped")
            console.print(f"💰 Final balance: ${agent.balance:.2f}")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
    
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")


@app.command()
def status():
    """Check SnapTrade connection status."""
    console.print("🔍 Checking SnapTrade connection status...")
    
    # Check environment variables
    table = Table(title="Environment Configuration")
    table.add_column("Variable", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Value", style="dim")
    
    client_id = os.getenv('SNAPTRADE_CLIENT_ID')
    consumer_key = os.getenv('SNAPTRADE_CONSUMER_KEY')
    enable_live = os.getenv('ENABLE_LIVE_TRADING')
    
    table.add_row(
        "SNAPTRADE_CLIENT_ID",
        "✅ Set" if client_id else "❌ Not set",
        f"{client_id[:8]}..." if client_id else "None"
    )
    table.add_row(
        "SNAPTRADE_CONSUMER_KEY", 
        "✅ Set" if consumer_key else "❌ Not set",
        "***hidden***" if consumer_key else "None"
    )
    table.add_row(
        "ENABLE_LIVE_TRADING",
        "✅ Enabled" if enable_live == 'true' else "📄 Paper mode",
        enable_live or "false"
    )
    
    console.print(table)
    
    # Try to connect to SnapTrade API
    if client_id and consumer_key:
        try:
            from snaptrade_python_sdk import SnapTrade
            
            snaptrade = SnapTrade(
                client_id=client_id,
                consumer_key=consumer_key
            )
            
            status_response = snaptrade.api_status.check()
            if status_response.data.get('online'):
                console.print("✅ SnapTrade API connection successful")
                console.print(f"📊 API Version: {status_response.data.get('version')}")
            else:
                console.print("❌ SnapTrade API not responding")
                
        except ImportError:
            console.print("❌ SnapTrade SDK not installed")
            console.print("Install with: pip install snaptrade-python-sdk")
        except Exception as e:
            console.print(f"❌ SnapTrade connection error: {e}")
    else:
        console.print("⚠️ SnapTrade credentials not configured")


@app.command()
def install():
    """Install SnapTrade SDK and dependencies."""
    console.print("📦 Installing SnapTrade SDK...")
    
    import subprocess
    
    try:
        # Install SnapTrade SDK
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "snaptrade-python-sdk>=11.0.110"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print("✅ SnapTrade SDK installed successfully")
        else:
            console.print(f"❌ Installation failed: {result.stderr}")
            
    except Exception as e:
        console.print(f"❌ Installation error: {e}")


if __name__ == "__main__":
    app()

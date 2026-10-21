import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from core.database import load_data, save_data

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()

THEMES = {
    "Cyberpunk Neon": {"banner_style": "bold cyan", "border_style": "bright_blue", "accent": "bold magenta"},
    "Matrix Hacker": {"banner_style": "bold green", "border_style": "green", "accent": "bold green"},
    "Gold Luxury": {"banner_style": "bold yellow", "border_style": "gold1", "accent": "bold yellow"}
}

BANNER_TEXT = """
  ╔═════════════════════════════════════════════════════════════════════════════╗
  ║    █████╗  ██████╗ ███████╗███╗   ██╗████████╗    ██████╗  ██████╗ ██████╗    ║
  ║   ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝   ██╔═══██╗██╔════╝ ██╔══██╗   ║
  ║   ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║      ██║   ██║██║  ███╗██████╔╝   ║
  ║   ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║      ██║   ██║██║   ██║██╔══██╗   ║
  ║   ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║      ╚██████╔╝╚██████╔╝███████╗   ║
  ╚═════════════════════════════════════════════════════════════════════════════╝
"""

def get_current_theme_colors():
    data = load_data()
    theme_name = data.get("theme", "Cyberpunk Neon")
    return THEMES.get(theme_name, THEMES["Cyberpunk Neon"])

def display_banner():
    colors = get_current_theme_colors()
    console.print(Panel(BANNER_TEXT, style=colors["banner_style"], border_style=colors["border_style"]))
    console.print(f" [⚡ SYSTEM STATUS: ONLINE]  [🎨 ACTIVE THEME: {load_data().get('theme', 'Cyberpunk Neon')}]", style=colors["accent"])
    console.print("─" * 80, style="dim")

def cyber_matrix_intro():
    lines = [
        "[dim]>> Initializing Quantum Neural Core...[/dim]",
        "[cyan]>> Establishing secure handshake with AI cluster nodes...[/cyan]",
        "[blue]>> Calibrating token encryption matrices...[/blue]",
        "[green]>> SUCCESS: System online and fully operational. Welcome, Operator.[/green]"
    ]
    for line in lines:
        console.print(line)
        time.sleep(0.15)
    print()

def show_loading_spinner(message="Processing Neural Bridge..."):
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40, style="blue", complete_style="bold green"),
        console=console
    ) as progress:
        task = progress.add_task(message, total=100)
        while not progress.finished:
            progress.update(task, advance=25)
            time.sleep(0.08)

def show_deployment_animation(agent_name):
    console.print(f"\n[bold yellow]🚀 Initiating deployment sequence for {agent_name}...[/bold yellow]")
    show_loading_spinner(f"Allocating GPU Tokens for {agent_name}")
    show_loading_spinner(f"Syncing REST Endpoint")
    console.print(f"[bold green]✔ {agent_name} deployed successfully to cluster![/bold green]\n")

import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()

BANNER_TEXT = """
  ╔═════════════════════════════════════════════════════════════════════════════╗
  ║    █████╗  ██████╗ ███████╗███╗   ██╗████████╗    ██████╗  ██████╗ ██████╗    ║
  ║   ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝   ██╔═══██╗██╔════╝ ██╔══██╗   ║
  ║   ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║      ██║   ██║██║  ███╗██████╔╝   ║
  ║   ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║      ██║   ██║██║   ██║██╔══██╗   ║
  ║   ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║      ╚██████╔╝╚██████╔╝██████╔╝   ║
  ╚═════════════════════════════════════════════════════════════════════════════╝
"""

def display_banner():
    console.print(Panel(BANNER_TEXT, style="bold cyan", border_style="bright_blue"))
    console.print(" [⚡ SYSTEM STATUS: ONLINE]  [🤖 ORCHESTRATION ENGINE ACTIVE]", style="bold green")
    console.print("─" * 80, style="dim")

def show_loading_spinner(message="Processing Neural Bridge..."):
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40, style="blue", complete_style="bold green"),
        console=console
    ) as progress:
        task = progress.add_task(message, total=100)
        while not progress.finished:
            progress.update(task, advance=20)
            time.sleep(0.1)

def show_deployment_animation(message="Deploying Cluster Agents..."):
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bold bright_green"),
        console=console
    ) as progress:
        task = progress.add_task(f"Deploying to {message}...", total=100)
        while not progress.finished:
            progress.update(task, advance=25)
            time.sleep(0.15)
    console.print("[bold bright_green]✔ Deployment successful! All cluster nodes are online.[/bold bright_green]")
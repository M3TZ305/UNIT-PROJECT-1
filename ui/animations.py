import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

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
    console.print("─" * 80, style="dim gray")

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
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from core.database import load_data

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

def cinematic_startup_sequence():
    """شاشة إطلاق سينمائية ضخمة ومبهرة تأخذ وقتاً كافياً ليلاحظها ويستمتع بها المستخدم"""
    display_banner()
    
    console.print("\n[bold yellow]⚡ BOOTING UP OMNI-CLUSTER NEURAL OS v4.8...[/bold yellow]\n")
    time.sleep(0.9)  # وقت كافي لقراءة الهيدر
    
    # خطوات التحميل المتسلسلة ببطء مريح وواضح
    steps = [
        ("[dim]>> [01/04] Initializing Quantum Neural Core...[/dim]", 0.5),
        ("[cyan]>> [02/04] Establishing secure handshake with AI cluster nodes...[/cyan]", 0.6),
        ("[blue]>> [03/04] Calibrating token encryption & decryption matrices...[/blue]", 0.6),
        ("[magenta]>> [04/04] Synchronizing decentralized node memory banks...[/magenta]", 0.7)
    ]
    
    for text, delay in steps:
        console.print(text)
        time.sleep(delay)
        
    # شريط تحميل مرئي حقيقي يأخذ وقتاً ثابتاً وملحوظاً
    with Progress(
        SpinnerColumn("dots", style="bold cyan"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=40, style="blue", complete_style="bold green"),
        TextColumn("[bold yellow]{task.percentage:>3.0f}%[/bold yellow]"),
        console=console
    ) as progress:
        task = progress.add_task("Stabilizing Quantum Fields", total=100)
        while not progress.finished:
            progress.update(task, advance=20)
            time.sleep(0.3)  # سرعة متوازنة وملاحظة جداً للمستخدم
            
    console.print("\n[bold green]✔ SUCCESS: System online and fully operational. Welcome, Operator.[/bold green]\n")
    time.sleep(1.2)  # توقف أخير قبل فتح القائمة ليتمكن المستخدم من قراءة رسالة الترحيب

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
            time.sleep(0.12)

def show_deployment_animation(agent_name):
    console.print(f"\n[bold yellow]🚀 Initiating deployment sequence for {agent_name}...[/bold yellow]")
    show_loading_spinner(f"Allocating GPU Tokens for {agent_name}")
    show_loading_spinner(f"Syncing REST Endpoint")
    console.print(f"[bold green]✔ {agent_name} deployed successfully to cluster![/bold green]\n")

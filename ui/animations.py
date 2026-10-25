import time
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.box import ROUNDED
from core.database import load_data
import questionary

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()
_BOOTED = False

CYBERPUNK_STYLE = questionary.Style([
    ('qmark', 'fg:#00f3ff bold'),
    ('question', 'bold white'),
    ('answer', 'fg:#00ff66 bold'),
    ('pointer', 'fg:#00f3ff bold'),
    ('highlighted', 'fg:#00f3ff bold'),
    ('selected', 'fg:#00ff66 bold'),
    ('instruction', 'dim fg:#ffb700'),
])

def clear_screen():
    """مسح الشاشة بالكامل وتعديل موضع المؤشر لتثبيت الرؤية ومنع تكدس المخزن المؤقت"""
    os.system('cls' if os.name == 'nt' else 'clear')
    console.clear()

THEMES = {
    "Cyberpunk Neon": {"banner_style": "bold #00f3ff", "border_style": "#00f3ff", "accent": "bold #ffb700"},
    "Matrix Hacker": {"banner_style": "bold #00ff66", "border_style": "#00ff66", "accent": "bold #00ff66"},
    "Gold Luxury": {"banner_style": "bold #ffb700", "border_style": "#ffb700", "accent": "bold #ffb700"}
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
    console.print(Panel(BANNER_TEXT, style=colors["banner_style"], border_style=colors["border_style"], box=ROUNDED))
    console.print(f" [bold #00f3ff]⚡ SYSTEM STATUS: ONLINE[/bold #00f3ff]  [bold #ffb700]🎨 ACTIVE THEME: {load_data().get('theme', 'Cyberpunk Neon')}[/bold #ffb700]", style=colors["accent"])
    console.print("─" * 80, style="dim")

def cinematic_startup_sequence():
    global _BOOTED
    if _BOOTED:
        return
    _BOOTED = True

    clear_screen()
    display_banner()
    
    console.print("\n[bold #00f3ff]✨ OMNI-CLUSTER NEURAL ORCHESTRATION ENGINE INITIALIZING...[/bold #00f3ff]")
    console.print("[dim]   [Please stand by while core systems and project branding load][/dim]\n")
    time.sleep(2.5)
    
    console.print("[bold #ffb700]⚡ BOOTING UP SYSTEM KERNEL v4.8...[/bold #ffb700]\n")
    time.sleep(1.2)
    
    steps = [
        ("[dim]>> [01/04] Initializing Quantum Neural Core & Memory Grids...[/dim]", 0.8),
        ("[bold #00f3ff]>> [02/04] Establishing secure quantum handshake with AI cluster nodes...[/bold #00f3ff]", 0.9),
        ("[bold #00f3ff]>> [03/04] Calibrating token encryption & decryption matrices...[/bold #00f3ff]", 0.9),
        ("[bold #00ff66]>> [04/04] Synchronizing decentralized node memory banks...[/bold #00ff66]", 1.0)
    ]
    
    for text, delay in steps:
        console.print(text)
        time.sleep(delay)
        
    with Progress(
        SpinnerColumn("dots", style="bold #00f3ff"),
        TextColumn("[bold #00f3ff]{task.description}[/bold #00f3ff]"),
        BarColumn(bar_width=40, style="dim #00f3ff", complete_style="bold #00ff66"),
        TextColumn("[bold #ffb700]{task.percentage:>3.0f}%[/bold #ffb700]"),
        console=console
    ) as progress:
        task = progress.add_task("Stabilizing Quantum Fields", total=100)
        while not progress.finished:
            progress.update(task, advance=20)
            time.sleep(0.4)
            
    console.print("\n[bold #00ff66]✔ SUCCESS: System online and fully operational. Welcome, Operator.[/bold #00ff66]\n")
    time.sleep(2.0)

def show_loading_spinner(message="Processing Neural Bridge..."):
    with Progress(
        SpinnerColumn("dots", style="bold #00f3ff"),
        TextColumn("[bold #00f3ff]{task.description}[/bold #00f3ff]"),
        BarColumn(bar_width=40, style="dim #00f3ff", complete_style="bold #00ff66"),
        console=console
    ) as progress:
        task = progress.add_task(message, total=100)
        while not progress.finished:
            progress.update(task, advance=25)
            time.sleep(0.15)

def show_deployment_animation(agent_name):
    console.print(f"\n[bold #ffb700]🚀 Initiating deployment sequence for {agent_name}...[/bold #ffb700]")
    show_loading_spinner(f"Allocating GPU Tokens for {agent_name}")
    show_loading_spinner(f"Syncing REST Endpoint")
    console.print(f"[bold #00ff66]✔ {agent_name} deployed successfully to cluster![/bold #00ff66]\n")

def smooth_menu_transition(section_name):
    clear_screen()
    display_banner()
    console.print(f"\n[bold #00f3ff]⚡ Loading [bold #ffb700]{section_name}[/bold #ffb700]...[/bold #00f3ff]")
    
    with Progress(
        SpinnerColumn("dots", style="bold #00f3ff"),
        TextColumn("[bold #00f3ff]{task.description}[/bold #00f3ff]"),
        BarColumn(bar_width=35, style="dim #00f3ff", complete_style="bold #00ff66"),
        console=console,
        transient=False
    ) as progress:
        task = progress.add_task(f"Synchronizing {section_name}", total=100)
        while not progress.finished:
            progress.update(task, advance=25)
            time.sleep(0.2)
            
    console.print(f"[bold #00ff66]>> [{section_name}] Initialized successfully.[/bold #00ff66]")
    time.sleep(0.8)
    console.print("─" * 80, style="dim")

def cinematic_exit():
    clear_screen()
    display_banner()
    
    warning_panel = Panel(
        "[bold #ffb700]WARNING:[/bold #ffb700] Initiating emergency quantum core shutdown & local storage data encryption...\n"
        "[dim]Disconnecting neural nodes, flushing memory buffers, and securing local state.[/dim]",
        title="[bold #ffb700]AGENT OGB // CRITICAL SHUTDOWN PROTOCOL[/bold #ffb700]",
        border_style="#ffb700",
        box=ROUNDED,
        padding=(1, 2)
    )
    console.print(warning_panel)
    time.sleep(1.2)
    
    console.print()
    
    with Progress(
        SpinnerColumn("dots", style="#00f3ff"),
        TextColumn("[bold #00f3ff]{task.description}[/bold #00f3ff]"),
        BarColumn(bar_width=40, style="dim #00f3ff", complete_style="bold #00ff66"),
        TextColumn("[bold #ffb700]{task.percentage:>3.0f}%[/bold #ffb700]"),
        console=console
    ) as progress:
        task1 = progress.add_task("Cooling down Quantum Cores...", total=100)
        while not progress.finished:
            progress.update(task1, advance=20)
            time.sleep(0.3)
            
    time.sleep(0.4)
    
    with Progress(
        SpinnerColumn("dots", style="#00f3ff"),
        TextColumn("[bold #00f3ff]{task.description}[/bold #00f3ff]"),
        BarColumn(bar_width=40, style="dim #00f3ff", complete_style="bold #00ff66"),
        TextColumn("[bold #ffb700]{task.percentage:>3.0f}%[/bold #ffb700]"),
        console=console
    ) as progress:
        task2 = progress.add_task("Encrypting local storage (data_store.json)...", total=100)
        while not progress.finished:
            progress.update(task2, advance=25)
            time.sleep(0.35)
            
    time.sleep(0.6)
    
    success_msg = "[🚀] SYSTEM OFFLINE. ALL NODES SECURED.\nHave a great day, Operator! See you at the top. ✨"
    success_panel = Panel(
        f"[bold #00ff66]{success_msg}[/bold #00ff66]",
        title="[bold #00ff66]AGENT OGB // OFFLINE[/bold #00ff66]",
        border_style="#00ff66",
        box=ROUNDED,
        padding=(1, 2)
    )
    console.print(success_panel)
    time.sleep(1.0)

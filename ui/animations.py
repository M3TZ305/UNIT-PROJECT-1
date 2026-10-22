import time
import sys
import os
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
_BOOTED = False

def clear_screen():
    """مسح الشاشة بالكامل وتعديل موضع المؤشر لتثبيت الرؤية ومنع تكدس المخزن المؤقت"""
    os.system('cls' if os.name == 'nt' else 'clear')
    console.clear()

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
    """شاشة إطلاق سينمائية ضخمة ومبهرة تعمل مرة واحدة فقط عند بدء التطبيق"""
    global _BOOTED
    if _BOOTED:
        return
    _BOOTED = True

    clear_screen()
    display_banner()
    
    console.print("\n[bold cyan]✨ OMNI-CLUSTER NEURAL ORCHESTRATION ENGINE INITIALIZING...[/bold cyan]")
    console.print("[dim]   [Please stand by while core systems and project branding load][/dim]\n")
    time.sleep(2.5)  # ديلاي مقصود ومطول لقراءة اسم البروجكت والترحاب
    
    console.print("[bold yellow]⚡ BOOTING UP SYSTEM KERNEL v4.8...[/bold yellow]\n")
    time.sleep(1.2)
    
    # خطوات التحميل المتسلسلة ببطء مريح وواضح
    steps = [
        ("[dim]>> [01/04] Initializing Quantum Neural Core & Memory Grids...[/dim]", 0.8),
        ("[cyan]>> [02/04] Establishing secure quantum handshake with AI cluster nodes...[/cyan]", 0.9),
        ("[blue]>> [03/04] Calibrating token encryption & decryption matrices...[/blue]", 0.9),
        ("[magenta]>> [04/04] Synchronizing decentralized node memory banks...[/magenta]", 1.0)
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
            time.sleep(0.4)  # سرعة متوازنة وملاحظة جداً للمستخدم
            
    console.print("\n[bold green]✔ SUCCESS: System online and fully operational. Welcome, Operator.[/bold green]\n")
    time.sleep(2.0)  # توقف أخير قبل الانتقال للقوائم الرئيسية

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
            time.sleep(0.15)

def show_deployment_animation(agent_name):
    console.print(f"\n[bold yellow]🚀 Initiating deployment sequence for {agent_name}...[/bold yellow]")
    show_loading_spinner(f"Allocating GPU Tokens for {agent_name}")
    show_loading_spinner(f"Syncing REST Endpoint")
    console.print(f"[bold green]✔ {agent_name} deployed successfully to cluster![/bold green]\n")

def smooth_menu_transition(section_name):
    """انميشن انتقال سلس ومرئي يعطي طابعاً سينمائياً راقياً"""
    clear_screen()
    display_banner()
    console.print(f"\n[bold cyan]⚡ Loading [yellow]{section_name}[/yellow]...[/bold cyan]")
    
    with Progress(
        SpinnerColumn("dots", style="bold cyan"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=35, style="blue", complete_style="bold green"),
        console=console,
        transient=False
    ) as progress:
        task = progress.add_task(f"Synchronizing {section_name}", total=100)
        while not progress.finished:
            progress.update(task, advance=25)
            time.sleep(0.2)
            
    console.print(f"[bold green]>> [{section_name}] Initialized successfully.[/bold green]")
    time.sleep(0.8)  # ديلاي مقصود لسلاسة الانتقال وعدم التسرع في فتح القوائم
    console.print("─" * 80, style="dim")

def cinematic_exit():
    """شاشة إيقاف تشغيل سينمائية لإنهاء التطبيق بأمان وبصريات مذهلة"""
    clear_screen()
    display_banner()
    
    # 2. Sleek Rich Panel with a red cyberpunk border warning about quantum core shutdown and data encryption
    warning_panel = Panel(
        "[bold red]WARNING:[/bold red] Initiating emergency quantum core shutdown & local storage data encryption...\n"
        "[dim]Disconnecting neural nodes, flushing memory buffers, and securing local state.[/dim]",
        title="[bold red]AGENT OGB // CRITICAL SHUTDOWN PROTOCOL[/bold red]",
        border_style="bright_red",
        padding=(1, 2)
    )
    console.print(warning_panel)
    time.sleep(1.2)
    
    console.print()
    
    # 3. Rich's Progress component for Task 1: "Cooling down Quantum Cores..." (cyan spinner, green progress bar)
    with Progress(
        SpinnerColumn("dots", style="cyan"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=40, style="dim green", complete_style="bold green"),
        TextColumn("[bold yellow]{task.percentage:>3.0f}%[/bold yellow]"),
        console=console
    ) as progress:
        task1 = progress.add_task("Cooling down Quantum Cores...", total=100)
        while not progress.finished:
            progress.update(task1, advance=20)
            time.sleep(0.3)
            
    time.sleep(0.4)
    
    # Task 2: "Encrypting local storage (data_store.json)..." (magenta/cyan spinner, green progress bar)
    with Progress(
        SpinnerColumn("dots", style="magenta"),
        TextColumn("[bold magenta]{task.description}[/bold magenta]"),
        BarColumn(bar_width=40, style="dim green", complete_style="bold green"),
        TextColumn("[bold yellow]{task.percentage:>3.0f}%[/bold yellow]"),
        console=console
    ) as progress:
        task2 = progress.add_task("Encrypting local storage (data_store.json)...", total=100)
        while not progress.finished:
            progress.update(task2, advance=25)
            time.sleep(0.35)
            
    time.sleep(0.6)
    
    # 4. Final success Rich Panel with a bright green border and exact message
    success_msg = "[🚀] SYSTEM OFFLINE. ALL NODES SECURED.\nHave a great day, Operator! See you at the top. ✨"
    success_panel = Panel(
        f"[bold green]{success_msg}[/bold green]",
        title="[bold green]AGENT OGB // OFFLINE[/bold green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    console.print(success_panel)
    time.sleep(1.0)


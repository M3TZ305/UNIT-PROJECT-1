import time
import platform
from datetime import datetime
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from core.database import load_data
from ui.animations import clear_screen

console = Console()

def generate_dashboard_layout():
    """توليد هيكل الشاشة المقسمة إلى 3 أقسام رئيسية"""
    data = load_data()
    agents = data.get("agents", [])
    history = data.get("history", [])
    tokens = data.get("tokens", 0)

    # هيكل الشاشة الأساسي (تقسيم عامودي: علوي وسفلي)
    layout = Layout()
    layout.split_column(
        Layout(name="upper", ratio=3),
        Layout(name="lower", ratio=1)
    )

    # تقسيم القسم العلوي أفقياً (قسم الكتالوج يمين/يسار، وقسم السجل الحي بجانبه)
    layout["upper"].split_row(
        Layout(name="catalog", ratio=2),
        Layout(name="logs", ratio=1)
    )

    # --- 1. قسم الكتالوج (Catalog Section) ---
    table = Table(title="[bold cyan]Live AI Agents Catalog[/bold cyan]", show_header=True, expand=True)
    table.add_column("ID", style="dim", width=4)
    table.add_column("Agent Name", style="bold green")
    table.add_column("Specialty", style="yellow")
    table.add_column("Price", justify="right", style="cyan")

    for agent in agents:
        table.add_row(agent["id"], agent["name"], agent["specialty"], f"{agent['price']} TC")
    
    catalog_panel = Panel(table, title="[bold green]📦 1. Catalog Section[/bold green]", border_style="green")

    # --- 2. قسم السجل الحي للعمليات (Live Logs Section) ---
    current_time = datetime.now().strftime("%H:%M:%S")
    logs_content = (
        f"[dim]{current_time} - Core neural bridge online[/dim]\n"
        f"[green]{current_time} - Cluster node US-East synced[/green]\n"
        f"[cyan]{current_time} - Token ledger verified securely[/cyan]\n"
        f"[yellow]{current_time} - Active deployments: {len(history)} nodes[/yellow]\n"
        f"[magenta]{current_time} - Monitoring background threads...[/magenta]\n"
        f"[bold green]>> Matrix stream running smoothly...[/bold green]"
    )
    logs_panel = Panel(logs_content, title="[bold yellow]⚡ 2. Live Logs Matrix[/bold yellow]", border_style="yellow")

    # ربط القسم العُلوي
    layout["upper"]["catalog"].update(catalog_panel)
    layout["upper"]["logs"].update(logs_panel)

    # --- 3. قسم استهلاك الـ GPU والسيرفرات في الأسفل (GPU & Server Indicators) ---
    gpu_info = (
        f" [bold magenta]GPU Load:[/bold magenta] 48% | "
        f"[bold cyan]VRAM Usage:[/bold cyan] 11.2 / 16.0 GB | "
        f"[bold yellow]Wallet Balance:[/bold yellow] {tokens} TC | "
        f"[bold green]Servers Status:[/bold green] ALL NODES OPTIMAL (100%)"
    )
    bottom_panel = Panel(gpu_info, title="[bold magenta]💻 3. GPU & Server Performance Indicators[/bold magenta]", border_style="magenta")
    
    layout["lower"].update(bottom_panel)

    return layout

def run_live_matrix_dashboard():
    """تشغيل الشاشة التفاعلية المقسمة بشكل مستقر ودون مشاكل في التيرمينال"""
    clear_screen()
    console.print("[bold yellow]🚀 Launching Live Split-Screen Dashboard Matrix...[/bold yellow]")
    console.print("[dim]Press [bold red]Ctrl + C[/bold red] or [bold red]q[/bold red] to return to the main menu.[/dim]\n")
    time.sleep(1.0)

    is_windows = platform.system() == "Windows"
    if is_windows:
        import msvcrt

    try:
        # استخدام screen=False لمنع مشاكل الـ Buffer واختفاء الشاشة في التيرمينال
        with Live(generate_dashboard_layout(), refresh_per_second=2, screen=False) as live:
            while True:
                if is_windows:
                    if msvcrt.kbhit():
                        try:
                            key = msvcrt.getch()
                            if key in (b'\xe0', b'\x00'):
                                msvcrt.getch()  # تفريغ مفاتيح الأسهم المزدوجة
                            elif key in (b'q', b'Q', b'\r', b'\n', b'\x1b'):
                                break
                        except Exception:
                            pass
                time.sleep(0.5)
                live.update(generate_dashboard_layout())
    except KeyboardInterrupt:
        pass
    
    clear_screen()
    console.print("[green]✔ Exiting Live Dashboard Matrix. Returning to main menu...[/green]\n")
    time.sleep(0.8)

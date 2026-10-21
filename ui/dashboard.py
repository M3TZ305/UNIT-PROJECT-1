from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from core.database import load_data

console = Console()

def display_live_dashboard():
    """عرض لوحة تحكم وإحصائيات بصرية شاملة للنظام"""
    data = load_data()
    tokens = data.get("tokens", 0)
    history = data.get("history", [])
    cart = data.get("cart", [])
    agents = data.get("agents", [])
    
    console.print("\n[bold cyan]📊 LIVE SYSTEM ORCHESTRATION DASHBOARD[/bold cyan]")
    console.print("─" * 80, style="dim")
    
    # 1. بطاقات الإحصائيات السريعة (Stat Cards)
    card1 = Panel(f"[bold yellow]{tokens} TC[/bold yellow]", title="[bold]Wallet Tokens[/bold]", border_style="yellow")
    card2 = Panel(f"[bold green]{len(history)}[/bold green]", title="[bold]Deployed Agents[/bold]", border_style="green")
    card3 = Panel(f"[bold cyan]{len(cart)}[/bold cyan]", title="[bold]Items in Cart[/bold]", border_style="cyan")
    card4 = Panel(f"[bold magenta]{len(agents)}[/bold magenta]", title="[bold]Marketplace Total[/bold]", border_style="magenta")
    
    console.print(Columns([card1, card2, card3, card4]))
    
    # 2. مؤشر شريط جاهزية وسعة السيرفرات (Cluster Resource Gauge)
    max_capacity = 5000
    usage_percent = min(100, int((tokens / max_capacity) * 100))
    
    console.print("\n[bold]⚡ Cluster Power Allocation Gauge:[/bold]")
    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=50, style="blue", complete_style="bold green"),
        TextColumn("[bold yellow]{task.percentage:>3.0f}%[/bold yellow]"),
        console=console
    ) as progress:
        task = progress.add_task("Token Pool Reserve", total=100)
        progress.update(task, completed=usage_percent)
        
    # 3. جدول حالة عقد السيرفرات المشغلة (Node Health Table)
    table = Table(title="[bold blue]🖥️ Neural Node Health Status[/bold blue]", show_header=True)
    table.add_column("Node ID", style="dim")
    table.add_column("Cluster Region", style="yellow")
    table.add_column("Latency", style="cyan")
    table.add_column("Status", style="bold green")
    
    table.add_row("NODE-US-EAST", "N. Virginia", "24ms", "🟢 OPTIMAL (100%)")
    table.add_row("NODE-EU-WEST", "Frankfurt", "42ms", "🟢 OPTIMAL (99.8%)")
    table.add_row("NODE-SA-CENTRAL", "Riyadh", "8ms", "🟢 ULTRA-FAST (100%)")
    
    console.print(table)
    console.print("─" * 80, style="dim")

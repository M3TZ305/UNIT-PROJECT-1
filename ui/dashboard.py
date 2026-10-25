from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.box import ROUNDED
from core.database import load_data

console = Console()

def display_live_dashboard():
    """عرض لوحة تحكم وإحصائيات بصرية شاملة للنظام"""
    data = load_data()
    tokens = data.get("tokens", 0)
    history = data.get("history", [])
    cart = data.get("cart", [])
    agents = data.get("agents", [])
    
    console.print("\n[bold #00f3ff]📊 [AgentOSا] LIVE SYSTEM DASHBOARD[/bold #00f3ff]")
    console.print("─" * 80, style="dim")
    
    # 1. بطاقات الإحصائيات السريعة (Stat Cards)
    card1 = Panel(f"[bold #ffb700]{tokens} TC[/bold #ffb700]", title="[bold #00f3ff]Wallet Tokens[/bold #00f3ff]", border_style="#ffb700", box=ROUNDED)
    card2 = Panel(f"[bold #00ff66]{len(history)}[/bold #00ff66]", title="[bold #00f3ff]Deployed Agents[/bold #00f3ff]", border_style="#00ff66", box=ROUNDED)
    card3 = Panel(f"[bold #00f3ff]{len(cart)}[/bold #00f3ff]", title="[bold #00f3ff]Items in Cart[/bold #00f3ff]", border_style="#00f3ff", box=ROUNDED)
    card4 = Panel(f"[bold #ffb700]{len(agents)}[/bold #ffb700]", title="[bold #00f3ff]Marketplace Total[/bold #00f3ff]", border_style="#00f3ff", box=ROUNDED)
    
    console.print(Columns([card1, card2, card3, card4]))
    
    # 2. مؤشر شريط جاهزية وسعة السيرفرات (Cluster Resource Gauge)
    max_capacity = 5000
    usage_percent = min(100, int((tokens / max_capacity) * 100))
    
    console.print("\n[bold #00f3ff]⚡ Cluster Power Allocation Gauge:[/bold #00f3ff]")
    with Progress(
        TextColumn("[bold #00f3ff]{task.description}[/bold #00f3ff]"),
        BarColumn(bar_width=50, style="dim #00f3ff", complete_style="bold #00ff66"),
        TextColumn("[bold #ffb700]{task.percentage:>3.0f}%[/bold #ffb700]"),
        console=console
    ) as progress:
        task = progress.add_task("Token Pool Reserve", total=100)
        progress.update(task, completed=usage_percent)
        
    # 3. جدول حالة عقد السيرفرات المشغلة (Node Health Table)
    table = Table(title="[bold #00f3ff]🖥️ Neural Node Health Status[/bold #00f3ff]", show_header=True, box=ROUNDED, border_style="#00f3ff", header_style="bold #ffb700")
    table.add_column("Node ID", style="dim")
    table.add_column("Cluster Region", style="bold #ffb700")
    table.add_column("Latency", style="bold #00f3ff")
    table.add_column("Status", style="bold #00ff66")
    
    table.add_row("NODE-US-EAST", "N. Virginia", "24ms", "🟢 OPTIMAL (100%)")
    table.add_row("NODE-EU-WEST", "Frankfurt", "42ms", "🟢 OPTIMAL (99.8%)")
    table.add_row("NODE-SA-CENTRAL", "Riyadh", "8ms", "🟢 ULTRA-FAST (100%)")
    
    console.print(table)
    console.print("─" * 80, style="dim")

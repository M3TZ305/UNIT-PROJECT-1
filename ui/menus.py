import questionary
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from core.database import load_data, save_data
from ui.animations import clear_screen

console = Console()

def display_agent_table(agents):
    table = Table(title="[bold cyan]Available AI Agents Marketplace[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Agent Name", style="bold green")
    table.add_column("Specialty", style="yellow")
    table.add_column("Success Rate", style="blue")
    table.add_column("Price (TC)", justify="right", style="cyan")

    for agent in agents:
        table.add_row(agent["id"], agent["name"], agent["specialty"], f"{agent['success_rate']}%", f"{agent['price']} TC")
    console.print(table)

def calculate_operator_rank(data):
    """تحتسب رتبة المستخدم بناءً على عدد عمليات الشراء والأنشطة في السجل"""
    history = data.get("history", [])
    count = len(history)
    
    if count >= 6:
        return "👑 [bold gold1]Master Architect[/bold gold1]"
    elif count >= 3:
        return "⚡ [bold green]Elite Hacker[/bold green]"
    elif count >= 1:
        return "💻 [bold cyan]Cyber Specialist[/bold cyan]"
    else:
        return "🌱 [dim]Novice Operator[/dim]"

def display_status_panel():
    data = load_data()
    tokens = data.get("tokens", 0)
    current_theme = data.get("theme", "Cyberpunk Neon")
    operator_rank = calculate_operator_rank(data)
    
    status_text = (
        f"[bold gold1]💰 WALLET:[/bold gold1] [bold green]{tokens} TC[/bold green]  │  "
        f"[bold cyan]🎨 THEME:[/bold cyan] [bold white]{current_theme}[/bold white]  │  "
        f"[bold magenta]RANK:[/bold magenta] {operator_rank}"
    )
    panel = Panel(
        Align.center(Text.from_markup(status_text)),
        title="[bold magenta]✦ OMNI-CLUSTER STATUS PANEL ✦[/bold magenta]",
        border_style="magenta",
        padding=(0, 1),
        expand=False
    )
    console.print(panel)

def main_menu():
    while True:
        clear_screen()
        display_status_panel()
        
        category = questionary.select(
            "Choose AI Orchestration Category:",
            choices=[
                "🛒  Store & Shopping",
                "🧪  AI Sandbox & Mini-games",
                "📊  Wallet, Dashboards & Reports",
                "⚙️  Manager Portal",
                "🚪  Exit"
            ]
        ).ask()
        
        if category is None or category == "🚪  Exit":
            return "🚪  Exit"
            
        if category == "🛒  Store & Shopping":
            sub_choice = questionary.select(
                "Store & Shopping Menu:",
                choices=[
                    "🛒  Browse AI Agents Catalogue",
                    "🔍  Search for an Agent",
                    "💡  Get AI Recommendations",
                    "🛍️  View My Cart & Checkout",
                    "📦  Track Deployment Status",
                    "⬅️  Back to Main Menu"
                ]
            ).ask()
            if sub_choice and sub_choice != "⬅️  Back to Main Menu":
                return sub_choice
                
        elif category == "🧪  AI Sandbox & Mini-games":
            sub_choice = questionary.select(
                "AI Sandbox & Mini-games Menu:",
                choices=[
                    "🖥️  Live Split-Screen Dashboard Matrix",
                    "🌐  Hack Dark Web for Free Tokens (Mini-Game)",
                    "🧪  Launch AI Agent Sandbox Playground",
                    "⬅️  Back to Main Menu"
                ]
            ).ask()
            if sub_choice and sub_choice != "⬅️  Back to Main Menu":
                return sub_choice
                
        elif category == "📊  Wallet, Dashboards & Reports":
            sub_choice = questionary.select(
                "Wallet, Dashboards & Reports Menu:",
                choices=[
                    "📊  View Live System Dashboard",
                    "📜  View Past Receipts & History",
                    "📁  Export Data Report to CSV",
                    "💳  Top-Up Wallet Tokens",
                    "🎨  Switch Terminal Theme",
                    "⬅️  Back to Main Menu"
                ]
            ).ask()
            if sub_choice and sub_choice != "⬅️  Back to Main Menu":
                return sub_choice
                
        elif category == "⚙️  Manager Portal":
            return "⚙️  Manager Portal"

def select_theme_menu():
    """قائمة اختيار الثيمات"""
    choice = questionary.select(
        "Choose a Visual Theme Style:",
        choices=[
            "Cyberpunk Neon",
            "Matrix Hacker",
            "Gold Luxury"
        ]
    ).ask()
    
    if choice:
        data = load_data()
        data["theme"] = choice
        save_data(data)
        console.print(f"[bold green]✔ Theme changed to '{choice}'! Re-open or refresh to apply full banner styles.[/bold green]")

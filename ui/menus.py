import questionary
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.box import ROUNDED
from core.database import load_data, save_data
from ui.animations import clear_screen, CYBERPUNK_STYLE

console = Console()

def display_agent_table(agents):
    from services.store import get_fluctuated_market_agents
    market_agents = get_fluctuated_market_agents(agents)
    
    table = Table(title="[bold #00f3ff]Available AI Agents Marketplace (Live Stock Exchange)[/bold #00f3ff]", show_header=True, box=ROUNDED, border_style="#00f3ff", header_style="bold #ffb700")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Agent Name", style="bold #00ff66")
    table.add_column("Specialty", style="bold #ffb700")
    table.add_column("Success Rate", style="bold #00f3ff")
    table.add_column("Market Price (TC)", justify="right", style="bold #ffb700")

    for agent in market_agents:
        price_str = agent.get("price_display", f"{agent['price']} TC")
        table.add_row(agent["id"], agent["name"], agent["specialty"], f"{agent['success_rate']}%", price_str)
    console.print(table)

def calculate_operator_rank(data):
    """تحتسب رتبة المستخدم بناءً على عدد عمليات الشراء والأنشطة في السجل"""
    history = data.get("history", [])
    count = len(history)
    
    if count >= 6:
        return "👑 [bold #ffb700]Master Architect[/bold #ffb700]"
    elif count >= 3:
        return "⚡ [bold #00ff66]Elite Hacker[/bold #00ff66]"
    elif count >= 1:
        return "💻 [bold #00f3ff]Cyber Specialist[/bold #00f3ff]"
    else:
        return "🌱 [dim]Novice Operator[/dim]"

def display_status_panel():
    data = load_data()
    tokens = data.get("tokens", 0)
    current_theme = data.get("theme", "Cyberpunk Neon")
    operator_rank = calculate_operator_rank(data)
    
    status_text = (
        f"[bold #ffb700]💰 WALLET:[/bold #ffb700] [bold #00ff66]{tokens} TC[/bold #00ff66]  │  "
        f"[bold #00f3ff]🎨 THEME:[/bold #00f3ff] [bold white]{current_theme}[/bold white]  │  "
        f"[bold #00f3ff]RANK:[/bold #00f3ff] {operator_rank}"
    )
    panel = Panel(
        Align.center(Text.from_markup(status_text)),
        title="[bold #00f3ff]✦ OMNI-CLUSTER STATUS PANEL ✦[/bold #00f3ff]",
        border_style="#00f3ff",
        box=ROUNDED,
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
            ],
            style=CYBERPUNK_STYLE
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
                    "🎟️  Redeem Promo Code",
                    "🛍️  View My Cart & Checkout",
                    "📦  Track Deployment Status",
                    "⬅️  Back to Main Menu"
                ],
                style=CYBERPUNK_STYLE
            ).ask()
            if sub_choice and sub_choice != "⬅️  Back to Main Menu":
                return sub_choice
                
        elif category == "🧪  AI Sandbox & Mini-games":
            sub_choice = questionary.select(
                "AI Sandbox & Mini-games Menu:",
                choices=[
                    "🖥️  Live Split-Screen Dashboard Matrix",
                    "🎨 ASCII Glitch Restorer (Mini-Game)",
                    "🤖 Test AI Model (Sandbox)",
                    "⬅️  Back to Main Menu"
                ],
                style=CYBERPUNK_STYLE
            ).ask()
            if sub_choice and sub_choice != "⬅️  Back to Main Menu":
                return sub_choice
                
        elif category == "📊  Wallet, Dashboards & Reports":
            sub_choice = questionary.select(
                "Wallet, Dashboards & Reports Menu:",
                choices=[
                    "📊  View Live System Dashboard",
                    "📜  View Past Receipts & History",
                    "🔐  View Encrypted Purchase Receipts",
                    "📋  View System Audit Logs",
                    "📁  Export Data Report to CSV",
                    "💳  Top-Up Wallet Tokens",
                    "🎟️  Redeem Promo Code",
                    "🎨  Switch Terminal Theme",
                    "⬅️  Back to Main Menu"
                ],
                style=CYBERPUNK_STYLE
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
        ],
        style=CYBERPUNK_STYLE
    ).ask()
    
    if choice:
        data = load_data()
        data["theme"] = choice
        save_data(data)
        console.print(f"[bold #00ff66]✔ Theme changed to '{choice}'! Re-open or refresh to apply full banner styles.[/bold #00ff66]")

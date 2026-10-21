import questionary
from rich.table import Table
from rich.console import Console
from core.database import load_data, save_data

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

def main_menu():
    data = load_data()
    tokens = data.get("tokens", 0)
    current_theme = data.get("theme", "Cyberpunk Neon")
    
    console.print(f"\n[bold yellow]💰 Wallet Balance: {tokens} TC | 🎨 Theme: {current_theme}[/bold yellow]")
    
    return questionary.select(
        "Choose your AI Orchestration Action:",
        choices=[
            "🛒 Browse AI Agents Catalogue",
            "🔍 Search for an Agent",
            "💡 Get AI Recommendations",
            "📊 View Live System Dashboard",
            "🛍️ View My Cart & Checkout",
            "💳 Top-Up Wallet Tokens",
            "🎨 Switch Terminal Theme",
            "📦 Track Deployment Status",
            "⚙️ [Manager Portal] Manage Agents & Stock",
            "🚪 Exit"
        ]
    ).ask()

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

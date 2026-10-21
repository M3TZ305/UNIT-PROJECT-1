import questionary
from rich.table import Table
from rich.console import Console

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
    return questionary.select(
        "Choose your AI Orchestration Action:",
        choices=[
            "🛒 Browse AI Agents Catalogue",
            "🔍 Search for an Agent",
            "💡 Get AI Recommendations",
            "🛍️ View My Cart & Checkout",
            "📦 Track Deployment Status",
            "⚙️ [Manager Portal] Manage Agents & Stock",
            "🚪 Exit"
        ]
    ).ask()
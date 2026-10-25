import sys
import os
os.environ["PROMPT_TOOLKIT_NO_WINDOWS_CONSOLE"] = "1"
import questionary
from core.database import load_data, save_data
from core.logger import log_action
from services.export import export_data_to_csv
from ui.animations import clear_screen, smooth_menu_transition, CYBERPUNK_STYLE
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import ROUNDED
import time

console = Console()

MANAGER_PIN = "1234"

def manager_login():
    """Manager login portal with view adjustment and screen fixing"""
    clear_screen()
    
    console.print(
        Panel(
            "[bold #00f3ff]🔒 RESTRICTED AREA: MANAGER PORTAL[/bold #00f3ff]\n"
            "[dim]Please authenticate to gain administrative access.[/dim]\n"
            "[bold #ffb700]💡 Hint: Default PIN is 1234[/bold #ffb700]",
            title="[bold #00f3ff]Security Authentication[/bold #00f3ff]",
            border_style="#00f3ff",
            box=ROUNDED,
            expand=False
        )
    )
    
    pin = console.input("\n[bold #ffb700]🔑 Enter Manager Access PIN (or type 'hint'):[/bold #ffb700] ")
    
    if pin.strip().lower() == "hint":
        console.print(Panel("[bold #ffb700]💡 Hint Reminder: The manager PIN is 1234[/bold #ffb700]", title="[bold #ffb700]Hint[/bold #ffb700]", border_style="#ffb700", box=ROUNDED, expand=False))
        time.sleep(1.5)
        pin = console.input("\n[bold #ffb700]🔑 Enter Manager Access PIN:[/bold #ffb700] ")

    if pin == MANAGER_PIN:
        console.print(Panel("[bold #00ff66]✔ ACCESS GRANTED. Welcome, Manager.[/bold #00ff66]", title="[bold #00ff66]Authentication Success[/bold #00ff66]", border_style="#00ff66", box=ROUNDED, expand=False))
        log_action("SUCCESS", "Manager successfully authenticated into the Manager Portal.")
        time.sleep(0.8)
        return True
    else:
        console.print(Panel("[bold red]❌ ACCESS DENIED: Invalid Security PIN.[/bold red]", title="[bold red]Authentication Failed[/bold red]", border_style="red", box=ROUNDED, expand=False))
        log_action("WARNING", "Manager authentication failed: Invalid security PIN entered.")
        time.sleep(1.0)
        return False

def manager_dashboard():
    """Manager dashboard for inventory management and registering new agents"""
    if not manager_login():
        return
        
    while True:
        clear_screen()
        choice = questionary.select(
            "Manager Control Panel:",
            choices=[
                "📊 View All Inventory & Stock",
                "➕ Register New AI Agent",
                "📁 Export System Data to CSV (report.csv)",
                "🗑️  Data Reset (Clear History & Logs)",
                "🔙 Back to Main Menu"
            ],
            style=CYBERPUNK_STYLE
        ).ask()
        
        if choice == "📊 View All Inventory & Stock":
            smooth_menu_transition("Manager Inventory")
            show_inventory()
            console.input("\n[dim]Press Enter to continue...[/dim]")
        elif choice == "➕ Register New AI Agent":
            smooth_menu_transition("Register New Agent")
            add_new_agent()
            console.input("\n[dim]Press Enter to continue...[/dim]")
        elif choice == "📁 Export System Data to CSV (report.csv)":
            smooth_menu_transition("CSV Exporter")
            export_data_to_csv()
            console.input("\n[dim]Press Enter to continue...[/dim]")
        elif choice == "🗑️  Data Reset (Clear History & Logs)":
            smooth_menu_transition("System Data Reset")
            reset_system_data()
            console.input("\n[dim]Press Enter to continue...[/dim]")
        else:
            log_action("SYSTEM", "Manager exited Administrator Portal and returned to main orchestration grid.")
            break

def reset_system_data():
    """Reset system data and clear logs and receipts"""
    confirm = questionary.confirm(
        "⚠️ WARNING: This will permanently wipe all history, cart items, encrypted receipts (receipts.json), audit logs (audit_logs.json), text receipts (receipts_log.txt), and reset wallet tokens to default (2000 TC). Proceed?",
        default=False,
        style=CYBERPUNK_STYLE
    ).ask()
    
    if not confirm:
        console.print(Panel("[bold #ffb700]ℹ️ Data reset canceled by operator.[/bold #ffb700]", title="[bold #ffb700]Action Aborted[/bold #ffb700]", border_style="#ffb700", box=ROUNDED, expand=False))
        return

    from core.database import DEFAULT_AGENTS
    fresh_data = {
        "agents": DEFAULT_AGENTS,
        "cart": [],
        "history": [],
        "tokens": 2000,
        "theme": "Cyberpunk Neon",
        "redeemed_codes": []
    }
    save_data(fresh_data)

    files_to_remove = ["receipts.json", "audit_logs.json", "receipts_log.txt"]
    removed_count = 0
    for f_name in files_to_remove:
        if os.path.exists(f_name):
            try:
                os.remove(f_name)
                removed_count += 1
            except Exception:
                pass

    log_action("SUCCESS", "System Data Reset executed: History, cart, receipts, and audit logs cleared.")
    
    success_panel = (
        f"[bold #00ff66]✨ SYSTEM DATA RESET COMPLETE ✨[/bold #00ff66]\n\n"
        f"[bold white]• Wallet Tokens:[/bold white] [bold #ffb700]2000 TC (Default)[/bold #ffb700]\n"
        f"[bold white]• Shopping Cart:[/bold white] [bold #00f3ff]Cleared (0 items)[/bold #00f3ff]\n"
        f"[bold white]• Purchase History:[/bold white] [bold #00f3ff]Reset (0 records)[/bold #00f3ff]\n"
        f"[bold white]• Purged Files:[/bold white] [bold #00f3ff]{removed_count} ledger files (receipts.json, audit_logs.json, receipts_log.txt)[/bold #00f3ff]\n\n"
        f"[dim]AgentOS has been initialized with a clean slate.[/dim]"
    )
    
    console.print(Panel(
        success_panel,
        title="[bold #00ff66]🧹 CLEAN SLATE RESTORED[/bold #00ff66]",
        border_style="#00ff66",
        box=ROUNDED,
        expand=False
    ))

def show_inventory():
    """Display current inventory table"""
    data = load_data()
    agents = data["agents"]
    
    table = Table(title="[bold #ffb700]Manager Inventory & Stock Control[/bold #ffb700]", show_header=True, box=ROUNDED, border_style="#ffb700", header_style="bold #00f3ff")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold #00ff66")
    table.add_column("Specialty", style="bold #00f3ff")
    table.add_column("Stock", justify="right", style="bold #ffb700")
    table.add_column("Price", justify="right", style="bold #ffb700")
    
    for agent in agents:
        table.add_row(
            agent["id"],
            agent["name"],
            agent["specialty"],
            str(agent.get("stock", 10)),
            f"{agent['price']} TC"
        )
    console.print(table)
    log_action("SYSTEM", f"Manager viewed inventory table containing {len(agents)} agents.")

def add_new_agent():
    """Register a new AI agent to the store"""
    data = load_data()
    
    name = questionary.text("Enter Agent Name:", style=CYBERPUNK_STYLE).ask()
    specialty = questionary.text("Enter Specialty (e.g. Vision, NLP):", style=CYBERPUNK_STYLE).ask()
    
    try:
        success_rate = float(questionary.text("Enter Success Rate (e.g. 98.5):", style=CYBERPUNK_STYLE).ask())
        price = int(questionary.text("Enter Price in Tokens (e.g. 400):", style=CYBERPUNK_STYLE).ask())
        stock = int(questionary.text("Enter Initial Stock Quantity:", style=CYBERPUNK_STYLE).ask())
    except ValueError:
        console.print(Panel("[bold red]❌ Invalid numeric values entered. Aborted.[/bold red]", title="[bold red]Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
        log_action("WARNING", "Agent registration failed due to invalid numeric inputs.")
        return
        
    new_id = str(len(data["agents"]) + 1).zfill(2)
    new_agent = {
        "id": new_id,
        "name": name,
        "specialty": specialty,
        "success_rate": success_rate,
        "price": price,
        "stock": stock
    }
    
    data["agents"].append(new_agent)
    save_data(data)
    log_action("SUCCESS", f"Registered new AI Agent '{name}' (Specialty: {specialty}, Price: {price} TC, Stock: {stock}) to marketplace.")
    console.print(Panel(f"[bold #00ff66]✔ Agent '{name}' successfully registered to the marketplace catalogue![/bold #00ff66]", title="[bold #00ff66]Registration Successful[/bold #00ff66]", border_style="#00ff66", box=ROUNDED, expand=False))

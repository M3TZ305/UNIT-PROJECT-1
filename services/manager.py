import sys
import os
os.environ["PROMPT_TOOLKIT_NO_WINDOWS_CONSOLE"] = "1"
import questionary
from core.database import load_data, save_data, is_valid_name
from core.crypto_receipts import display_encrypted_receipts
from core.logger import log_action
from services.export import export_data_to_csv
from ui.animations import clear_screen, smooth_menu_transition, CYBERPUNK_STYLE
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import DOUBLE, ROUNDED
import time

console = Console()

MANAGER_PIN = "1234"

def manager_login():
    """Manager login portal with Deep Matrix Green governance theme and security clearance badges."""
    while True:
        clear_screen()
        
        shield_panel = Panel(
            "[bold #00ff66]🛡️ SECURITY SHIELD: ACTIVE (100%) │ CLEARANCE: ALPHA-1 ROOT[/bold #00ff66]\n"
            "[dim]Authentication required for Cyber Security & Governance Command Center.[/dim]\n"
            "[bold #ffb700]💡 Hint: Default PIN is 1234[/bold #ffb700]\n"
            "[dim]Press Enter to return to menu[/dim]",
            title="[bold #00ff66][AgentOS] // GOVERNANCE SECURITY GATEWAY[/bold #00ff66]",
            border_style="#00ff66",
            box=DOUBLE,
            expand=False
        )
        console.print(shield_panel)
        console.print()

        pin = console.input("\n[bold #00ff66]🔑 Enter Manager Access PIN: [/bold #00ff66]")
        
        if not pin.strip():
            console.print("[dim]Returning to Main Menu...[/dim]")
            time.sleep(0.4)
            return False
            
        if pin.strip().lower() == "hint":
            console.print(Panel("[bold #ffb700]💡 Hint Reminder: The manager PIN is 1234[/bold #ffb700]", title="[bold #ffb700]Hint[/bold #ffb700]", border_style="#ffb700", box=ROUNDED, expand=False))
            time.sleep(1.5)
            continue

        if pin.strip() == MANAGER_PIN:
            console.print(Panel("[bold #00ff66]✔ ACCESS GRANTED. Alpha-1 Clearance Verified. Welcome, System Architect.[/bold #00ff66]", title="[bold #00ff66]Authentication Success[/bold #00ff66]", border_style="#00ff66", box=DOUBLE, expand=False))
            log_action("SUCCESS", "Manager successfully authenticated into the Cyber Security & Governance Portal.")
            time.sleep(0.8)
            return True
        else:
            console.print(Panel("[bold red]❌ ACCESS DENIED: Invalid Security PIN or Unauthorized Probe Detected.[/bold red]", title="[bold red]Authentication Failed[/bold red]", border_style="red", box=DOUBLE, expand=False))
            log_action("WARNING", "Manager authentication failed: Invalid security PIN entered.")
            time.sleep(1.2)

def manager_dashboard():
    """Manager dashboard for inventory management and registering new agents under Cyber Security & Governance theme."""
    if not manager_login():
        return
        
    while True:
        clear_screen()
        
        shield_panel = Panel(
            "[bold #00ff66]🛡️ GOVERNANCE ACTIVE │ SYSTEM INTEGRITY: 100% │ ENCRYPTION: FERNET[/bold #00ff66]\n"
            "[dim]Cyber Security & Governance Category Control Center[/dim]",
            title="[bold #00ff66][AgentOS] // ADMINISTRATOR COMMAND PORTAL[/bold #00ff66]",
            border_style="#00ff66",
            box=DOUBLE,
            expand=False
        )
        console.print(shield_panel)
        console.print()

        choice = questionary.select(
            "Manager Control Panel:",
            choices=[
                "📊 View All Inventory & Stock",
                "➕ Register New AI Agent",
                "📜 View Encrypted Purchase Receipts & History",
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
        elif choice == "📜 View Encrypted Purchase Receipts & History":
            smooth_menu_transition("Encrypted Purchase Receipts & History")
            display_encrypted_receipts()
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
    """Reset system data and clear logs and receipts using robust select menu under governance theme"""
    confirm_choice = questionary.select(
        "⚠️ WARNING: This will permanently wipe all history, cart items, encrypted receipts (receipts.json), audit logs (audit_logs.json), text receipts (receipts_log.txt), and reset wallet tokens to default (2000 TC). Proceed?",
        choices=[
            "No (Cancel)",
            "Yes (Proceed)"
        ],
        style=CYBERPUNK_STYLE
    ).ask()
    
    if confirm_choice != "Yes (Proceed)":
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
        f"[bold white]• Shopping Cart:[/bold white] [bold #00ff66]Cleared (0 items)[/bold #00ff66]\n"
        f"[bold white]• Purchase History:[/bold white] [bold #00ff66]Reset (0 records)[/bold #00ff66]\n"
        f"[bold white]• Purged Files:[/bold white] [bold #00ff66]{removed_count} ledger files (receipts.json, audit_logs.json, receipts_log.txt)[/bold #00ff66]\n\n"
        f"[dim]AgentOS governance vault re-initialized with a clean slate.[/dim]"
    )
    
    console.print(Panel(
        success_panel,
        title="[bold #00ff66]🧹 CLEAN SLATE RESTORED[/bold #00ff66]",
        border_style="#00ff66",
        box=DOUBLE,
        expand=False
    ))

def show_inventory():
    """Display current inventory table under Cyber Security & Governance theme"""
    data = load_data()
    agents = data["agents"]
    
    table = Table(title="[bold #00ff66]🛡️ [AgentOS] GOVERNANCE INVENTORY & STOCK CONTROL[/bold #00ff66]", show_header=True, box=DOUBLE, border_style="#00ff66", header_style="bold #ffb700")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold #00ff66")
    table.add_column("Specialty", style="bold #ffb700")
    table.add_column("Stock", justify="right", style="bold #00f3ff")
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
    """Register a new AI agent to the store under Cyber Security & Governance theme with validation"""
    data = load_data()
    
    while True:
        clear_screen()
        smooth_menu_transition("Register New Agent")
        console.print("[dim]Press Enter to return to menu[/dim]\n")
        
        name = questionary.text("Enter Agent Name:", style=CYBERPUNK_STYLE).ask()
        if not name or not name.strip():
            return
        valid, err_msg = is_valid_name(name)
        if not valid:
            console.print(Panel(f"[bold red]{err_msg}[/bold red]", title="[bold red]Validation Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
            log_action("WARNING", f"Agent registration failed: {err_msg}")
            time.sleep(1.2)
            continue
            
        specialty = questionary.text("Enter Specialty (e.g. Vision, NLP):", style=CYBERPUNK_STYLE).ask()
        if not specialty or not specialty.strip():
            return
            
        try:
            success_rate_str = questionary.text("Enter Success Rate (e.g. 98.5):", style=CYBERPUNK_STYLE).ask()
            if not success_rate_str or not success_rate_str.strip():
                return
            success_rate = float(success_rate_str)
            
            price_str = questionary.text("Enter Price in Tokens (e.g. 400):", style=CYBERPUNK_STYLE).ask()
            if not price_str or not price_str.strip():
                return
            price = int(price_str)
            
            stock_str = questionary.text("Enter Initial Stock Quantity:", style=CYBERPUNK_STYLE).ask()
            if not stock_str or not stock_str.strip():
                return
            stock = int(stock_str)
            break
        except ValueError:
            console.print(Panel("[bold red]❌ Invalid input! Letters are not allowed in numbers.[/bold red]", title="[bold red]Validation Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
            log_action("WARNING", "Agent registration failed due to invalid numeric inputs (letters in numbers).")
            time.sleep(1.2)
            continue
        
    new_id = str(len(data["agents"]) + 1).zfill(2)
    new_agent = {
        "id": new_id,
        "name": name.strip(),
        "specialty": specialty.strip(),
        "success_rate": success_rate,
        "price": price,
        "stock": stock
    }
    
    data["agents"].append(new_agent)
    save_data(data)
    log_action("SUCCESS", f"Registered new AI Agent '{name.strip()}' (Specialty: {specialty.strip()}, Price: {price} TC, Stock: {stock}) to marketplace.")
    console.print(Panel(f"[bold #00ff66]✔ Agent '{name.strip()}' successfully registered to the marketplace catalogue![/bold #00ff66]", title="[bold #00ff66]Registration Successful[/bold #00ff66]", border_style="#00ff66", box=DOUBLE, expand=False))

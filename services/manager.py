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
    """بوابة دخول المدير مع ضبط العرض وتثبيت الشاشة"""
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
    """لوحة تحكم المدير لإدارة المخزون وإضافة وكلاء جدد"""
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
        else:
            log_action("SYSTEM", "Manager exited Administrator Portal and returned to main orchestration grid.")
            break

def show_inventory():
    """عرض جدول المخزون الحالي"""
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
    """إضافة وكيل ذكاء اصطناعي جديد للمتجر"""
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

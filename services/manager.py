import sys
import os
os.environ["PROMPT_TOOLKIT_NO_WINDOWS_CONSOLE"] = "1"
import questionary
from core.database import load_data, save_data
from services.export import export_data_to_csv
from ui.animations import clear_screen, smooth_menu_transition
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time

console = Console()

# رمز الدخول الافتراضي للمدير
MANAGER_PIN = "1234"

def manager_login():
    """بوابة دخول المدير مع ضبط العرض وتثبيت الشاشة"""
    clear_screen()
    
    console.print(
        Panel(
            "[bold cyan]🔒 RESTRICTED AREA: MANAGER PORTAL[/bold cyan]\n"
            "[dim]Please authenticate to gain administrative access.[/dim]\n"
            "[yellow]💡 Hint: Default PIN is 1234[/yellow]",
            border_style="cyan",
            expand=False
        )
    )
    
    pin = console.input("\n[bold yellow]🔑 Enter Manager Access PIN (or type 'hint'):[/bold yellow] ")
    
    if pin.strip().lower() == "hint":
        console.print("\n[bold yellow]💡 Hint Reminder: The manager PIN is 1234[/bold yellow]\n")
        time.sleep(1.5)
        pin = console.input("\n[bold yellow]🔑 Enter Manager Access PIN:[/bold yellow] ")

    if pin == MANAGER_PIN:
        console.print("\n[bold green]✔ ACCESS GRANTED. Welcome, Manager.[/bold green]\n")
        time.sleep(0.8)
        return True
    else:
        console.print("\n[bold red]❌ ACCESS DENIED: Invalid Security PIN.[/bold red]\n")
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
            ]
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
            break

def show_inventory():
    """عرض جدول المخزون الحالي"""
    data = load_data()
    agents = data["agents"]
    
    table = Table(title="[bold yellow]Manager Inventory & Stock Control[/bold yellow]", show_header=True)
    table.add_column("ID", style="dim")
    table.add_column("Name", style="green")
    table.add_column("Specialty", style="cyan")
    table.add_column("Stock", justify="right", style="magenta")
    table.add_column("Price", justify="right", style="yellow")
    
    for agent in agents:
        table.add_row(
            agent["id"],
            agent["name"],
            agent["specialty"],
            str(agent.get("stock", 10)),
            f"{agent['price']} TC"
        )
    console.print(table)

def add_new_agent():
    """إضافة وكيل ذكاء اصطناعي جديد للمتجر"""
    data = load_data()
    
    name = questionary.text("Enter Agent Name:").ask()
    specialty = questionary.text("Enter Specialty (e.g. Vision, NLP):").ask()
    
    try:
        success_rate = float(questionary.text("Enter Success Rate (e.g. 98.5):").ask())
        price = int(questionary.text("Enter Price in Tokens (e.g. 400):").ask())
        stock = int(questionary.text("Enter Initial Stock Quantity:").ask())
    except ValueError:
        console.print("[red]❌ Invalid numeric values entered. Aborted.[/red]")
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
    console.print(f"[green]✔ Agent '{name}' successfully registered to the marketplace catalogue![/green]")

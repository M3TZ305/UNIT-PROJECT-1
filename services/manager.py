import questionary
from core.database import load_data, save_data
from rich.console import Console
from rich.table import Table

console = Console()

def manager_login():
    """التحقق البسيط من صلاحيات المدير"""
    password = questionary.password("Enter Manager Access Key (Hint: 1234):").ask()
    if password == "1234":
        console.print("[green]✔ Manager access granted![/green]")
        return True
    else:
        console.print("[red]❌ Incorrect access key. Access denied.[/red]")
        return False

def manager_dashboard():
    """لوحة تحكم المدير لإدارة المخزون وإضافة وكلاء جدد"""
    if not manager_login():
        return
        
    while True:
        choice = questionary.select(
            "Manager Control Panel:",
            choices=[
                "📊 View All Inventory & Stock",
                "➕ Register New AI Agent",
                "🔙 Back to Main Menu"
            ]
        ).ask()
        
        if choice == "📊 View All Inventory & Stock":
            show_inventory()
        elif choice == "➕ Register New AI Agent":
            add_new_agent()
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
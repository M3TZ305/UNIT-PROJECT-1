import questionary
from core.database import load_data, save_data
from rich.console import Console
from rich.table import Table

console = Console()

def search_agents(query):
    """البحث عن وكيل بالاسم أو التخصص"""
    data = load_data()
    query = query.lower()
    results = [a for a in data["agents"] if query in a["name"].lower() or query in a["specialty"].lower()]
    return results

def add_to_cart(agent_id):
    """إضافة وكيل إلى سلة المشتريات"""
    data = load_data()
    agent = next((a for a in data["agents"] if a["id"] == agent_id), None)
    
    if not agent:
        console.print(f"[red]❌ Agent ID '{agent_id}' not found![/red]")
        return False
        
    if any(item["id"] == agent_id for item in data["cart"]):
        console.print(f"[yellow]⚠️ Agent '{agent['name']}' is already in your cart.[/yellow]")
        return False
        
    data["cart"].append(agent)
    save_data(data)
    console.print(f"[green]✔ Added {agent['name']} to cart successfully![/green]")
    return True

def remove_from_cart(agent_id):
    """إزالة وكيل من السلة"""
    data = load_data()
    cart = data["cart"]
    new_cart = [item for item in cart if item["id"] != agent_id]
    
    if len(new_cart) == len(cart):
        console.print(f"[red]❌ Agent ID '{agent_id}' is not in your cart.[/red]")
        return False
        
    data["cart"] = new_cart
    save_data(data)
    console.print(f"[green]✔ Agent removed from cart successfully![/green]")
    return True

def list_cart():
    """عرض محتويات سلة المشتريات"""
    data = load_data()
    cart = data["cart"]
    
    if not cart:
        console.print("[yellow]🛒 Your cart is currently empty.[/yellow]")
        return 0
        
    table = Table(title="[bold magenta]Your Shopping Cart[/bold magenta]", show_header=True)
    table.add_column("ID", style="dim")
    table.add_column("Agent Name", style="bold green")
    table.add_column("Price (TC)", justify="right", style="cyan")
    
    total = 0
    for item in cart:
        table.add_row(item["id"], item["name"], f"{item['price']} TC")
        total += item["price"]
        
    console.print(table)
    console.print(f"[bold cyan]Total Cart Value: {total} TC[/bold cyan]\n")
    return total

def get_recommendations():
    """تقديم توصيات ذكية للمستخدم بناءً على سجل المشتريات"""
    data = load_data()
    history = data.get("history", [])
    agents = data["agents"]
    
    if not history:
        return sorted(agents, key=lambda x: x["success_rate"], reverse=True)[:2]
    
    bought_ids = {item["id"] for item in history}
    recommended = [a for a in agents if a["id"] not in bought_ids]
    return recommended[:2] if recommended else agents[:2]

def top_up_tokens():
    """ميزة شحن الرصيد مع التحقق الصارم من الاسم ورقم البطاقة (10 أرقام بالضبط)"""
    data = load_data()
    current_tokens = data.get("tokens", 0)
    
    console.print(f"\n[cyan]💳 Your Current Balance:[/cyan] [bold yellow]{current_tokens} TC[/bold yellow]")
    
    # 1. طلب اسم المستخدم والتحقق من أنه حروف فقط
    name = questionary.text("Enter your full name for billing:").ask()
    if not name or not name.strip() or not name.replace(" ", "").isalpha():
        console.print("[red]❌ Invalid Name! Name must contain letters only (no numbers or special symbols). Top-up canceled.[/red]\n")
        return
        
    # 2. طلب رقم البطاقة والتحقق من طوله (10 أرقام بالضبط)
    card_number = questionary.text("Enter 10-Digit Card Number:").ask()
    if not card_number or not card_number.isdigit() or len(card_number) != 10:
        console.print("[red]❌ Invalid Card Number! It must be exactly 10 digits (less or more is rejected). Top-up canceled.[/red]\n")
        return
        
    # 3. طلب كمية الـ Tokens
    amount_str = questionary.text("Enter Token amount to top-up (e.g. 1000):").ask()
    if amount_str and amount_str.isdigit():
        amount = int(amount_str)
        if amount > 0:
            data["tokens"] = current_tokens + amount
            save_data(data)
            console.print(f"[bold green]✔ Thank you, {name.strip()}! Successfully added {amount} TC! New Balance: {data['tokens']} TC[/bold green]\n")
            return
            
    console.print("[red]❌ Invalid token amount entered. Top-up canceled.[/red]\n")

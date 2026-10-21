import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    
    # إذا لم تكن هناك مشتريات سابقة، نقترح الأفضل تقييماً
    if not history:
        return sorted(agents, key=lambda x: x["success_rate"], reverse=True)[:2]
    
    # اقتراح وكلاء غير موجودين في السجل
    bought_ids = {item["id"] for item in history}
    recommended = [a for a in agents if a["id"] not in bought_ids]
    return recommended[:2] if recommended else agents[:2]

def top_up_tokens():
    """شحن رصيد المحفظة بالتوكنز"""
    data = load_data()
    amount_str = questionary.text("Enter amount of Tokens (TC) to top-up:").ask()
    try:
        amount = int(amount_str)
        if amount <= 0:
            console.print("[red]❌ Amount must be greater than zero.[/red]")
            return
        data["tokens"] = data.get("tokens", 2000) + amount
        save_data(data)
        console.print(f"[green]✔ Successfully added {amount} TC! New Wallet Balance: {data['tokens']} TC[/green]")
    except ValueError:
        console.print("[red]❌ Invalid numeric value entered.[/red]")
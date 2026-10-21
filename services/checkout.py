import time
from core.database import load_data, save_data
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def process_checkout(endpoint_address):
    """إتمام عملية الشراء، خصم الرصيد، حفظ التاريخ، وإصدار الفاتورة"""
    data = load_data()
    cart = data["cart"]
    
    if not cart:
        console.print("[yellow]🛒 Your cart is empty. Add agents before checkout.[/yellow]")
        return False
        
    total_price = sum(item["price"] for item in cart)
    current_tokens = data.get("tokens", 2000)
    
    if current_tokens < total_price:
        console.print(f"[red]❌ Insufficient tokens! You have {current_tokens} TC, but need {total_price} TC.[/red]")
        return False
        
    # خصم الرصيد وتفريغ السلة ونقل المنتجات للسجل (History)
    data["tokens"] -= total_price
    for item in cart:
        data["history"].append(item)
        
    data["cart"] = []
    save_data(data)
    
    # محاكاة تجهيز النشر
    console.print("\n[bold yellow]⚡ Processing Quantum Payment & Cluster Allocation...[/bold yellow]")
    time.sleep(1)
    
    # عرض الفاتورة (Receipt)
    generate_receipt(cart, total_price, endpoint_address)
    return True

def generate_receipt(cart, total_price, endpoint_address):
    """طباعة إيصال رقمي فاخر بعمليات الشراء"""
    receipt_table = Table(title="[bold green]📜 OFFICIAL SPACETIME & AI RECEIPT[/bold green]", show_header=True)
    receipt_table.add_column("Item Name", style="cyan")
    receipt_table.add_column("Type", style="yellow")
    receipt_table.add_column("Price", justify="right", style="green")
    
    for item in cart:
        receipt_table.add_row(item["name"], item["specialty"], f"{item['price']} TC")
        
    console.print(receipt_table)
    console.print(Panel(
        f"[bold]Target Endpoint Address:[/bold] {endpoint_address}\n"
        f"[bold]Total Paid:[/bold] {total_price} TC\n"
        f"[bold]Status:[/bold] [green]SUCCESSFULLY DEPLOYED & LICENSED[/green]",
        title="[cyan]Transaction Details[/cyan]",
        border_style="green"
    ))

def track_deployment_status():
    """تتبع حالة نشر وشحن الوكلاء"""
    data = load_data()
    history = data.get("history", [])
    
    if not history:
        console.print("[yellow]📦 No active or past deployments found in history.[/yellow]")
        return
        
    table = Table(title="[bold cyan]Active AI Cluster Deployments[/bold cyan]", show_header=True)
    table.add_column("Agent Name", style="bold green")
    table.add_column("Specialty", style="yellow")
    table.add_column("Deployment Status", style="bold blue")
    
    for item in history:
        table.add_row(item["name"], item["specialty"], "🟢 ONLINE / SYNCED (100%)")
        
    console.print(table)
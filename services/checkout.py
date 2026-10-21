import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from core.database import load_data, save_data
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

def process_checkout(endpoint_address):
    """إتمام عملية الشراء مع خطوات سينمائية بطيئة وملاحظة بوضوح للمستخدم"""
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
        
    # خصم الرصيد وتفريغ السلة ونقل المنتجات للسجل
    data["tokens"] -= total_price
    for item in cart:
        data["history"].append(item)
        
    data["cart"] = []
    save_data(data)
    
    # 1. مرحلة معالجة الدفع ببطء ملحوظ
    console.print("\n")
    with console.status("[bold yellow]⚡ Processing Quantum Payment & Cluster Allocation...[/bold yellow]", spinner="dots"):
        time.sleep(2.0)  # توقف واضح ليقرأ المستخدم الرسالة
    
    # 2. مرحلة شاشة الاحتفال والوميض الحركي
    display_success_celebration()
    
    # 3. توقف قصير مريح قبل طباعة الفاتورة على الشاشة
    with console.status("[bold cyan]📜 Compiling Official Spacetime Receipt...[/bold cyan]", spinner="arc"):
        time.sleep(1.8)
    
    generate_receipt(cart, total_price, endpoint_address)
    
    # 4. توقف قبل حفظ الملف وتأكيد السجل
    with console.status("[bold green]💾 Exporting & Syncing Receipts Ledger...[/bold green]", spinner="line"):
        time.sleep(1.5)
        
    save_receipt_to_file(cart, total_price, endpoint_address)
    return True

def display_success_celebration():
    """أنيميشن احتفالي حركي ومبهر مع تأثير الوميض ببطء ملحوظ"""
    with console.status("[bold yellow]🎆 Launching Cluster Fireworks & Generating License...[/bold yellow]", spinner="earth"):
        time.sleep(2.2)
    
    colors = ["green", "cyan", "yellow", "green", "cyan", "green"]
    for color in colors:
        console.print(Text("✨ SUCCESS! ALL NODES DEPLOYED & SYNCED ✨", style=f"bold {color}"), justify="center")
        time.sleep(0.35)
        
    time.sleep(0.5)
        
    celebration_box = Panel(
        "[bold green]✨ TRANSACTION COMPLETE & CLUSTER DEPLOYED ✨[/bold green]\n"
        "[cyan]═══════════════════════════════════════════════[/cyan]\n"
        "[bold yellow]🔐 SECURE LICENSE BADGE GENERATED SUCCESSFULLY[/bold yellow]\n"
        "[dim]Status: Verified by Quantum Ledger. All nodes are active & synced.[/dim]",
        title="[bold green]🎉 SUCCESS CELEBRATION[/bold green]",
        border_style="bold green"
    )
    console.print("\n")
    console.print(celebration_box)
    console.print("\n")
    time.sleep(1.0)  # وقفة بعد عرض صندوق الاحتفال ليتمكن المستخدم من تأمله

def generate_receipt(cart, total_price, endpoint_address):
    """طباعة إيصال رقمي فاخر على الشاشة"""
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
    time.sleep(1.5)  # وقفة لتأمل الفاتورة قبل إكمال أي عملية أخرى

def save_receipt_to_file(cart, total_price, endpoint_address):
    """حفظ وتخزين جميع عمليات الشراء وتراكمها في سجل الفواتير"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "receipts_log.txt"
    
    content = f"""==================================================
           OFFICIAL AI MARKETPLACE RECEIPT        
==================================================
Date/Time: {timestamp}
Target Endpoint: {endpoint_address}
--------------------------------------------------
PURCHASED AGENTS:
"""
    for item in cart:
        content += f"- {item['name']} ({item['specialty']}) | Price: {item['price']} TC\n"
        
    content += f"""--------------------------------------------------
TOTAL PAID: {total_price} TC
STATUS: SUCCESSFUL & DEPLOYED
==================================================

"""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[bold green]📄 Receipt logged & saved to '{filename}'![/bold green]\n")
        time.sleep(1.0)
    except Exception as e:
        console.print(f"[red]⚠️ Failed to export receipt file: {e}[/red]")

def track_deployment_status():
    """تتبع حالة نشر وشحن الوكلاء"""
    data = load_data()
    history = data.get("history", [])
    
    if not history:
        console.print("[yellow]📦 No active or past deployments found in history.[/yellow]")
        return
        
    with console.status("[bold cyan]Querying Cluster Deployment Nodes...[/bold cyan]", spinner="dots"):
        time.sleep(1.2)
        
    table = Table(title="[bold cyan]Active AI Cluster Deployments[/bold cyan]", show_header=True)
    table.add_column("Agent Name", style="bold green")
    table.add_column("Specialty", style="yellow")
    table.add_column("Deployment Status", style="bold blue")
    
    for item in history:
        table.add_row(item["name"], item["specialty"], "🟢 ONLINE / SYNCED (100%)")
        
    console.print(table)

def view_purchase_history():
    """عرض سجل المشتريات والفواتير السابقة داخل جدول أنيق في البرنامج"""
    data = load_data()
    history = data.get("history", [])
    
    if not history:
        console.print("[yellow]📜 No purchase history or receipts found yet.[/yellow]")
        return
        
    table = Table(title="[bold cyan]📜 Past Purchase History & Deployed Receipts[/bold cyan]", show_header=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Agent Name", style="bold green")
    table.add_column("Specialty", style="yellow")
    table.add_column("Price Paid", justify="right", style="cyan")
    
    for idx, item in enumerate(history, 1):
        table.add_row(
            str(idx),
            item["name"],
            item["specialty"],
            f"{item['price']} TC"
        )
    console.print(table)
    console.print("[dim]💡 Tip: Full text receipts are also automatically appended to 'receipts_log.txt'.[/dim]\n")

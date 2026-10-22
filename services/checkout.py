import time
import random
import uuid
from datetime import datetime
from core.database import load_data, save_data
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import questionary

console = Console()

def process_checkout(endpoint_address):
    """إتمام عملية الشراء، توليد شهادة الترخيص الرقمية ASCII Art، وحفظها"""
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
        
    # طلب اسم المشتري لإصدار شهادة الترخيص الرسمية
    buyer_name = questionary.text("Enter License Holder Full Name:").ask()
    if not buyer_name or not buyer_name.strip():
        buyer_name = "Authorized Developer"

    # خصم الرصيد وتفريغ السلة ونقل المنتجات للسجل
    data["tokens"] -= total_price
    for item in cart:
        data["history"].append(item)
        
    data["cart"] = []
    save_data(data)
    
    # 1. معالجة الدفع السينمائية
    console.print("\n")
    with console.status("[bold yellow]⚡ Processing Quantum Payment & Cluster Allocation...[/bold yellow]", spinner="dots"):
        time.sleep(2.0)
    
    # 2. شاشة الاحتفال والحركات الحركية
    display_success_celebration()
    
    # 3. توليد وعرض شهادة الترخيص الرقمية بـ ASCII Art
    with console.status("[bold cyan]🎨 Generating Encrypted ASCII Digital License...[/bold cyan]", spinner="arc"):
        time.sleep(1.5)
        
    cert_text, ref_id = generate_ascii_certificate(buyer_name.strip(), endpoint_address)
    
    # طباعة الشهادة بألوان متوهجة فخمة
    console.print(Panel(
        f"[bold bright_cyan]{cert_text}[/bold bright_cyan]",
        title="[bold green]🏆 OFFICIAL DIGITAL LICENSE CERTIFICATE[/bold green]",
        border_style="bold bright_cyan"
    ))
    time.sleep(2.0)
    
    # 4. حفظ الفاتورة والشهادة في ملف السجل
    save_receipt_to_file(cart, total_price, endpoint_address, buyer_name.strip(), ref_id, cert_text)
    return True

def display_success_celebration():
    """أنيميشن احتفالي حركي ومبهر مع تأثير الوميض"""
    with console.status("[bold yellow]🎆 Launching Cluster Fireworks & Generating License...[/bold yellow]", spinner="earth"):
        time.sleep(2.2)
    
    colors = ["green", "cyan", "yellow", "green", "cyan", "green"]
    for color in colors:
        console.print(Text("✨ SUCCESS! ALL NODES DEPLOYED & SYNCED ✨", style=f"bold {color}"), justify="center")
        time.sleep(0.35)
        
    time.sleep(0.5)

def generate_ascii_certificate(buyer_name, endpoint_address):
    """توليد شهادة ترخيص رقمية ضخمة بتصميم ASCII Art فريد ومشفر"""
    ref_id = f"CRN-{uuid.uuid4().hex[:6].upper()}-{random.randint(1000, 9999)}"
    barcode = "█ █║█║█ █║█ █║█║█ █║█ █║█║█ █ █║██"
    
    ascii_cert = f"""
  +------------------------------------------------------------------+
  |                   AI CLUSTER LICENSE CERTIFICATE                 |
  +------------------------------------------------------------------+
  |  HOLDER NAME  : {buyer_name:<45} |
  |  REFERENCE ID : {ref_id:<45} |
  |  ENDPOINT IP  : {endpoint_address:<45} |
  |  STATUS       : [ SECURED & VERIFIED BY QUANTUM CORE ]           |
  |                                                                  |
  |  SECURE BARCODE: {barcode}                 |
  +------------------------------------------------------------------+
    """
    return ascii_cert, ref_id

def save_receipt_to_file(cart, total_price, endpoint_address, buyer_name, ref_id, cert_text):
    """حفظ شهادة الترخيص والفاتورة تراكمياً في سجل الفواتير"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "receipts_log.txt"
    
    content = f"""{cert_text}
Timestamp: {timestamp}
Total Paid: {total_price} TC
--------------------------------------------------
"""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[bold green]📄 Digital Certificate & Receipt successfully logged to '{filename}'![/bold green]\n")
        time.sleep(1.0)
    except Exception as e:
        console.print(f"[red]⚠️ Failed to export certificate file: {e}[/red]")

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

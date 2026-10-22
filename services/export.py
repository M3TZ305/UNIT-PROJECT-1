import csv
from datetime import datetime
from core.database import load_data
from rich.console import Console

console = Console()

def export_data_to_csv():
    """تصدير سجل المشتريات والبيانات إلى ملف report.csv حقيقي"""
    data = load_data()
    history = data.get("history", [])
    agents = data.get("agents", [])
    
    filename = "report.csv"
    
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # 1. كتابة الترويسة والبيانات العامة
            writer.writerow(["=== AI MARKETPLACE EXPORT REPORT ==="])
            writer.writerow(["Generated At", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow(["Total Tokens Remaining", data.get("tokens", 0)])
            writer.writerow([])  # سطر فارغ للترتيب
            
            # 2. كتابة جدول سجل المشتريات (Transaction History)
            writer.writerow(["--- TRANSACTION & DEPLOYMENT HISTORY ---"])
            writer.writerow(["Transaction #", "Agent ID", "Agent Name", "Buyer Name", "Specialty", "Purchase Time", "Price (TC)"])
            
            if history:
                for idx, item in enumerate(history, 1):
                    writer.writerow([
                        idx,
                        item.get("id", "N/A"),
                        item.get("name", "N/A"),
                        item.get("buyer", "Authorized Developer"),
                        item.get("specialty", "N/A"),
                        item.get("timestamp", "N/A"),
                        item.get("price", 0)
                    ])
            else:
                writer.writerow(["No transactions recorded yet", "", "", "", "", "", ""])
                
            writer.writerow([])
            
            # 3. كتابة جدول كتالوج الوكلاء والمخزون الحالي (Catalog Inventory)
            writer.writerow(["--- LIVE AGENTS INVENTORY ---"])
            writer.writerow(["Agent ID", "Agent Name", "Specialty", "Success Rate (%)", "Price (TC)", "Stock"])
            
            for agent in agents:
                writer.writerow([
                    agent.get("id"),
                    agent.get("name"),
                    agent.get("specialty"),
                    agent.get("success_rate"),
                    agent.get("price"),
                    agent.get("stock", 10)
                ])
                
        console.print(f"\n[bold green]📊 Report successfully exported to '{filename}'![/bold green]")
        console.print("[dim]You can now open 'report.csv' in Excel or any data viewer.[/dim]\n")
        return True
    except Exception as e:
        console.print(f"[red]❌ Failed to export CSV report: {e}[/red]\n")
        return False

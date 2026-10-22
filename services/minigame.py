import random
import time
import questionary
from core.database import load_data, save_data
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_hacking_minigame():
    """لعبة مصغرة لفك شفرة الدارك ويب واختراق السيرفر لكسب رصيد Tokens مجاني"""
    console.print(Panel(
        "[bold red]⚠️ WARNING: TRACEFIREWALL DETECTED![/bold red]\n"
        "[yellow]You are attempting to breach the Quantum Dark Web gateway to mine free tokens.\n"
        "You have 3 attempts to crack the 3-digit security passcode (Range: 100 - 500).[/yellow]",
        title="[bold red]🌐 DARK WEB HACKING TERMINAL[/bold red]",
        border_style="red"
    ))
    
    secret_code = random.randint(100, 500)
    attempts = 3
    
    while attempts > 0:
        console.print(f"\n[bold cyan]🔓 Attempts remaining: {attempts}[/bold cyan]")
        guess_str = questionary.text("Enter 3-digit security passcode guess:").ask()
        
        if not guess_str or not guess_str.isdigit():
            console.print("[red]❌ Invalid input! Enter numbers only.[/red]")
            continue
            
        guess = int(guess_str)
        
        # محاكاة تحليل الاختراق
        with console.status("[bold yellow]⚡ Bypassing firewall layers...[/bold yellow]", spinner="aesthetic"):
            time.sleep(1.0)
            
        if guess == secret_code:
            reward = 750
            data = load_data()
            data["tokens"] = data.get("tokens", 0) + reward
            save_data(data)
            
            console.print(Panel(
                f"[bold green]🎉 ACCESS GRANTED! FIREWALL BREACHED SUCCESSFULLY![/bold green]\n"
                f"[yellow]You successfully mined and transferred [bold]{reward} TC[/bold] to your wallet.[/yellow]",
                title="[bold green]💻 HACKING SUCCESSFUL[/bold green]",
                border_style="green"
            ))
            time.sleep(1.5)
            return True
        elif guess < secret_code:
            console.print("[bold yellow]📈 ACCESS DENIED: The target passcode is HIGHER ⬆️[/bold yellow]")
        else:
            console.print("[bold yellow]📉 ACCESS DENIED: The target passcode is LOWER ⬇️[/bold yellow]")
            
        attempts -= 1
        
    console.print(Panel(
        "[bold red]🚨 TRACE COMPLETE! YOU HAVE BEEN LOCKED OUT OF THE DARK WEB![/bold red]\n"
        "[dim]Security counter-measures deployed. No tokens awarded.[/dim]",
        title="[bold red]💀 HACK FAILED[/bold red]",
        border_style="red"
    ))
    time.sleep(2.0)
    return False

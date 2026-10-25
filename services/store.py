import random
import re
import questionary
from core.database import load_data, save_data
from core.logger import log_action
from core.crypto_receipts import create_encrypted_receipt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.box import ROUNDED
from ui.animations import CYBERPUNK_STYLE

console = Console()

def get_fluctuated_market_agents(agents=None):
    """Calculate dynamic market price fluctuations and generate Rich markup badges for agents."""
    if agents is None:
        data = load_data()
        agents = data.get("agents", [])
        
    fluctuated_list = []
    for agent in agents:
        agent_copy = agent.copy()
        if "base_price" not in agent_copy:
            agent_copy["base_price"] = agent_copy["price"]
            
        pct = round(random.uniform(-3.5, 3.5), 1)
        if pct == 0.0:
            pct = 1.5
            
        new_price = max(10, int(round(agent_copy["base_price"] * (1 + pct / 100))))
        agent_copy["price"] = new_price
        agent_copy["fluctuation_pct"] = pct
        
        if pct >= 0:
            agent_copy["price_display"] = f"{new_price} TC [bold #00ff66]▲ +{pct:.1f}%[/bold #00ff66]"
        else:
            agent_copy["price_display"] = f"{new_price} TC [bold red]▼ {pct:.1f}%[/bold red]"
            
        fluctuated_list.append(agent_copy)
        
    return fluctuated_list

def search_agents(query):
    """Search for an agent by name or specialty"""
    data = load_data()
    query = query.lower()
    results = [a for a in data["agents"] if query in a["name"].lower() or query in a["specialty"].lower()]
    log_action("SYSTEM", f"Searched agents catalogue with query: '{query}' (Found {len(results)} results)")
    return results

def add_to_cart(agent_id):
    """Add an agent to the shopping cart"""
    data = load_data()
    agent = next((a for a in data["agents"] if a["id"] == agent_id), None)
    
    if not agent:
        console.print(Panel(f"[bold red]❌ Agent ID '{agent_id}' not found![/bold red]", title="[bold red]Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
        return False
        
    if any(item["id"] == agent_id for item in data["cart"]):
        console.print(Panel(f"[bold #ffb700]⚠️ Agent '{agent['name']}' is already in your cart.[/bold #ffb700]", title="[bold #ffb700]Cart Warning[/bold #ffb700]", border_style="#ffb700", box=ROUNDED, expand=False))
        return False
        
    data["cart"].append(agent)
    save_data(data)
    log_action("SUCCESS", f"Added agent '{agent['name']}' (ID: {agent_id}) to shopping cart.")
    console.print(Panel(f"[bold #00ff66]✔ Added {agent['name']} to cart successfully![/bold #00ff66]", title="[bold #00ff66]Success[/bold #00ff66]", border_style="#00ff66", box=ROUNDED, expand=False))
    return True

def remove_from_cart(agent_id):
    """Remove an agent from the cart"""
    data = load_data()
    cart = data["cart"]
    new_cart = [item for item in cart if item["id"] != agent_id]
    
    if len(new_cart) == len(cart):
        console.print(Panel(f"[bold red]❌ Agent ID '{agent_id}' is not in your cart.[/bold red]", title="[bold red]Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
        return False
        
    data["cart"] = new_cart
    save_data(data)
    log_action("SYSTEM", f"Removed agent ID '{agent_id}' from shopping cart.")
    console.print(Panel("[bold #00ff66]✔ Agent removed from cart successfully![/bold #00ff66]", title="[bold #00ff66]Success[/bold #00ff66]", border_style="#00ff66", box=ROUNDED, expand=False))
    return True

def list_cart():
    """Display shopping cart contents"""
    data = load_data()
    cart = data["cart"]
    
    if not cart:
        console.print(Panel("[bold #ffb700]🛒 Your cart is currently empty.[/bold #ffb700]", title="[bold #ffb700]Shopping Cart[/bold #ffb700]", border_style="#ffb700", box=ROUNDED, expand=False))
        return 0
        
    table = Table(title="[bold #00f3ff]Your Shopping Cart[/bold #00f3ff]", show_header=True, box=ROUNDED, border_style="#00f3ff", header_style="bold #ffb700")
    table.add_column("ID", style="dim")
    table.add_column("Agent Name", style="bold #00ff66")
    table.add_column("Price (TC)", justify="right", style="bold #ffb700")
    
    total = 0
    for item in cart:
        table.add_row(item["id"], item["name"], f"{item['price']} TC")
        total += item["price"]
        
    console.print(table)
    console.print(Panel(f"[bold #00f3ff]Total Cart Value: {total} TC[/bold #00f3ff]", title="[bold #00f3ff]Summary[/bold #00f3ff]", border_style="#00f3ff", box=ROUNDED, expand=False))
    return total

def get_recommendations():
    """Provide smart AI recommendations to the operator based on purchase history"""
    data = load_data()
    history = data.get("history", [])
    agents = data["agents"]
    
    if not history:
        recs = sorted(agents, key=lambda x: x["success_rate"], reverse=True)[:2]
    else:
        bought_ids = {item["id"] for item in history}
        recommended = [a for a in agents if a["id"] not in bought_ids]
        recs = recommended[:2] if recommended else agents[:2]
        
    log_action("SYSTEM", f"Generated {len(recs)} AI recommendations for operator.")
    return recs

def top_up_tokens():
    """Token top-up feature with validation for name, Saudi mobile number (^05[0-9]{8}$), and bank card (16 digits)"""
    data = load_data()
    current_tokens = data.get("tokens", 0)
    
    console.print(Panel(f"[bold #00f3ff]💳 Your Current Balance:[/bold #00f3ff] [bold #ffb700]{current_tokens} TC[/bold #ffb700]", title="[bold #00f3ff]Token Wallet Top-Up Portal[/bold #00f3ff]", border_style="#00f3ff", box=ROUNDED, expand=False))
    
    name = questionary.text("Full Name:", style=CYBERPUNK_STYLE).ask()
    if not name or not name.strip():
        console.print(Panel("[bold red]❌ Invalid Name! Name cannot be empty. Top-up canceled.[/bold red]", title="[bold red]Validation Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
        log_action("WARNING", "Top-up attempt failed due to empty operator name.")
        return
        
    mobile = questionary.text("Saudi Mobile Number (e.g. 05XXXXXXXX):", style=CYBERPUNK_STYLE).ask()
    if not mobile or not re.match(r"^05[0-9]{8}$", mobile.strip()):
        console.print(Panel("[bold red]❌ Invalid Saudi Mobile Number! Must start with '05' followed by 8 digits (e.g., 0512345678). Top-up canceled.[/bold red]", title="[bold red]Validation Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
        log_action("WARNING", "Top-up attempt failed due to invalid Saudi mobile number format.")
        return
        
    card_number = questionary.text("Bank Card Number (16 digits):", style=CYBERPUNK_STYLE).ask()
    if not card_number or not card_number.isdigit() or len(card_number) != 16:
        console.print(Panel("[bold red]❌ Invalid Bank Card Number! Must be exactly 16 numeric digits. Top-up canceled.[/bold red]", title="[bold red]Validation Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
        log_action("WARNING", "Top-up attempt failed due to invalid bank card number format.")
        return
        
    amount_str = questionary.text("Enter Token amount to top-up (e.g. 1000):", style=CYBERPUNK_STYLE).ask()
    if not amount_str or not amount_str.isdigit() or int(amount_str) <= 0:
        console.print(Panel("[bold red]❌ Invalid token amount entered. Top-up canceled.[/bold red]", title="[bold red]Error[/bold red]", border_style="red", box=ROUNDED, expand=False))
        log_action("WARNING", "Top-up attempt failed due to invalid token amount.")
        return
        
    amount = int(amount_str)
    data["tokens"] = current_tokens + amount
    save_data(data)
    
    ref_id = f"TOPUP-{random.randint(1000,9999)}"
    masked_card = f"****-****-****-{card_number[-4:]}"
    
    create_encrypted_receipt(
        ref_id,
        f"Wallet Top-Up ({name.strip()})",
        f"+{amount} TC",
        receipt_type="TOKEN TOP-UP",
        extra_data={
            "full_name": name.strip(),
            "saudi_mobile": mobile.strip(),
            "card_masked": masked_card
        }
    )
    
    log_action("TRANSACTION", f"Wallet top-up successful: +{amount} TC added by {name.strip()} (Mobile: {mobile.strip()}). New balance: {data['tokens']} TC")
    
    success_banner = (
        f"[bold #00ff66]🎉 TOKEN RECHARGE SUCCESSFUL! 🎉[/bold #00ff66]\n\n"
        f"[bold white]Full Name:[/bold white] [bold #00f3ff]{name.strip()}[/bold #00f3ff]\n"
        f"[bold white]Saudi Mobile:[/bold white] [bold #00f3ff]{mobile.strip()}[/bold #00f3ff]\n"
        f"[bold white]Bank Card:[/bold white] [bold #ffb700]{masked_card}[/bold #ffb700]\n"
        f"[bold white]Amount Added:[/bold white] [bold #00ff66]+{amount} TC[/bold #00ff66]\n"
        f"[bold white]New Wallet Balance:[/bold white] [bold #ffb700]{data['tokens']} TC[/bold #ffb700]\n\n"
        f"[dim]Reference ID: {ref_id} │ Securely Logged & Encrypted[/dim]"
    )
    
    console.print(Panel(
        success_banner,
        title="[bold #00ff66]💳 RECHARGE SECURED[/bold #00ff66]",
        border_style="#00ff66",
        box=ROUNDED,
        expand=False
    ))

def redeem_promo_code():
    """Redeem discount coupons/promo codes (e.g., 'GRAD2026', 'CYBER100', 'VIP2026') to add bonus credits to wallet."""
    data = load_data()
    if "redeemed_codes" not in data:
        data["redeemed_codes"] = []
        
    console.print(Panel(
        "[bold #00f3ff]🎟️ [AgentOSا] PROMO CODE REDEMPTION PORTAL[/bold #00f3ff]\n"
        "[dim]Enter valid promotional codes to inject bonus tokens directly into your wallet.[/dim]\n"
        "[bold #ffb700]💡 Hint: Try codes like 'GRAD2026', 'CYBER100', 'AGENTOS500', or 'VIP2026'[/bold #ffb700]",
        title="[bold #00f3ff]Promo Code Hub[/bold #00f3ff]",
        border_style="#00f3ff",
        box=ROUNDED,
        expand=False
    ))
    
    code = questionary.text("Enter Promo Code:", style=CYBERPUNK_STYLE).ask()
    if not code:
        return
        
    clean_code = code.strip().upper()
    
    promo_rewards = {
        "GRAD2026": 1000,
        "CYBER100": 500,
        "AGENTOS500": 500,
        "OGB500": 500,
        "VIP2026": 2000
    }
    
    if clean_code not in promo_rewards:
        console.print(Panel(
            f"[bold red]❌ INVALID PROMO CODE: '{code}'[/bold red]\n"
            "[dim]The code entered does not exist or has expired in the neural registry.[/dim]",
            title="[bold red]Redemption Failed[/bold red]",
            border_style="red",
            box=ROUNDED,
            expand=False
        ))
        log_action("WARNING", f"Attempted to redeem invalid promo code: '{code}'")
        return
        
    if clean_code in data["redeemed_codes"]:
        console.print(Panel(
            f"[bold #ffb700]⚠️ PROMO CODE ALREADY REDEEMED[/bold #ffb700]\n"
            f"[dim]You have already claimed the reward for '{clean_code}'. Each code can only be used once per operator.[/dim]",
            title="[bold #ffb700]Already Claimed[/bold #ffb700]",
            border_style="#ffb700",
            box=ROUNDED,
            expand=False
        ))
        log_action("WARNING", f"Attempted to re-redeem already claimed promo code: '{clean_code}'")
        return
        
    bonus = promo_rewards[clean_code]
    data["tokens"] = data.get("tokens", 2000) + bonus
    data["redeemed_codes"].append(clean_code)
    save_data(data)
    create_encrypted_receipt(f"PROMO-{clean_code}", f"Promo Code Reward ({clean_code})", f"+{bonus} TC", receipt_type="PROMO BONUS")
    
    new_balance = data["tokens"]
    log_action("TRANSACTION", f"Promo code '{clean_code}' redeemed successfully. Bonus: +{bonus} TC. New balance: {new_balance} TC")
    
    success_banner = (
        f"[bold #00ff66]🎉 PROMO CODE SUCCESSFULLY REDEEMED! 🎉[/bold #00ff66]\n\n"
        f"[bold white]Redeemed Code:[/bold white] [bold #00f3ff]{clean_code}[/bold #00f3ff]\n"
        f"[bold white]Bonus Awarded:[/bold white] [bold #00ff66]+{bonus} TC[/bold #00ff66]\n"
        f"[bold white]New Wallet Balance:[/bold white] [bold #ffb700]{new_balance} TC[/bold #ffb700]\n\n"
        f"[dim]Credits have been securely injected into your account.[/dim]"
    )
    
    console.print(Panel(
        success_banner,
        title="[bold #00ff66]🏆 REWARD GRANTED[/bold #00ff66]",
        border_style="#00ff66",
        box=ROUNDED,
        expand=False
    ))

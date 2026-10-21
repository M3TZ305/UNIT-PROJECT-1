import sys
import os
os.environ["PROMPT_TOOLKIT_NO_WINDOWS_CONSOLE"] = "1"
import questionary
from core.database import load_data
from ui.animations import display_banner, show_deployment_animation, cyber_matrix_intro
from ui.menus import main_menu, display_agent_table, select_theme_menu
from ui.dashboard import display_live_dashboard
from services.store import search_agents, add_to_cart, remove_from_cart, list_cart, get_recommendations, top_up_tokens
from services.checkout import process_checkout, track_deployment_status
from services.manager import manager_dashboard
from rich.console import Console

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()

def run_app():
    display_banner()
    cyber_matrix_intro()
    
    while True:
        choice = main_menu()
        data = load_data()
        
        if choice == "🛒 Browse AI Agents Catalogue":
            display_agent_table(data["agents"])
            agent_id = questionary.text("Enter Agent ID to add to cart (or press Enter to go back):").ask()
            if agent_id:
                add_to_cart(agent_id.strip())
                
        elif choice == "🔍 Search for an Agent":
            query = questionary.text("Enter search keyword (name or specialty):").ask()
            if query:
                results = search_agents(query)
                if results:
                    display_agent_table(results)
                    agent_id = questionary.text("Enter Agent ID to add to cart (or press Enter):").ask()
                    if agent_id:
                        add_to_cart(agent_id.strip())
                else:
                    console.print("[yellow]No agents found matching your query.[/yellow]")
                    
        elif choice == "💡 Get AI Recommendations":
            recs = get_recommendations()
            console.print("\n[bold cyan]✨ Recommended AI Agents For Your Next Deployment:[/bold cyan]")
            display_agent_table(recs)
            agent_id = questionary.text("Enter Agent ID to add to cart (or press Enter):").ask()
            if agent_id:
                add_to_cart(agent_id.strip())
                
        elif choice == "📊 View Live System Dashboard":
            display_live_dashboard()
                
        elif choice == "🛍️ View My Cart & Checkout":
            total = list_cart()
            if total > 0:
                sub_choice = questionary.select(
                    "Cart Actions:",
                    choices=["Proceed to Checkout", "Remove an Item", "Back to Main Menu"]
                ).ask()
                
                if sub_choice == "Proceed to Checkout":
                    endpoint = questionary.text("Enter Target Endpoint / IP Address for deployment:").ask()
                    if endpoint:
                        success = process_checkout(endpoint.strip())
                        if success:
                            show_deployment_animation("Purchased Cluster Agents")
                elif sub_choice == "Remove an Item":
                    item_id = questionary.text("Enter Agent ID to remove from cart:").ask()
                    if item_id:
                        remove_from_cart(item_id.strip())
                        
        elif choice == "💳 Top-Up Wallet Tokens":
            top_up_tokens()
            
        elif choice == "🎨 Switch Terminal Theme":
            select_theme_menu()
            
        elif choice == "📦 Track Deployment Status":
            track_deployment_status()
            
        elif choice == "⚙️ [Manager Portal] Manage Agents & Stock":
            manager_dashboard()
            
        elif choice == "🚪 Exit" or choice is None:
            console.print("[bold cyan]Exiting AI Orchestration Grid. Goodbye![/bold cyan]")
            break
        
        console.print("\n" + "─" * 80 + "\n")

if __name__ == "__main__":
    run_app()

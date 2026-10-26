import sys
import os
import time
os.environ["PROMPT_TOOLKIT_NO_WINDOWS_CONSOLE"] = "1"
import questionary
from core.database import load_data
from core.logger import display_audit_logs
from ui.animations import cinematic_startup_sequence, show_deployment_animation, smooth_menu_transition, clear_screen, cinematic_exit, CYBERPUNK_STYLE
from ui.menus import main_menu, display_agent_table, select_theme_menu
from ui.dashboard import display_live_dashboard
from ui.dashboard_matrix import run_live_matrix_dashboard
from services.store import search_agents, add_to_cart, remove_from_cart, list_cart, get_recommendations, top_up_tokens, redeem_promo_code
from services.checkout import process_checkout, track_deployment_status, view_purchase_history
from services.manager import manager_dashboard
from services.sandbox import launch_sandbox
from services.minigame import run_hacking_minigame
from services.export import export_data_to_csv
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()

def run_app():
    # Cinematic startup sequence
    cinematic_startup_sequence()
    
    # Smooth transition to main menu
    smooth_menu_transition("[AgentOS] Main Grid")
    
    while True:
        choice = main_menu()
        data = load_data()
        
        if choice == "🖥️  Live Split-Screen Dashboard Matrix":
            smooth_menu_transition("Live Split-Screen Matrix")
            run_live_matrix_dashboard()
                
        elif choice == "🛒  Browse AI Agents Catalogue":
            smooth_menu_transition("AI Catalogue")
            display_agent_table(data["agents"])
            console.print("[dim]Press Enter to return to menu[/dim]\n")
            while True:
                agent_id = questionary.text("Enter Agent ID to add to cart:", style=CYBERPUNK_STYLE).ask()
                if not agent_id or not agent_id.strip():
                    break
                success = add_to_cart(agent_id.strip())
                if success:
                    break
                time.sleep(1.2)
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
                
        elif choice == "🔍  Search for an Agent":
            smooth_menu_transition("Agent Search Engine")
            while True:
                clear_screen()
                smooth_menu_transition("Agent Search Engine")
                console.print("[dim]Press Enter to return to menu[/dim]\n")
                query = questionary.text("Enter search keyword (name or specialty):", style=CYBERPUNK_STYLE).ask()
                if not query or not query.strip():
                    break
                results = search_agents(query.strip())
                if results:
                    display_agent_table(results)
                    console.print("[dim]Press Enter to return to menu[/dim]\n")
                    while True:
                        agent_id = questionary.text("Enter Agent ID to add to cart:", style=CYBERPUNK_STYLE).ask()
                        if not agent_id or not agent_id.strip():
                            break
                        success = add_to_cart(agent_id.strip())
                        if success:
                            break
                        time.sleep(1.2)
                    break
                else:
                    console.print(Panel("[bold #ffb700]No agents found matching your query.[/bold #ffb700]", title="[bold #ffb700]Search Notice[/bold #ffb700]", border_style="#ffb700", box=ROUNDED, expand=False))
                    time.sleep(1.2)
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
                    
        elif choice == "💡  Get AI Recommendations":
            smooth_menu_transition("Neural Recommendation Hub")
            recs = get_recommendations()
            console.print("\n[bold #00f3ff]✨ Recommended AI Agents For Your Next Deployment:[/bold #00f3ff]")
            display_agent_table(recs)
            console.print("[dim]Press Enter to return to menu[/dim]\n")
            while True:
                agent_id = questionary.text("Enter Agent ID to add to cart:", style=CYBERPUNK_STYLE).ask()
                if not agent_id or not agent_id.strip():
                    break
                success = add_to_cart(agent_id.strip())
                if success:
                    break
                time.sleep(1.2)
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
                
        elif choice == "🎨 ASCII Glitch Restorer (Mini-Game)":
            smooth_menu_transition("ASCII Glitch Restorer Terminal")
            run_hacking_minigame()
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
                
        elif "Test AI Model" in choice:
            smooth_menu_transition("AI Agent Sandbox Playground")
            launch_sandbox()
                
        elif choice == "📊  View Live System Dashboard":
            smooth_menu_transition("Live System Dashboard")
            display_live_dashboard()
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
                
        elif choice == "📋  View System Audit Logs":
            smooth_menu_transition("System Audit Logs")
            display_audit_logs()
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
                
        elif choice == "📁  Export Data Report to CSV":
            smooth_menu_transition("CSV Data Exporter")
            export_data_to_csv()
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
                
        elif choice == "🛍️  View My Cart & Checkout":
            smooth_menu_transition("Shopping Cart & Checkout")
            total = list_cart()
            if total > 0:
                sub_choice = questionary.select(
                    "Cart Actions:",
                    choices=["Proceed to Checkout", "Remove an Item", "Back to Main Menu"],
                    style=CYBERPUNK_STYLE
                ).ask()
                
                if sub_choice == "Proceed to Checkout":
                    while True:
                        clear_screen()
                        smooth_menu_transition("Shopping Cart & Checkout")
                        list_cart()
                        console.print("[dim]Press Enter to return to menu[/dim]\n")
                        endpoint = questionary.text("Enter Target Endpoint / IP Address for deployment:", style=CYBERPUNK_STYLE).ask()
                        if not endpoint or not endpoint.strip():
                            break
                        success = process_checkout(endpoint.strip())
                        if success:
                            show_deployment_animation("Purchased Cluster Agents")
                            break
                        time.sleep(1.2)
                elif sub_choice == "Remove an Item":
                    while True:
                        clear_screen()
                        smooth_menu_transition("Shopping Cart & Checkout")
                        list_cart()
                        console.print("[dim]Press Enter to return to menu[/dim]\n")
                        item_id = questionary.text("Enter Agent ID to remove from cart:", style=CYBERPUNK_STYLE).ask()
                        if not item_id or not item_id.strip():
                            break
                        success = remove_from_cart(item_id.strip())
                        if success:
                            break
                        time.sleep(1.2)
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
                
        elif choice == "💳  Top-Up Wallet Tokens":
            smooth_menu_transition("Token Wallet Top-Up")
            top_up_tokens()
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
            
        elif "Redeem Promo Code" in choice:
            smooth_menu_transition("Promo Code Redemption Hub")
            redeem_promo_code()
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
            
        elif choice == "🎨  Switch Terminal Theme":
            smooth_menu_transition("Terminal Theme Engine")
            select_theme_menu()
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
            
        elif choice == "📦  Track Deployment Status":
            smooth_menu_transition("Cluster Deployment Status")
            track_deployment_status()
            console.input("\n[dim]Press Enter to return to menu...[/dim]")
            
        elif choice == "⚙️  Manager Portal":
            smooth_menu_transition("Manager Administrator Portal")
            manager_dashboard()
            
        elif choice == "🚪  Exit" or choice is None:
            cinematic_exit()
            break

if __name__ == "__main__":
    run_app()

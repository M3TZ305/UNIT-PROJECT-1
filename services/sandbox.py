import time
import questionary
from core.database import load_data
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_agent_sandbox():
    """ساحة اختبار وتجربة الوكلاء الذكيين محلياً وبشكل تفاعلي ذكي"""
    data = load_data()
    history = data.get("history", [])
    
    if not history:
        console.print("[yellow]⚠️ You haven't deployed any AI Agents yet! Buy an agent first to unlock the Sandbox.[/yellow]")
        return

    choices = [f"{item['id']} - {item['name']} ({item['specialty']})" for item in history]
    choices.append("🔙 Return to Main Menu")
    
    selected = questionary.select(
        "🧪 Select a deployed AI Agent to test in the Sandbox:",
        choices=choices
    ).ask()
    
    if not selected or selected == "🔙 Return to Main Menu":
        return
        
    selected_id = selected.split(" - ")[0]
    agent = next((a for a in history if a["id"] == selected_id), None)
    
    if not agent:
        return

    console.print(Panel(
        f"[bold cyan]🤖 Connected to {agent['name']} Live AI Sandbox[/bold cyan]\n"
        f"[dim]Specialty: {agent['specialty']} | Success Rate: {agent['success_rate']}%[/dim]\n"
        f"[yellow]Type your prompt/command to execute on the agent (or 'exit' to quit):[/yellow]",
        border_style="cyan"
    ))

    while True:
        prompt = questionary.text(f"[{agent['name']} Prompt] >").ask()
        
        if not prompt or prompt.lower().strip() == "exit":
            console.print(f"[dim]Disconnecting from {agent['name']} Sandbox...[/dim]")
            break
            
        with console.status(f"[bold green]🧠 {agent['name']} is processing neural prompt...[/bold green]", spinner="dots"):
            time.sleep(1.0) # محاكاة وقت التفكير البشري
            
        # توليد رد ذكي بناءً على إدخال المستخدم وتخصص الوكيل
        user_input_lower = prompt.lower()
        if "hi" in user_input_lower or "hello" in user_input_lower or "مرحبا" in user_input_lower:
            ai_output = f"Hello Operator! As {agent['name']}, I am fully online and ready to assist you with {agent['specialty']} tasks."
        elif "code" in user_input_lower:
            ai_output = f"[{agent['name']}] Analyzing code syntax... All structures are optimized for high-performance deployment."
        else:
            ai_output = f"[{agent['name']}] Successfully analyzed query: '{prompt}'. Executing specialized protocols for {agent['specialty']} with 99.8% precision."
        
        console.print(Panel(
            f"[bold white]{ai_output}[/bold white]",
            title=f"[bold green]🤖 {agent['name']} Output[/bold green]",
            border_style="green"
        ))
        console.print()

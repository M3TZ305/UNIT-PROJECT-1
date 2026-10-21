import time
import questionary
from core.database import load_data
from rich.console import Console
from rich.panel import Panel

console = Console()

# محاكاة الاستجابات الذكية بناءً على تخصص الوكيل
AGENT_RESPONSES = {
    "Architecture": "[DeepCode-V4] 🏗️ Analyzing repository structural patterns...\n>> Suggested Refactoring: Convert monolithic dependencies into modular clean packages.",
    "Cyber Defense": "[SecGuard-X] 🛡️ Scanning target network for CVE vulnerabilities...\n>> Threat Status: Zero critical vulnerabilities detected. Firewall grid active.",
    "Analytics": "[DataVision-Pro] 📊 Aggregating multi-source token usage trends...\n>> Insights: High efficiency detected in batch GPU allocations.",
    "Content Generation": "[NeuralWriter] ✍️ Generating optimized technical summary...\n>> Output: System operating at optimal neural throughput with minimal latency."
}

def run_agent_sandbox():
    """ساحة اختبار وتجربة الوكلاء الذكيين المشتراة حياً"""
    data = load_data()
    history = data.get("history", [])
    
    if not history:
        console.print("[yellow]⚠️ You haven't deployed any AI Agents yet! Buy an agent first to unlock the Sandbox.[/yellow]")
        return

    # استخراج قائمة الأسماء المتاحة في السجل
    choices = [f"{item['id']} - {item['name']} ({item['specialty']})" for item in history]
    choices.append("🔙 Return to Main Menu")
    
    selected = questionary.select(
        "🧪 Select a deployed AI Agent to test in the Sandbox:",
        choices=choices
    ).ask()
    
    if not selected or selected == "🔙 Return to Main Menu":
        return
        
    # معرفة الوكيل المختار
    selected_id = selected.split(" - ")[0]
    agent = next((a for a in history if a["id"] == selected_id), None)
    
    if not agent:
        return

    console.print(Panel(
        f"[bold cyan]🤖 Connected to {agent['name']} Sandbox Environment[/bold cyan]\n"
        f"[dim]Specialty: {agent['specialty']} | Success Rate: {agent['success_rate']}%[/dim]\n"
        f"[yellow]Type your prompt/command to execute on the agent (or 'exit' to quit):[/yellow]",
        border_style="cyan"
    ))

    while True:
        prompt = questionary.text(f"[{agent['name']} Prompt] >").ask()
        
        if not prompt or prompt.lower().strip() == "exit":
            console.print(f"[dim]Disconnecting from {agent['name']} Sandbox...[/dim]")
            break
            
        # محاكاة التفكير والتوليد للـ AI
        with console.status(f"[bold green]🧠 {agent['name']} is processing prompt...[/bold green]", spinner="dots"):
            time.sleep(1.2)
            
        # جلب الاستجابة بناءً على التخصص
        response = AGENT_RESPONSES.get(
            agent['specialty'], 
            f"[{agent['name']}] Successfully processed prompt: '{prompt}'. Executed with 100% accuracy."
        )
        
        console.print(Panel(
            f"[bold white]{response}[/bold white]",
            title="[bold green]🤖 AI Output[/bold green]",
            border_style="green"
        ))
        console.print()

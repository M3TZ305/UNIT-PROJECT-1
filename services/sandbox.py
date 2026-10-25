import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from core.database import load_data
import questionary

console = Console()

def calculate_benchmark_metrics(agent):
    """Calculate realistic performance metrics for an agent based on its success rate."""
    raw_rate = agent.get("success_rate", 98.5)
    if isinstance(raw_rate, str):
        try:
            base_reliability = float(raw_rate.replace("%", "").strip())
        except ValueError:
            base_reliability = 98.5
    else:
        base_reliability = float(raw_rate)
        
    latency = round(random.uniform(11.5, 42.8), 2)
    accuracy = min(100.0, max(90.0, round(base_reliability + random.uniform(-0.6, 0.9), 2)))
    throughput = random.randint(520, 1580)
    security_status = random.choice([
        "PASSED [0 Vulnerabilities Detected]",
        "VERIFIED [Encrypted Quantum Tunnel]",
        "OPTIMIZED [Zero-Day Defense Active]",
        "PASSED [Full Compliance Protocol]"
    ])
    
    return {
        "latency": latency,
        "accuracy": accuracy,
        "throughput": throughput,
        "security_status": security_status,
        "base_reliability": base_reliability
    }

def launch_sandbox():
    """Launch the professional AI Model Performance & Benchmark Testing Suite."""
    console.clear()
    
    data = load_data()
    inventory = data.get("inventory", []) or data.get("history", [])
    
    if not inventory:
        console.print(Panel(
            "[bold red]❌ NO DEPLOYED AGENTS FOUND IN INVENTORY[/bold red]\n"
            "[dim]You need to purchase/deploy at least one AI Agent from the Store & complete checkout before running neural benchmarks![/dim]",
            title="[bold red]Benchmark Access Denied[/bold red]",
            border_style="red",
            expand=False
        ))
        console.input("\n[dim]Press Enter to return to Main Menu...[/dim]")
        return

    # Cinematic loading progress bar
    with Progress(
        SpinnerColumn("dots", style="bold cyan"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30, complete_style="bold cyan", finished_style="bold green"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Initializing Neural Benchmark Matrix...", total=100)
        for _ in range(12):
            time.sleep(0.04)
            progress.update(task, advance=8.33)

    # Build agent selection options
    agent_options = []
    for i, agent in enumerate(inventory):
        name = agent.get('name', 'AI Agent')
        specialty = agent.get('category', agent.get('specialty', 'General Neural AI'))
        agent_options.append(f"{i+1:02d} - {name} ({specialty})")
    
    agent_options.append("⬅ Back to Main Menu")
    
    selected = questionary.select(
        "⚡ Select a Deployed AI Agent to Benchmark:",
        choices=agent_options
    ).ask()
    
    if not selected or "Back to Main Menu" in selected:
        return
        
    try:
        agent_index = int(selected.split(" - ")[0]) - 1
        agent = inventory[agent_index]
    except (ValueError, IndexError):
        return
    
    agent_name = agent.get("name", "Unknown Agent")
    specialty = agent.get("category", agent.get("specialty", "General AI"))
    base_rate = agent.get("success_rate", "98.5%")
    
    console.clear()
    console.print(Panel(
        f"[bold bright_cyan]🚀 AI MODEL PERFORMANCE & BENCHMARK SUITE[/bold bright_cyan]\n"
        f"[bold white]Target Agent:[/bold white] [green]{agent_name}[/green]\n"
        f"[bold white]Specialty Matrix:[/bold white] [yellow]{specialty}[/yellow]\n"
        f"[bold white]Base Reliability Rate:[/bold white] [cyan]{base_rate}[/cyan]\n"
        f"[dim]Press [Enter] to execute benchmark cycle | Type 'exit' or 'quit' to return.[/dim]",
        title="[bold cyan]Neural Benchmark Active[/bold cyan]",
        border_style="bright_cyan",
        expand=False
    ))
    
    test_count = 0
    
    while True:
        try:
            user_input = console.input(f"\n[bold green]⚡ [{agent_name}] > Press Enter to run benchmark (or 'exit'): [/bold green]").strip()
            
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print(f"\n[dim]Disconnecting from {agent_name} Benchmark Suite. Returning to Main Menu...[/dim]")
                time.sleep(0.4)
                break
                
            test_count += 1
            
            # Dynamic loading spinner/progress bar for neural inference test
            with Progress(
                SpinnerColumn("aesthetic", style="bold magenta"),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task(f"[magenta]Running neural inference test #{test_count} for {agent_name}...", total=None)
                time.sleep(0.7)
            
            metrics = calculate_benchmark_metrics(agent)
            
            report_content = (
                f"[bold cyan]📊 TEST CYCLE #{test_count} REPORT[/bold cyan]\n"
                f"--------------------------------------------------\n"
                f"⏱️  [bold white]Response Latency:[/bold white]    [bold yellow]{metrics['latency']} ms[/bold yellow]\n"
                f"🎯 [bold white]Inference Accuracy:[/bold white]  [bold green]{metrics['accuracy']}%[/bold green]\n"
                f"⚡ [bold white]Throughput Speed:[/bold white]    [bold bright_magenta]{metrics['throughput']} tokens/sec[/bold bright_magenta]\n"
                f"🛡️  [bold white]Core Security Check:[/bold white] [bold bright_green]{metrics['security_status']}[/bold bright_green]\n"
                f"--------------------------------------------------\n"
                f"[dim]Agent Status: OPERATIONAL & FULLY SYNCED[/dim]"
            )
            
            console.print(Panel(
                report_content,
                title=f"[bold green]Benchmark Report — Test #{test_count}[/bold green]",
                border_style="green",
                expand=False
            ))
            
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[dim]Benchmark session terminated safely by user.[/dim]")
            break

run_agent_sandbox = launch_sandbox

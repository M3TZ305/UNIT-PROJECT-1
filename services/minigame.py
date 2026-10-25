import os
import time
import random
import msvcrt
from core.database import load_data, save_data
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from rich.text import Text
from rich.box import ROUNDED

console = Console()

BASE_ART = [
    "   █████╗  ██████╗ ███████╗   ",
    "  ██╔══██╗██╔════╝ ██╔════╝   ",
    "  ███████║██║  ███╗█████╗     ",
    "  ██╔══██║██║   ██║██╔══╝     ",
    "  ██║  ██║╚██████╔╝███████╗   ",
    "   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   "
]

def run_ascii_glitch_restorer():
    """ASCII Glitch Restorer: Visual artwork restoration mini-game using Rich Live and Arrow keys."""
    try:
        console.print(Panel(
            "[bold #00f3ff]🎨 ASCII GLITCH RESTORER // PROTOCOL 🎨[/bold #00f3ff]\n"
            "[bold #ffb700]Move your repair scanner [bold]🟩[/bold] across the glitched AI canvas using [bold]Arrow Keys[/bold].\n"
            "Restore corrupted pixels back to original art to achieve 100% integrity within [bold]15 seconds[/bold].\n"
            "Press [bold red]Q[/bold] to abort at any time.[/bold #ffb700]",
            title="[bold #ffb700]🖼️ RESTORATION ARENA INTRO[/bold #ffb700]",
            border_style="#ffb700",
            box=ROUNDED
        ))
        console.input("\n[bold #00ff66]Press Enter to launch ASCII Glitch Restorer...[/bold #00ff66]")
        
        target_grid = [list(row) for row in BASE_ART]
        height = len(target_grid)
        width = len(target_grid[0])
        
        glitched_grid = [row[:] for row in target_grid]
        glitch_chars = ['X', '#', '?', '$', '%', '&', '@']
        
        glitch_coords = []
        for r in range(height):
            for c in range(width):
                if target_grid[r][c] != ' ':
                    if random.random() < 0.45:
                        glitched_grid[r][c] = random.choice(glitch_chars)
                        glitch_coords.append((r, c))
                        
        total_glitches = len(glitch_coords)
        if total_glitches == 0:
            glitched_grid[2][5] = 'X'
            glitch_coords.append((2, 5))
            total_glitches = 1
            
        fixed_count = 0
        cursor_r = 0
        cursor_c = 0
        
        start_time = time.time()
        duration = 15.0
        
        with Live(console=console, refresh_per_second=15, transient=True) as live:
            while True:
                elapsed = time.time() - start_time
                time_left = max(0.0, duration - elapsed)
                
                restored_pct = int((fixed_count / total_glitches) * 100) if total_glitches > 0 else 100
                
                if time_left <= 0 or restored_pct >= 100:
                    break
                    
                while msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    if ch in ('\x00', '\xe0'):
                        arrow = msvcrt.getwch()
                        if arrow == 'H':
                            cursor_r = max(0, cursor_r - 1)
                        elif arrow == 'P':
                            cursor_r = min(height - 1, cursor_r + 1)
                        elif arrow == 'K':
                            cursor_c = max(0, cursor_c - 1)
                        elif arrow == 'M':
                            cursor_c = min(width - 1, cursor_c + 1)
                    else:
                        if ch.lower() == 'q':
                            break
                            
                if (cursor_r, cursor_c) in glitch_coords:
                    if glitched_grid[cursor_r][cursor_c] != target_grid[cursor_r][cursor_c]:
                        glitched_grid[cursor_r][cursor_c] = target_grid[cursor_r][cursor_c]
                        fixed_count += 1
                        
                frame_lines = []
                frame_lines.append(f" ⏱️ Time Left: {time_left:4.1f}s  │  🎨 Integrity Restored: [bold #00ff66]{restored_pct}%[/bold #00ff66]")
                frame_lines.append("═" * (width + 4))
                
                for r in range(height):
                    row_str = ""
                    for c in range(width):
                        if r == cursor_r and c == cursor_c:
                            row_str += "[bold #ffb700]█[/bold #ffb700]"
                        else:
                            ch_char = glitched_grid[r][c]
                            if ch_char == target_grid[r][c] and ch_char != ' ':
                                row_str += f"[bold #00ff66]{ch_char}[/bold #00ff66]"
                            elif ch_char != ' ':
                                row_str += f"[bold red]{ch_char}[/bold red]"
                            else:
                                row_str += " "
                    frame_lines.append(f"  {row_str}  ")
                    
                frame_lines.append("═" * (width + 4))
                frame_lines.append(" Controls: [Arrow Keys] Move Scanner  │  [Q] Abort ")
                
                panel_render = Panel(
                    "\n".join(frame_lines),
                    title="[bold #00f3ff]🎨 ASCII GLITCH RESTORER // LIVE CANVAS[/bold #00f3ff]",
                    border_style="#00f3ff",
                    box=ROUNDED,
                    padding=(0, 1)
                )
                live.update(panel_render)
                
                time.sleep(0.06)
                
        final_pct = int((fixed_count / total_glitches) * 100) if total_glitches > 0 else 100
        earned_tokens = int(final_pct * 10)
        
        data = load_data()
        data["tokens"] = data.get("tokens", 0) + earned_tokens
        save_data(data)
        
        status_style = "#00ff66" if final_pct >= 80 else ("#ffb700" if final_pct >= 40 else "red")
        title_text = "🎉 ARTWORK RESTORATION SUCCESSFUL" if final_pct >= 80 else "⚡ RESTORATION PARTIAL"
        
        summary_panel = Panel(
            Align.center(Text.from_markup(
                f"[bold #00ff66]🚀 ASCII GLITCH RESTORATION COMPLETED![/bold #00ff66]\n\n"
                f"[bold #00f3ff]🎨 Final Integrity Restored:[/bold #00f3ff] [bold white]{final_pct}%[/bold white]\n"
                f"[bold #00f3ff]✨ Glitches Cleared:[/bold #00f3ff] [bold white]{fixed_count}/{total_glitches}[/bold white]\n"
                f"{'─'*45}\n"
                f"[bold #ffb700]💰 TOKENS CREDITED TO WALLET: +{earned_tokens} TC[/bold #ffb700]\n"
                f"[dim]Wallet synchronized with local database (data_store.json).[/dim]"
            )),
            title=f"[bold {status_style}]{title_text}[/bold {status_style}]",
            border_style=status_style,
            box=ROUNDED,
            padding=(1, 2)
        )
        console.print(summary_panel)
        time.sleep(1.5)
        return earned_tokens > 0

    except (KeyboardInterrupt, EOFError):
        console.print(Panel("[bold #ffb700]⚠️ ASCII Glitch Restorer aborted by Operator. Returning to main menu...[/bold #ffb700]", title="[bold #ffb700]Aborted[/bold #ffb700]", border_style="#ffb700", box=ROUNDED, expand=False))
        time.sleep(1.0)
        return False

def run_hacking_minigame():
    """Alias for backwards compatibility."""
    return run_ascii_glitch_restorer()

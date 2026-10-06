import subprocess
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def run_subdomain_scan(target, output_file=None, no_save=False):
    console.print(f"\n[bold cyan][▶] Starting Subdomain Enumeration for {target}...[/bold cyan]")
    
    subdomains = []
    
    # Run subfinder silently in the background
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Running Subfinder on {target}...", total=None)
            
            result = subprocess.run(
                ["subfinder", "-d", target, "-silent"],
                capture_output=True, text=True, timeout=120
            )
            
            if result.returncode == 0:
                subdomains = result.stdout.strip().split('\n')
                subdomains = [s for s in subdomains if s] # Remove empty lines
            else:
                console.print(f"[bold red][!] Subfinder failed: {result.stderr}[/bold red]")
                
    except FileNotFoundError:
        console.print("[bold red][!] Error: Subfinder is not installed or not in PATH.[/bold red]")
        return []
    except Exception as e:
        console.print(f"[bold red][!] An error occurred: {e}[/bold red]")
        return []

    # Display Results in a Beautiful Table
    if subdomains:
        console.print(f"\n[bold green][+] Found {len(subdomains)} subdomains![/bold green]\n")
        
        table = Table(title=f"Subdomains for {target}", border_style="bright_cyan", show_lines=False)
        table.add_column("#", style="dim", width=5)
        table.add_column("Subdomain", style="bold white")
        
        for i, sub in enumerate(subdomains, 1):
            table.add_row(str(i), sub)
            
        console.print(table)

        # Auto-Save Logic
        if not no_save:
            if not output_file:
                os.makedirs("reports", exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
                output_file = f"reports/{target}_{timestamp}_subdomains.txt"
            
            with open(output_file, "w") as f:
                for sub in subdomains:
                    f.write(f"{sub}\n")
            console.print(f"[bold green][+] Results saved to: {output_file}[/bold green]\n")
    else:
        console.print("[yellow][!] No subdomains found.[/yellow]\n")

    return subdomains

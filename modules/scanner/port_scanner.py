import subprocess
import re
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

def run_port_scan(target, output_file=None, no_save=False):
    console.print(f"\n[bold cyan][▶] Starting Port Scanning (Nmap) for {target}...[/bold cyan]")
    
    open_ports = []
    
    try:
        console.print("[yellow][*] Running Nmap (Top 50 Ports + Service Detection)...[/yellow]")
        # Using grepable output (-oG) for easy parsing
        result = subprocess.run(
            ["nmap", "-sV", "--top-ports", "50", "-oG", "-", target],
            capture_output=True, text=True, timeout=300
        )
        
        if result.returncode == 0:
            # Parse Nmap grepable output
            for line in result.stdout.split('\n'):
                if line.startswith('Ports:'):
                    # Example: Ports: 22/open/tcp//ssh//OpenSSH 7.6p1 Ubuntu 4ubuntu0.3/
                    ports_data = line.split('Ports: ')[1]
                    for port_info in ports_data.split(', '):
                        parts = port_info.split('/')
                        if len(parts) >= 2 and parts[1] == 'open':
                            port_num = parts[0]
                            service = parts[3] if len(parts) > 3 else 'unknown'
                            version = parts[4] if len(parts) > 4 else ''
                            open_ports.append({
                                "port": port_num,
                                "service": service,
                                "version": version
                            })
        else:
            console.print(f"[bold red][!] Nmap scan failed: {result.stderr}[/bold red]")
            
    except FileNotFoundError:
        console.print("[bold red][!] Error: Nmap is not installed.[/bold red]")
        return []
    except Exception as e:
        console.print(f"[bold red][!] An error occurred: {e}[/bold red]")
        return []

    # Display Results
    if open_ports:
        console.print(f"\n[bold green][+] Found {len(open_ports)} open ports![/bold green]\n")
        
        table = Table(title=f"Open Ports for {target}", border_style="bright_magenta", show_lines=False)
        table.add_column("Port", style="bold cyan", width=10)
        table.add_column("Service", style="bold white", width=20)
        table.add_column("Version", style="dim")
        
        for p in open_ports:
            table.add_row(p["port"], p["service"], p["version"])
            
        console.print(table)

        # Auto-Save Logic
        if not no_save:
            if not output_file:
                os.makedirs("reports", exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
                output_file = f"reports/{target}_{timestamp}_ports.txt"
            
            with open(output_file, "w") as f:
                for p in open_ports:
                    f.write(f"{p['port']}\t{p['service']}\t{p['version']}\n")
            console.print(f"[bold green][+] Port scan results saved to: {output_file}[/bold green]\n")
    else:
        console.print("[yellow][!] No open ports found in top 50.[/yellow]\n")

    return open_ports

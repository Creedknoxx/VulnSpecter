import subprocess
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

def run_vuln_scan(target, output_file=None, no_save=False):
    console.print(f"\n[bold cyan][▶] Starting Vulnerability Scanning (Nuclei) for {target}...[/bold cyan]")
    
    vulnerabilities = []
    
    try:
        console.print("[yellow][*] Running Nuclei (Default Templates)...[/yellow]")
        # Nuclei JSON output for easy parsing
        result = subprocess.run(
            ["nuclei", "-u", target, "-json", "-silent", "-timeout", "10"],
            capture_output=True, text=True, timeout=600
        )
        
        if result.returncode == 0:
            # Parse JSON lines output
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        vuln = json.loads(line)
                        vulnerabilities.append({
                            "name": vuln.get("info", {}).get("name", "Unknown"),
                            "severity": vuln.get("info", {}).get("severity", "INFO").upper(),
                            "template": vuln.get("template-id", "N/A"),
                            "url": vuln.get("matched-at", target)
                        })
                    except json.JSONDecodeError:
                        continue
        else:
            console.print(f"[bold red][!] Nuclei scan failed: {result.stderr}[/bold red]")
            
    except FileNotFoundError:
        console.print("[bold red][!] Error: Nuclei is not installed.[/bold red]")
        return []
    except Exception as e:
        console.print(f"[bold red][!] An error occurred: {e}[/bold red]")
        return []

    # Display Results
    if vulnerabilities:
        console.print(f"\n[bold red][!] Found {len(vulnerabilities)} vulnerabilities![/bold red]\n")
        
        table = Table(title=f"Vulnerabilities for {target}", border_style="bright_red", show_lines=True)
        table.add_column("Severity", style="bold", width=10)
        table.add_column("Name", style="bold white")
        table.add_column("Template", style="dim")
        
        # Color mapping for severity
        severity_colors = {
            "CRITICAL": "bold red",
            "HIGH": "red",
            "MEDIUM": "yellow",
            "LOW": "blue",
            "INFO": "cyan"
        }
        
        for v in vulnerabilities:
            color = severity_colors.get(v["severity"], "white")
            table.add_row(f"[{color}]{v['severity']}[/{color}]", v["name"], v["template"])
            
        console.print(table)

        # Auto-Save Logic
        if not no_save:
            if not output_file:
                os.makedirs("reports", exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
                output_file = f"reports/{target}_{timestamp}_vulns.json"
            
            with open(output_file, "w") as f:
                json.dump(vulnerabilities, f, indent=4)
            console.print(f"[bold green][+] Vulnerability results saved to: {output_file}[/bold green]\n")
    else:
        console.print("[bold green][+] No vulnerabilities found with default templates![/bold green]\n")

    return vulnerabilities

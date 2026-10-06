#!/usr/bin/env python3
# ============================================
# DEVELOPER INFO (Edit this section later)
# ============================================
# Author: [YOUR_NAME]
# Email: [YOUR_EMAIL]
# GitHub: https://github.com/Creedknoxx
# Version: 1.0.0
# Tool Name: VulnSpecter
# Codename: Vuln5p3c73r
# ============================================

import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich import box

# Import our custom modules
from utils.dependency_manager import DependencyManager

console = Console()
import ipaddress

def is_ip_address(target):
    """Check if the target is an IP address or a domain name."""
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False
BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║   VULNSPECTER v1.0.0                                          ║
║   Automated Security Testing Platform                         ║
║   Codename: Vuln5p3c73r                                       ║
╚═══════════════════════════════════════════════════════════════╝
"""

def print_banner():
    panel = Panel(
        BANNER,
        title="[bold red]VulnSpecter[/bold red]",
        subtitle="[bold italic cyan]v1.0.0 :: Vuln5p3c73r Edition[/bold italic cyan]",
        border_style="bright_magenta",
        box=box.DOUBLE_EDGE,
        padding=(1, 2)
    )
    console.print(panel)

def main():
    parser = argparse.ArgumentParser(
        description="VulnSpecter - Automated Recon, Vulnerability & Exploit Intelligence Platform"
    )
    
    # Arguments
    parser.add_argument('-t', '--target', type=str, help='Target Domain or IP (e.g., example.com)')
    parser.add_argument('--version', action='store_true', help='Show version')
    parser.add_argument('--check-deps', action='store_true', help='Show detailed dependency table')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output for installation')
    parser.add_argument('-o', '--output', type=str, help='Custom output file path')
    parser.add_argument('--no-save', action='store_true', help='Do not save results to a file')
    parser.add_argument('--scan-ports', action='store_true', help='Run Nmap port scan')
    parser.add_argument('--scan-vulns', action='store_true', help='Run Nuclei vulnerability scan')
    parser.add_argument('--exploit-intel', action='store_true', help='Map vulnerabilities to public exploits')
    parser.add_argument('--report', action='store_true', help='Generate final HTML report')
    args = parser.parse_args()
    
    # 1. Print Banner
    print_banner()

    # 2. Handle Version
    if args.version:
        console.print("[bold green]VulnSpecter v1.0.0 (Vuln5p3c73r Edition)[/bold green]")
        sys.exit(0)

    # 3. Initialize Dependency Manager
    dep_manager = DependencyManager()

    # 4. Handle Check Deps Mode
    if args.check_deps:
        dep_manager.show_dependency_table()
        sys.exit(0)

    # 5. Handle Missing Target
    if not args.target:
        console.print("[bold red][!][/bold red] Error: No target specified!")
        console.print("[yellow][*][/yellow] Usage: python3 main.py -t example.com")
        console.print("[yellow][*][/yellow] Use --check-deps to view system requirements.")
        sys.exit(1)

    # 6. Auto-Install Dependencies
    dep_manager.check_and_install(verbose=args.verbose)

    console.print("\n[bold green][+][/bold green] Environment verified successfully.")
    console.print(f"[bold green][+][/bold green] Target acquired: [bold cyan]{args.target}[/bold cyan]")
    
    # 7. Smart Target Detection & Recon
    if is_ip_address(args.target):
        console.print(f"[bold yellow][*] Target is an IP address. Skipping subdomain enumeration.[/bold yellow]")
        console.print(f"[bold yellow][*] Proceeding directly to port scanning...[/bold yellow]\n")
    else:
        from modules.recon.subdomain_scanner import run_subdomain_scan
        run_subdomain_scan(args.target, output_file=args.output, no_save=args.no_save)
    # 8. Run Scanners based on flags
    if args.scan_ports:
        from modules.scanner.port_scanner import run_port_scan
        run_port_scan(args.target, output_file=args.output, no_save=args.no_save)
        
    if args.scan_vulns:
        from modules.scanner.vuln_scanner import run_vuln_scan
        run_vuln_scan(args.target, output_file=args.output, no_save=args.no_save)
    # 9. Run Exploit Intelligence (if enabled and vulns were scanned)
    if args.exploit_intel and args.scan_vulns:
        from modules.scanner.vuln_scanner import run_vuln_scan
        from modules.exploit.exploit_mapper import run_exploit_intelligence
        
        console.print("[yellow][*] Re-running Nuclei to capture vulnerabilities for mapping...[/yellow]")
        vulns = run_vuln_scan(args.target, output_file=args.output, no_save=True)
        run_exploit_intelligence(vulns)
    # 10. Generate Final Report
    if args.report:
        from modules.reporting.html_reporter import generate_html_report
        generate_html_report(args.target)
    
    # 11. Auto-scan if no specific flags provided
    if not args.scan_ports and not args.scan_vulns:
        console.print("[yellow][*] No scan flags provided. Running default port scan...[/yellow]")
        from modules.scanner.port_scanner import run_port_scan
        run_port_scan(args.target, output_file=args.output, no_save=args.no_save)        
if __name__ == "__main__":
    main()

import platform
import shutil
import subprocess
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

console = Console()

class DependencyManager:
    def __init__(self):
        self.os_info = self._get_os_info()
        # Install commands with sudo for admin privileges
        self.tools = {
            "Nmap": {"cmd": "nmap", "install_cmd": "sudo apt-get install -y nmap"},
            "Subfinder": {"cmd": "subfinder", "install_cmd": "sudo apt-get install -y subfinder"},
            "Nuclei": {"cmd": "nuclei", "install_cmd": "sudo apt-get install -y nuclei"},
            "Metasploit": {"cmd": "msfconsole", "install_cmd": "sudo apt-get install -y metasploit-framework"},
            "Searchsploit": {"cmd": "searchsploit", "install_cmd": "sudo apt-get install -y exploitdb"}
        }

    def _get_os_info(self):
        system = platform.system()
        if system == "Linux":
            try:
                with open('/etc/os-release') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME'):
                            return line.split('=')[1].strip().strip('"')
            except Exception:
                pass
            return f"Linux {platform.release()}"
        return f"{system} {platform.release()}"

    def is_installed(self, cmd):
        """Check if tool is in standard PATH or common Go/Local bin paths."""
        if shutil.which(cmd):
            return True
        
        home = str(Path.home())
        extra_paths = [
            f"{home}/go/bin/{cmd}",
            f"{home}/.local/bin/{cmd}",
            f"/usr/local/go/bin/{cmd}"
        ]
        
        for path in extra_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return True
                
        return False

    def install_tool(self, tool_name, install_cmd):
        """Actually runs the installation command in the background."""
        try:
            # Run the command silently
            result = subprocess.run(
                install_cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if installation was successful
            if result.returncode == 0:
                return True
            else:
                console.print(f"[bold red]    → ️ Failed to install {tool_name}. Error: {result.stderr[:100]}[/bold red]")
                return False
                
        except Exception as e:
            console.print(f"[bold red]    → ️ Installation error for {tool_name}: {str(e)}[/bold red]")
            return False

    def check_and_install(self, verbose=False):
        """Silently checks and installs missing tools automatically."""
        missing_tools = [name for name, info in self.tools.items() if not self.is_installed(info["cmd"])]
        
        if not missing_tools:
            if verbose:
                console.print("[bold green][+][/bold green] All core dependencies are already installed.")
            return True

        if verbose or len(missing_tools) > 0:
            console.print(f"[bold yellow][!][/bold yellow] Found {len(missing_tools)} missing tools. Auto-installing...\n")

        success_count = 0
        for tool_name in missing_tools:
            cmd = self.tools[tool_name]["cmd"]
            install_cmd = self.tools[tool_name]["install_cmd"]
            
            console.print(f"[bold cyan][*][/bold cyan] Installing {tool_name}...")
            
            # Show a professional spinner while installing
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Setting up {tool_name}...", total=None)
                
                # ACTUAL INSTALLATION HAPPENS HERE
                is_success = self.install_tool(tool_name, install_cmd)
                
            if is_success:
                console.print(f"[bold green]    → ✅ {tool_name} installed successfully.[/bold green]")
                success_count += 1
            else:
                console.print(f"[bold red]    → ❌ {tool_name} installation failed.[/bold red]")
            
        if success_count == len(missing_tools):
            console.print(f"\n[bold green][+] All missing dependencies installed successfully![/bold green]\n")
        else:
            console.print(f"\n[bold yellow][!] Some dependencies failed to install. Please check manually.[/bold yellow]\n")
            
        return True

    def show_dependency_table(self):
        """Shows the detailed table only when --check-deps is used."""
        console.print("\n[bold yellow][*] Running detailed dependency check...[/bold yellow]\n")
        
        table = Table(
            title="System & Tool Status",
            border_style="bright_cyan",
            box=box.ROUNDED,
            show_lines=True
        )
        
        table.add_column("Component", style="bold white", width=20)
        table.add_column("Status", justify="center", width=15)
        table.add_column("Details / Path", style="dim", width=50)

        table.add_row("Operating System", "[bold green]DETECTED[/bold green]", self.os_info)
        table.add_row("Python", "[bold green]INSTALLED[/bold green]", f"Version: {platform.python_version()}")

        for tool_name, info in self.tools.items():
            is_installed = self.is_installed(info["cmd"])
            if is_installed:
                status = "[bold green]✅ INSTALLED[/bold green]"
                path_found = shutil.which(info['cmd'])
                if not path_found:
                    home = str(Path.home())
                    if os.path.exists(f"{home}/go/bin/{info['cmd']}"):
                        path_found = f"{home}/go/bin/{info['cmd']}"
                details = f"Found at: {path_found}" if path_found else "Installed"
            else:
                status = "[bold red]❌ MISSING[/bold red]"
                details = "Will be auto-installed during scan"
            
            table.add_row(tool_name, status, details)

        console.print(table)
        console.print("\n[bold green][+] Dependency Check Completed![/bold green]\n")

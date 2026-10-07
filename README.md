<p align="center">
  <img src="banner.png" alt="VulnSpecter Banner" width="100%">
</p>

# VulnSpecter (Vuln5p3c73r Edition)

**Automated Security Testing Platform**

## Overview
VulnSpecter is a professional-grade automated security testing tool designed for ethical hackers, penetration testers, and bug bounty hunters. It provides comprehensive reconnaissance, vulnerability scanning, and exploit intelligence in a single platform.

## Features
- **Smart Target Detection**: Automatically detects IP vs Domain and adjusts scanning strategy
- **Auto Dependency Management**: Checks and installs missing tools automatically
- **Subdomain Enumeration**: Powered by Subfinder
- **Port Scanning**: Nmap integration with service detection
- **Vulnerability Scanning**: Nuclei integration for CVE detection
- **Exploit Intelligence**: Maps vulnerabilities to Exploit-DB and Metasploit modules
- **Professional Reporting**: Generates HTML reports with dark theme

## Installation

### Prerequisites
- Python 3.10 or higher
- Kali Linux / Ubuntu / Debian (recommended)
- Internet connection for auto-installing system dependencies

### Quick Install
```bash
# Clone the repository
git clone https://github.com/CreedKnoxx/VulnSpecter.git
cd VulnSpecter

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the tool (system dependencies will auto-install)
python3 main.py --check-deps

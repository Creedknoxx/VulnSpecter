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
```bash
git clone https://github.com/Creedknoxx/VulnSpecter.git
cd VulnSpecter
python3 -m venv venv
source venv/bin/activate
pip install rich

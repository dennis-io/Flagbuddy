#!/usr/bin/env python3
import os
import time
import subprocess
from rich.console import Console
from xml.etree import ElementTree as ET
from rich.table import Table

# Create a console for rich output
console = Console()

def main():
    console.print(" Welcome to CTF Buddy! Let's start the enumeration... ", style="bold blue")
    target = input("Please enter the target IP: ")
    console.print(f" Target set to {target}. Initiating port scan... ", style="bold green")

    # Running Nmap command
    nmap_cmd = f'sudo nmap -p- -T4 -sV -oX scan.xml {target}'
    subprocess.run(nmap_cmd, shell=True)
    
    # Check for the existence of 'scan.xml' every 5 seconds, up to 5 minutes
    for _ in range(60):
        if os.path.isfile('scan.xml'):
            break
        time.sleep(5)
    else:
        console.print(" The Nmap command is taking too long. Please check your network connection and try again.", style="bold red")
        return
    
    console.print(" Nmap scan finished. Parsing results...", style="bold green")
    
    # Parse XML file
    try:
        tree = ET.parse("scan.xml")
        root = tree.getroot()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Port")
        table.add_column("Service")
        table.add_column("Product")

        for i in root.iter('port'):
            port = i.get('portid')
            service = i.find('service').get('name')
            product = i.find('service').get('product')
            table.add_row(port, service, product)

        console.print(table)

        # Hydra command
        if service == "ssh":
            console.print(" Detected SSH service. Suggesting Hydra command for brute-forcing:", style="bold yellow")
            console.print(f'hydra -l /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/wordlists/rockyou.txt -s {port} -t 4 -vV {target} ssh', style="bold cyan")

    except ET.ParseError:
        console.print(" There was an error while parsing the scan.xml file. Please try again.", style="bold red")
        return

    console.print(" Enumeration finished. Happy Hacking! ", style="bold blue")

if __name__ == "__main__":
    main()

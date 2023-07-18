#!/usr/bin/env python3

from xml.etree import ElementTree as ET
from rich.console import Console
from rich.table import Table
from rich import box
import subprocess
import os
import time

def main():
    console = Console()
    console.print("🚀 Welcome to CTF Buddy! Let's start the enumeration... 🕵", style="bold blue")

    target = console.input("Please enter the target IP: ")

    console.print(f"🏁 Target set to {target}. Initiating port scan... 🔍", style="bold blue")

    display_choice = console.input("How would you like to display the results? Type '1' for a simplified table, or '2' for full nmap output: ")

    # Run Nmap and parse the output
    nmap_command = f"nmap -p- -sV -sC -A -T4 -oX scan.xml {target}"
    os.system(f"{nmap_command} > /dev/null 2>&1")

    while not os.path.exists('scan.xml'):
        time.sleep(1)

    if display_choice == '1':
        tree = ET.parse("scan.xml")
        root = tree.getroot()

        # Create a table to display the scan results
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Port")
        table.add_column("State")
        table.add_column("Service")
        table.add_column("Product")
        table.add_column("Version")

        for host in root.findall("host"):
            for ports in host.findall("ports"):
                for port in ports.findall("port"):
                    table.add_row(
                        port.get("portid"), 
                        port.find("state").get("state"), 
                        port.find("service").get("name"),
                        port.find("service").get("product", "N/A"),
                        port.find("service").get("version", "N/A")
                    )
                    if port.find("service").get("name") == "ssh":
                        console.print(f"\n💡 Suggested Hydra command for SSH on {target}:{port.get('portid')}:")
                        console.print(f"hydra -l /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/wordlists/rockyou.txt -s {port.get('portid')} -t 4 -vV {target} ssh", style="bold green")

        console.print(table)

    elif display_choice == '2':
        with open('scan.xml') as f:
            console.print(f.read())
    
    else:
        console.print("Invalid choice. Please try again.", style="bold red")

if __name__ == "__main__":
    main()
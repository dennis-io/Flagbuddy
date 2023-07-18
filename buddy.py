#!/usr/bin/env python3

import os
import time
from xml.etree import ElementTree as ET

from rich import box
from rich.console import Console
from rich.table import Table

def main():
    # Check if the script is run as root
    if os.geteuid() != 0:
        exit("❗ This script must be run as root! This is required for the nmap scan to function correctly. Exiting.")

    console = Console()
    console.print("🚀 Welcome to CTF Buddy! Let's start the enumeration... 🕵️", style="bold blue")

    target = console.input("Please enter the target IP: ")

    console.print(f"🏁 Target set to {target}. Initiating port scan... 🔍", style="bold blue")

    # Run Nmap and parse the output
    nmap_command = f"nmap -p- -sV -T4 -oX scan.xml {target}"
    os.system(f"{nmap_command} > /dev/null 2>&1")

    while not os.path.exists('scan.xml'):
        time.sleep(1)

    tree = ET.parse("scan.xml")
    root = tree.getroot()

    # Create a table to display the scan results
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Port")
    table.add_column("State")
    table.add_column("Service")
    table.add_column("Product")
    table.add_column("Version")  # Added version column

    for host in root.findall("host"):
        for ports in host.findall("ports"):
            for port in ports.findall("port"):
                table.add_row(
                    port.get("portid"), 
                    port.find("state").get("state"), 
                    port.find("service").get("name"),
                    port.find("service").get("product", "N/A"),
                    port.find("service").get("version", "N/A")  # Added version
                )
                if port.find("service").get("name") == "ssh":
                    console.print(f"\n💡 Suggested Hydra command for SSH on {target}:{port.get('portid')}:")
                    console.print(f"hydra -l /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/wordlists/rockyou.txt -s {port.get('portid')} -t 4 -vV {target} ssh", style="bold green")

    console.print(table)

if __name__ == "__main__":
    main()

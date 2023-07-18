from rich.console import Console
from rich.table import Table
from rich.progress import track
import xml.etree.ElementTree as ET
from subprocess import run, PIPE
import requests
import time

console = Console()

def main():
    console.print("🚀 Welcome to CTF Buddy! Let's start the enumeration... 🕵️", style="bold blue")

    target = console.input("Please enter the target IP: ")

    with console.status("[bold yellow]Running Nmap on the target... 🕐", spinner="aesthetic") as status:
        command = ["nmap", "-sc", "-sv", "-A", "-p-", "-oX", "scan.xml", target]
        run(command, stdout=PIPE, stderr=PIPE)

    tree = ET.parse("scan.xml")
    root = tree.getroot()

    console.print("💡 Nmap Scan Summary 💡", style="bold magenta")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("IP", style="dim", width=12)
    table.add_column("Port", style="dim", width=12)
    table.add_column("Service", style="dim")
    table.add_column("Product", style="dim")
    table.add_column("Version", style="dim")

    for elem in root.iter('host'):
        for item in elem.iter('port'):
            service = item.find('service')
            ip = item.get('addr')
            port = item.get('portid')
            service_name = service.get('name')
            product = service.get('product')
            version = service.get('version')
            table.add_row(ip, port, service_name, product, version)

    console.print(table)

    console.print("🔐 SSH Brute Force Recommendations 🔐", style="bold magenta")

    for elem in root.iter('host'):
        for item in elem.iter('port'):
            if item.find('service').get('name') == 'ssh':
                console.print(f"Hydra command for SSH on {target}:{item.get('portid')}:", style="bold yellow")
                console.print(f"hydra -l /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/wordlists/rockyou.txt -s {item.get('portid')} -t 4 -vV {target} ssh", style="bold green")

if __name__ == '__main__':
    main()

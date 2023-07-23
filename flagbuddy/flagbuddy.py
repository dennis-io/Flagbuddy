import json
import nmap
import logging
import ipaddress
from colorama import Fore, Style

# Set up logging
logging.basicConfig(filename='flagbuddy.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

HIGH_PRIORITY_SERVICES = ['http', 'https', 'ssh', 'ftp', 'telnet', 'smtp', 'pop3', 'imap', 'dns', 'mysql', 'mssql', 'oracle', 'postgresql', 'rdp', 'vnc', 'smb']

def run_nmap(ip):
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments='-sC -sV -p-')
        open_ports = [int(port) for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open']
        services = {int(port): nm[ip]['tcp'][port]['name'] for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open'}
        versions = {int(port): nm[ip]['tcp'][port]['version'] for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open'}
        return open_ports, services, versions
    except Exception as e:
        logging.error(f"Error running nmap scan: {e}")
        print(f"Error running nmap scan: {e}")
        return [], {}, {}

def load_advice(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading advice file {filename}: {e}")
        print(f"Error loading advice file {filename}: {e}")
        return {}

def validate_ip(ip):
    try:
        return ipaddress.ip_address(ip)
    except ValueError:
        print("Invalid IP address.")
        raise  # Re-raise the exception

def main():
    while True:
        ip_input = input("Enter the target IP: ")
        try:
            ip = validate_ip(ip_input)
            break  # Exit the loop if the IP address is valid
        except ValueError:
            continue  # Just continue to the next iteration of the loop
    ip = str(ip)  # Convert IP address back to string
    logging.info(f"Running nmap scan on {ip}...")
    print(f"Running nmap scan on {ip}...")
    open_ports, services, versions = run_nmap(ip)
    print(f"Open ports: {open_ports}")
    port_advice = load_advice('port_advice.json')
    service_advice = load_advice('service_advice.json')
    high_priority_ports = [port for port in open_ports if services.get(port) in HIGH_PRIORITY_SERVICES]
    low_priority_ports = [port for port in open_ports if port not in high_priority_ports]
    view_all = input("Do you want to view all advice at once? (y/n): ").lower() == 'y'
    for port in high_priority_ports + low_priority_ports:
        service = services.get(port)
        version = versions.get(port)
        advice = service_advice.get(service) or port_advice.get(str(port))
        if advice:
            print(f"\n{Fore.GREEN}Advice for port {port} ({service}):{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Tool: {advice['tool']}{Style.RESET_ALL}")
            if isinstance(advice['command'], list):
                print("Commands:")
                for command in advice['command']:
                    print(f"- {command.replace('<ip>', ip)}")
            else:
                print(f"Command: {advice['command'].replace('<ip>', ip)}")
            print(f"{Fore.CYAN}Explanation: {advice['explanation']}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}No advice for port {port} ({service}).{Style.RESET_ALL}")
        if version:
            print(f"Version: {version}")
        if not view_all:
            user_input = input("Press Enter to continue to next port or 'q' to quit: ")
            if user_input.lower() == 'q':
                break

if __name__ == "__main__":
    main()



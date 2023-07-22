import json
import nmap
from colorama import Fore, Style

# Define a list of high priority services to be used later
HIGH_PRIORITY_SERVICES = ['ftp', 'telnet', 'http', 'https', 'ssh', 'rdp', 'smb']

# Define a function to run an nmap scan on a given IP address
def run_nmap(ip):
    # Create a new nmap PortScanner object
    nm = nmap.PortScanner()
    # Run an nmap scan on the given IP address with the arguments '-sC -sV'
    nm.scan(ip, arguments='-sC -sV')
    # Get a list of open ports from the nmap scan
    open_ports = [int(port) for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open']
    # Get a dictionary of services running on open ports from the nmap scan
    services = {int(port): nm[ip]['tcp'][port]['name'] for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open'}
    # Get a dictionary of versions for services running on open ports from the nmap scan
    versions = {int(port): nm[ip]['tcp'][port]['version'] for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open'}
    # Return the open ports, services, and versions
    return open_ports, services, versions

# Define a function to load advice from a JSON file
def load_advice(filename):
    with open(filename) as f:
        return json.load(f)

# Define the main function
def main():
    # Prompt the user to enter a target IP address
    ip = input("Enter the target IP: ")
    # Print a message indicating that an nmap scan is being run on the target IP address
    print(f"Running nmap scan on {ip}...")
    # Run an nmap scan on the target IP address
    open_ports, services, versions = run_nmap(ip)
    # Print a list of open ports found by the nmap scan
    print(f"Open ports: {open_ports}")
    # Load advice for ports and services from JSON files
    port_advice = load_advice('port_advice.json')
    service_advice = load_advice('service_advice.json')
    # Separate open ports into high and low priority lists based on the services running on them
    high_priority_ports = [port for port in open_ports if services.get(port) in HIGH_PRIORITY_SERVICES]
    low_priority_ports = [port for port in open_ports if port not in high_priority_ports]
    # Prompt the user to choose whether to view all advice at once or not
    view_all = input("Do you want to view all advice at once? (y/n): ").lower() == 'y'
    # Loop through each open port and print advice and version information if available
    for port in high_priority_ports + low_priority_ports:
        # Get the service running on the current port
        service = services.get(port)
        # Get the version for the service running on the current port
        version = versions.get(port)
        # Get advice for the service running on the current port, or advice for the port if no service advice is available
        advice = service_advice.get(service) or port_advice.get(str(port))
        # If advice is available, print it along with the tool to use, the command to run, and an explanation of the advice
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
        # If no advice is available, print a message indicating that there is no advice for the current port
        else:
            print(f"\n{Fore.YELLOW}No advice for port {port} ({service}).{Style.RESET_ALL}")
        # If a version is available, print it
        if version:
            print(f"Version: {version}")
        # If the user does not want to view all advice at once, prompt them to continue to the next port or quit
        if not view_all:
            user_input = input("Press Enter to continue to next port or 'q' to quit: ")
            if user_input.lower() == 'q':
                break

# Call the main function if this script is being run as the main module
if __name__ == "__main__":
    main()
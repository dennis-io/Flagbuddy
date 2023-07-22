import json
import nmap

def run_nmap(ip):
    nm = nmap.PortScanner()
    nm.scan(ip, arguments='-sC -sV -p-')
    open_ports = [int(port) for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open']
    services = {int(port): nm[ip]['tcp'][port]['name'] for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open'}
    versions = {int(port): nm[ip]['tcp'][port]['version'] for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open'}
    return open_ports, services, versions


def load_advice(filename):
    with open(filename) as f:
        return json.load(f)

def main():
    ip = input("Enter the target IP: ")
    print(f"Running nmap scan on {ip}...")
    open_ports, services, versions = run_nmap(ip)
    print(f"Open ports: {open_ports}")
    port_advice = load_advice('port_advice.json')
    service_advice = load_advice('service_advice.json')
    for port in open_ports:
        service = services.get(port)
        version = versions.get(port)
        advice = service_advice.get(service) or port_advice.get(str(port))
        if advice:
            print(f"\nAdvice for port {port} ({service}):")
            print(f"Tool: {advice['tool']}")
            if isinstance(advice['command'], list):
                print("Commands:")
                for command in advice['command']:
                    print(f"- {command.replace('<ip>', ip)}")
            else:
                print(f"Command: {advice['command'].replace('<ip>', ip)}")
            print(f"Explanation: {advice['explanation']}")
        else:
            print(f"\nNo advice for port {port} ({service}).")
        if version:
            print(f"Version: {version}")

if __name__ == "__main__":
    main()


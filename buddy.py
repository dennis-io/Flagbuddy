#!/usr/bin/env python3
# buddy.py

import os
import subprocess
import xml.etree.ElementTree as ET
import socket
import sys

def is_root():
    return os.geteuid() == 0

def perform_nmap_scan(target_ip):
    # Generate a unique filename for the XML output
    xml_output_file = f"nmap_{target_ip}_scan.xml"

    # Run Nmap and suppress output
    nmap_command = f"nmap -sC -sV -A -p- -oX {xml_output_file} {target_ip}"
    try:
        subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the Nmap scan:")
        print(e.output.decode())
        sys.exit(1)

    return xml_output_file

def parse_nmap_output(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for host in root.findall('host'):
        ip = host.find('address').get('addr')
        print(f"\nHost: {ip}\nPort | Protocol | Service | Version")
        print("-----------------------------------------")
        for port in host.iter('port'):
            protocol = port.get('protocol')
            portid = port.get('portid')
            service = port.find('service').get('name')
            version = port.find('service').get('product')
            print(f"{portid} | {protocol} | {service} | {version}")

        print("\n")

def suggest_hydra_commands(nmap_file):
    tree = ET.parse(nmap_file)
    root = tree.getroot()

    for host in root.findall('host'):
        ip = host.find('address').get('addr')
        for port in host.iter('port'):
            service = port.find('service').get('name')
            if service == 'ssh':
                print(f"Hydra command for SSH on {ip}:{port.get('portid')}:")
                print(f"hydra -l /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/wordlists/rockyou.txt -s {port.get('portid')} -t 4 -vV {ip} ssh")

def main():
    if not is_root():
        print("This script must be run with sudo privileges as Nmap often requires them for its scanning capabilities.")
        sys.exit(1)
        
    target_ip = input("Enter target IP: ")

    try:
        socket.inet_aton(target_ip)
    except socket.error:
        print("Invalid IP address.")
        sys.exit(1)

    xml_file = perform_nmap_scan(target_ip)
    parse_nmap_output(xml_file)
    suggest_hydra_commands(xml_file)

    # Optional: remove the XML file after we're done
    os.remove(xml_file)

if __name__ == "__main__":
    main()

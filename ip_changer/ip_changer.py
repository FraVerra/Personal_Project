'''
Autore: Verra Francesco

'''

import subprocess
import random
import sys
import time
'''
def write_ip_in_file(current_ip):
    try:
        file = open("file_creati/ip_default.txt","r")
        print("\n[*] Correctly entered in the file")
        
    except FileNotFoundError:
        file = open("file_creati/ip_default.txt","w")
        print("[*] File correctly created")
    lines = file.readlines()
    print(lines[0])
    file.close()

def read_ip_from_file()
'''
def extract_ip(text):
    parts = text.replace("(", "").replace(")", "").split()
    for p in parts:
        if p.count(".") == 3 and all(x.isdigit() for x in p.split(".")):
            return p
    return None


def octects_division(ip_address):
    octects = ip_address.split(".")
    return octects

def ip_converter(octects):
    binary_octects = []
    for data in octects:
        int_value = int(data)
        octects = f"{int_value:08b}"
        binary_octects.append(octects)

    final_result = ".".join(binary_octects)
    return final_result

def binary_to_decimal(binary_ip):
    octects = octects_division(binary_ip)
    decimal_ip = []
    for octect in octects:
        decimal_value = str(int(octect, 2))
        decimal_ip.append(decimal_value)
    return ".".join(decimal_ip)

def from_number_to_string(number):
    return f"{number}"

def from_ip_to_number(ip_address):
    octets = octects_division(ip_address)
    number = 0
    for octet in octets:
        number = number * 256 + int(octet)
    return number

def from_number_to_ip(number):
    octets = []
    for _ in range(4):
        octets.insert(0, str(number % 256))
        number //= 256
    return ".".join(octets)

def random_ip_generator(min_ip, max_ip, diz):
    max_ip_number = from_ip_to_number(max_ip)
    min_ip_number = from_ip_to_number(min_ip)
    correct = False
    while not correct:
        new_ip = random.randint(int(min_ip_number), int(max_ip_number))
        if new_ip not in diz:
            correct = True
    return from_number_to_ip(new_ip)

def ip_plus_subnet(random_ip, subnet_mask):
    return (f"{random_ip}/{subnet_mask}")

def function_command_status(command, ok_message, failure_message, decision):
    execution = subprocess.run(command, capture_output=True, text=True, check=True)
    if execution.returncode == 0:
        print(ok_message)
        if decision:
            return execution
    else:
        print(failure_message)
        print("[*] Closing the program")
        sys.exit()

def broadcast_ip_generator(binary_ip, subnet_mask):
    broad_ip = []
    cont = 0
    for data in binary_ip:
        if data != ".":
            if cont >= int(subnet_mask):
                broad_ip.append("1")
            else:
                broad_ip.append(data)
            cont+=1
        else:
            broad_ip.append(data)
    return "".join(broad_ip)

def network_ip_generator(binary_ip, subnet_mask):
    net_ip = []
    cont = 0
    for data in binary_ip:
        if data != ".":
            if cont >= int(subnet_mask):
                net_ip.append("0")
            else:
                net_ip.append(data)
            cont+=1
        else:
            net_ip.append(data)
    return "".join(net_ip)

def command_execution(gateway_IP, network_interface, current_ip_address, current_subnet_mask, ip_address_plus_subnet_mask, random_ip):
    #-------------
    disable_network_manager = ["sudo", "nmcli", "dev", "set", network_interface, "managed", "no"]
    disable_network_manager_ok_m = "[+] Network Manager correctly disabled"
    disable_network_manager_fail_m = "[-] Fatal error during Network Manager disconnection"
    function_command_status(disable_network_manager, disable_network_manager_ok_m, disable_network_manager_fail_m, False)
    time.sleep(1)
    #------------
    disable_network_interface = ["sudo", "ip", "link", "set", "dev", network_interface, "down"]
    disable_network_interface_ok_m = "[+] Network Interface correctly disabled"
    disable_network_interface_fail_m = "[-] Fatal error during Network Interface disconnection"
    function_command_status(disable_network_interface, disable_network_interface_ok_m, disable_network_manager_fail_m, False)
    time.sleep(1)
    #--------------
    delete_every_ip = ["sudo", "ip", "addr", "flush", "dev", network_interface]
    delete_every_ip_ok_m = "[+] Old IP addresses correctly deleted"
    delete_every_ip_fail_m = "[-] Fatal error during deleting old IP addresses"
    function_command_status(delete_every_ip, delete_every_ip_ok_m, delete_every_ip_fail_m, False)
    time.sleep(1)
    #------------
    new_ip_address = ["sudo", "ip", "addr", "add", random_ip, "dev", network_interface]
    new_ip_address_ok_m = "[+] New IP address has been correctly added"
    new_ip_address_fail_m = "[-] Fatal error in adding new IP address"
    function_command_status(new_ip_address, new_ip_address_ok_m, new_ip_address_fail_m, False)
    time.sleep(1)
    #--------------
    enable_network_interface = ["sudo", "ip", "link", "set", "dev", network_interface, "up"]
    enable_network_interface_ok_m = "[+] Network Interface successfully turned on"
    enable_network_interface_fail_m = "[-] Fatal error while turning on Network Interface"
    function_command_status(enable_network_interface, enable_network_interface_ok_m, enable_network_interface_fail_m, False)
    time.sleep(5)
    #--------------
    enable_network_manager = ["sudo", "nmcli", "dev", "set", network_interface, "managed", "yes"]
    enable_network_manager_ok_m = "[+] Successfully enabled network manager"
    enable_network_manager_fail_m = "[-] Fatal error while turning On network manager"
    function_command_status(enable_network_manager, enable_network_manager_ok_m, enable_network_manager_fail_m, False)
    time.sleep(5)
    #--------------
    setting_gateway = ["sudo", "ip", "route", "add", "default", "via", gateway_IP, "dev", network_interface]
    setting_gateway_ok_m = "[+] Gateway successfully initialized"
    setting_gateway_fail_m = "[-] Fatal error while initializing the Gateway"
    function_command_status(setting_gateway, setting_gateway_ok_m, setting_gateway_fail_m, False)
    time.sleep(5)
    #---------------
    delete_old_IP = ["sudo","ip","addr","del",ip_address_plus_subnet_mask,"dev",network_interface]
    delete_old_IP_ok_m = "[+] Successfully deleted old secondary IP address!"
    delete_old_IP_fail_m = "[-] Warning: Failed to delete old secondary IP address."
    function_command_status(delete_old_IP, delete_old_IP_ok_m, delete_old_IP_fail_m, False)
    time.sleep(2)
    
    print("[+] Successfully changed the IP address!")

def show_ip_informations(return_option):

    gateway_IP = None
    network_interface = None
    current_ip_address = None
    current_subnet_mask = None
    ip_address_plus_subnet_mask = None

    gateway_informations = []
    ip_informations = []
    parts = []
    hosts_in_the_network = []
    octects = []

    read_gateway = subprocess.run(["sudo","ip","route","show","default"], capture_output=True, text=True, check=True)
    #print(read_gateway.stdout) 
    gateway_informations = read_gateway.stdout.split(" ")
    gateway_IP = gateway_informations[2]
    network_interface = gateway_informations[4]
    print("\n")
    print(f"[*] Current Gateway address: {gateway_IP}")
    print(f"[*] Current Network Interface: {network_interface}")

    ip_a = subprocess.run(["ip","a"], capture_output=True, text=True, check=True)
    #print(ip_a.stdout)
    ip_informations = ip_a.stdout.split("\n")
    #print(ip_informations)
    for line in ip_informations:
        line = line.strip()
        if "inet" in line and network_interface in line:
            parts = line.split(" ")
            ip_address_plus_subnet_mask = parts[1]
            current_ip_address = parts[1].split("/")[0]
            current_subnet_mask = parts[1].split("/")[-1]
            binary_octects = ip_converter(octects_division(current_ip_address))
            binary_broadcast_ip = broadcast_ip_generator(binary_octects, current_subnet_mask)
            broadcast_ip = binary_to_decimal(binary_broadcast_ip)
            print(f"[*] Current IP address: {current_ip_address} ({binary_octects})")
            print(f"[*] Current Broadcast IP: {broadcast_ip} ({binary_broadcast_ip})")
            print(f"[*] Current subnet mask: /{current_subnet_mask}\n")

    if return_option == True:
        return gateway_IP, network_interface, current_ip_address, current_subnet_mask, ip_address_plus_subnet_mask, broadcast_ip
    else:
        print("[*] For the function 'show_ip_informations' user decided to not return anything")


def scan_network_hosts(current_gateway, network_ip):
    diz = {}
    scanned_hosts = None
    lines_in_Nmap = []
    octects = []
    scanned_hosts_command = ["nmap","-sn", network_ip]
    scanned_hosts_ok_m = "[+] Correctly scanned all the hosts in the network"
    scanned_hosts_fail_m = "[-] Fatal error while scanning the hosts in the network"
    print("\n[~] Running Nmap tool, please wait...")
    scanned_hosts = function_command_status(scanned_hosts_command, scanned_hosts_ok_m, scanned_hosts_fail_m, True)
    #print(f"\n{scanned_hosts.stdout}")
    lines_in_Nmap = scanned_hosts.stdout.split("\n")
    for data in lines_in_Nmap:
        data = data.strip()
        if "Nmap scan report for" in data:
            hosts_ip = extract_ip(data)
            if hosts_ip != current_gateway:
                octects = octects_division(hosts_ip)
                diz[hosts_ip]=ip_converter(octects)
    return diz

def main():

    gateway_IP,network_interface,current_ip_address,current_subnet_mask,ip_address_plus_subnet_mask,broadcast_ip = show_ip_informations(True)
    
    octects_current_ip = octects_division(current_ip_address)
    network_ip_binary = network_ip_generator(ip_converter(octects_current_ip), current_subnet_mask)
    network_ip_dec = binary_to_decimal(network_ip_binary)
    network_ip_plus_subnet = ip_plus_subnet(network_ip_dec, int(current_subnet_mask))
    
    diz = scan_network_hosts(gateway_IP, network_ip_plus_subnet)
    print(diz)

    print(f"{octects_current_ip},{network_ip_binary},{network_ip_dec},{network_ip_plus_subnet},{broadcast_ip}")

    random_ip = random_ip_generator(network_ip_dec, broadcast_ip, diz)
    new_ip = ip_plus_subnet(random_ip, current_subnet_mask)
    

    command_execution(gateway_IP, network_interface, current_ip_address, current_subnet_mask,ip_address_plus_subnet_mask, new_ip)
    show_ip_informations(False)

if __name__ == "__main__":
    main()

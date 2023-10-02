import socket
import ipaddress
import whois
from tabulate import tabulate

def get_domain_info(domain):
    try:
        ip_addresses = [ipaddress.ip_address(ip) for ip in socket.gethostbyname_ex(domain)[2]]
        print(f"\nDomain Information for {domain}:")
        print(f"IP Addresses: {', '.join(map(str, ip_addresses))}")
        domain_info = whois.whois(domain)
        registrar = domain_info.registrar if isinstance(domain_info.registrar, list) else [domain_info.registrar]
        print(f"Registrar: {', '.join(map(str, registrar))}")
    except Exception as e:
        print(f"Error getting domain information: {str(e)}")

def get_service_name(port):
    service_mapping = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        443: 'HTTPS',
        8080: 'HTTP Proxy',
    }
    return service_mapping.get(port, 'Not Running')

def scan_port(hostname, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((hostname, port))
    sock.close()
    return result

def send_message(hostname, port, message, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((hostname, port))
            s.sendall(message.encode())
            data = s.recv(1024)
        print(f"Received response from port {port}: {data.decode()}")
        return data.decode()
    except socket.timeout:
        print(f"Timeout waiting for response from port {port}")
        return None
    except Exception as e:
        print(f"Error sending/receiving message to/from port {port}: {str(e)}")
        return None

def scan_ports_range(hostname, start_port, end_port, timeout):
    open_ports = []
    data = []
    print(f"\nScanning ports from {start_port} to {end_port} on {hostname} with a timeout of {timeout} seconds:")
    data.append(["Port", "Status", "Service"])
    for port in range(start_port, end_port + 1):
        result = scan_port(hostname, port, timeout)
        status = 'Open' if result == 0 else 'Closed'
        service_name = get_service_name(port)
        data.append([port, status, service_name])
        if result == 0:
            open_ports.append(port)
    print(tabulate(data, headers="firstrow"))
    return open_ports

def send_messages_or_check_another_domain(hostname, open_ports, timeout):
    table_data = []
    print("\nOptions:")
    print("1. Send messages/requests to open ports")
    print("2. Check another domain")
    print("3. Exit")
    option = input("Enter the option (1, 2, or 3): ")
    if option == '1':
        for port in open_ports:
            message_option = input(f"Do you want to send a message to port {port}? (Y/N): ").upper()
            if message_option == 'Y':
                message = input(f"Enter the message to send to port {port}: ")
                response = send_message(hostname, port, message, timeout)
                if response is not None:
                    print(f"Response from port {port}: {response}")
                else:
                    print(f"No response received from port {port} (timeout).")
            elif message_option != 'N':
                print(f"Invalid option for port {port}. Please enter Y or N.")
        option = input("Do you want to perform another scan? (Y/N): ").upper()
        if option == 'Y':
            return True
        elif option == 'N':
            return False
        else:
            print("Invalid option. Exiting.")
            return False
    elif option == '2':
        change_domain(timeout)
    elif option == '3':
        return False
    else:
        print("Invalid option. Please enter 1, 2, or 3.")

def send_message_to_specific_port(hostname, timeout):
    port = int(input("Enter the port to send a message to: "))
    message = input(f"Enter the message to send to port {port}: ")
    response = send_message(hostname, port, message, timeout)
    if response is not None:
        print(f"Response from port {port}: {response}")
    else:
        print(f"No response received from port {port} (timeout).")

def perform_domain_check(domain, timeout):
    get_domain_info(domain)
    print("\nChoose an option:")
    print("1. Scan common ports")
    print("2. Scan ports from wordlist")
    print("3. Scan custom ports range")
    print("4. Send message to specific port")
    print("5. Change domain")
    print("6. Exit")
    option = input("Enter the option (1, 2, 3, 4, 5, or 6): ")
    if option == '1':
        timeout = select_timeout()
        open_ports = scan_common_ports(domain, timeout)
        if open_ports:
            should_continue = send_messages_or_check_another_domain(domain, open_ports, timeout)
            if should_continue:
                perform_domain_check(domain, timeout)
        else:
            print("No open ports detected.")
            option = input("Do you want to perform another scan? (Y/N): ").upper()
            if option == 'Y':
                perform_domain_check(domain, timeout)
    elif option == '2':
        wordlist_filename = input("\nEnter the filename of the wordlist: ")
        timeout = select_timeout()
        open_ports = scan_wordlist_ports(domain, wordlist_filename, timeout)
        if open_ports:
            should_continue = send_messages_or_check_another_domain(domain, open_ports, timeout)
            if should_continue:
                perform_domain_check(domain, timeout)
        else:
            print("No open ports detected.")
            option = input("Do you want to perform another scan? (Y/N): ").upper()
            if option == 'Y':
                perform_domain_check(domain, timeout)
    elif option == '3':
        start_port = int(input("\nEnter the start port: "))
        end_port = int(input("Enter the end port: "))
        timeout = select_timeout()
        open_ports = scan_ports_range(domain, start_port, end_port, timeout)
        if open_ports:
            should_continue = send_messages_or_check_another_domain(domain, open_ports, timeout)
            if should_continue:
                perform_domain_check(domain, timeout)
        else:
            print("No open ports detected.")
            option = input("Do you want to perform another scan? (Y/N): ").upper()
            if option == 'Y':
                perform_domain_check(domain, timeout)
    elif option == '4':
        send_message_to_specific_port(domain, timeout)
        should_continue = input("Do you want to perform another scan? (Y/N): ").upper() == 'Y'
        if should_continue:
            perform_domain_check(domain, timeout)
    elif option == '5':
        change_domain(timeout)
    elif option == '6':
        return False
    else:
        print("Invalid option. Please enter 1, 2, 3, 4, 5, or 6.")

def change_domain(timeout):
    new_domain = input("Enter the new domain: ")
    perform_domain_check(new_domain, timeout)

def select_timeout():
    print("\nSelect the timeout (in seconds):")
    print("1. Quick scan (0.1 seconds)")
    print("2. Balanced scan (0.5 seconds)")
    print("3. Thorough scan (1.0 seconds)")
    selected_option = input("Enter the option number (1, 2, or 3): ")
    return 0.1 if selected_option == '1' else 0.5 if selected_option == '2' else 1.0

def scan_common_ports(hostname, timeout):
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 8080]
    open_ports = []
    data = []
    print(f"\nScanning common ports on {hostname} with a timeout of {timeout} seconds:")
    data.append(["Port", "Status", "Service"])
    for port in common_ports:
        result = scan_port(hostname, port, timeout)
        status = 'Open' if result == 0 else 'Closed'
        service_name = get_service_name(port)
        data.append([port, status, service_name])
        if result == 0:
            open_ports.append(port)
    print(tabulate(data, headers="firstrow"))
    return open_ports

def scan_wordlist_ports(hostname, wordlist_filename, timeout):
    open_ports = []
    data = []
    print(f"\nScanning ports from wordlist on {hostname} with a timeout of {timeout} seconds:")
    data.append(["Port", "Status", "Service"])
    try:
        with open(wordlist_filename, 'r') as file:
            wordlist = [int(line.strip()) for line in file]
            for port in wordlist:
                result = scan_port(hostname, port, timeout)
                status = 'Open' if result == 0 else 'Closed'
                service_name = get_service_name(port)
                data.append([port, status, service_name])
                if result == 0:
                    open_ports.append(port)
    except FileNotFoundError:
        print("Wordlist file not found.")
    print(tabulate(data, headers="firstrow"))
    return open_ports

def port_scanner():
    disclaimer = (
        "Port Scanner Tool - For Ethical and Educational Use Only\n"
        "Creator: Nicolas Poersch (GitHub: nicolaspoersch)\n"
        "By using this tool, you agree that you will use it for ethical and educational purposes only.\n"
        "Unauthorized or malicious use is strictly prohibited.\n"
    )
    print(disclaimer)
    user_agrees = input("Do you agree to use this tool ethically and educationally? (Type 'YES' to agree): ").upper()
    if user_agrees != 'YES':
        print("\nExiting...")
        return
    print("\nYou have agreed to use this tool ethically. Let's proceed.\n")
    domain = input("Enter the domain: ")
    perform_domain_check(domain, timeout=1.0)

if __name__ == "__main__":
    port_scanner()
    input("\nPress Enter to exit.")
import socket
from ping3 import ping
import nmap

# Function to get the local IP address
def get_local_ip():
    # Create a UDP socket using IPv4 addressing
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Attempt to connect to a non-existing IP and port
        # Forces the OS to assign a local IP address to the socket
        s.connect(('10.255.255.255', 1))
        # Get the local IP address assigned to the socket
        local_ip = s.getsockname()[0]
    except:
        # If any error occurs, fall back to the loopback IP '127.0.0.1'
        local_ip = '127.0.0.1'
    finally:
        # Close the socket, releasing the resources associated with it
        s.close()
    return local_ip

# Function to perform an Nmap scan on the target host
def scan_target_host(target_host):
    # Create an Nmap scanner object
    nm_scanner = nmap.PortScanner()
     # Perform a SYN scan on the target host, with OS detection (-O) and service version detection (-sV)
    # -sS: Perform a SYN scan (half-open scan)
    # -O:  Enable OS detection (may require root privileges)
    # -sV: Enable service version detection
    nm_scanner.scan(target_host, arguments='-sS -O -sV')
    # Print the scan result in CSV format (can be further processed or analyzed)
    print(nm_scanner.csv())

# Get the default local IP address
default_ip = get_local_ip()

# Prompt the user for the target host, using the default local IP if none is entered
target_host = input(f"Enter the target host (IP or domain, default is {default_ip}): ") or default_ip

# Send a ping request to the target host using the ping3 library
response_time = ping(target_host)

# Check if the target host is reachable (response_time is not None)
if response_time is not None:
    # Print a message with the target host and response time
    print(f"{target_host} is reachable, response time: {response_time} ms")
    # Perform the Nmap scan on the reachable target host
    scan_target_host(target_host)
else:
    # Print a message indicating that the target host is not reachable
    print(f"{target_host} is not reachable")

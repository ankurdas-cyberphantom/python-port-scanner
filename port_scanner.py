import socket
from datetime import datetime

Ip_addr = input("Enter IP address: ")
start_point = int(input("Enter start port number: "))
end_point = int(input("Enter end port number: "))

Scan_start_time = datetime.now()
print(f"\nScan started at: {Scan_start_time}")

open_ports = []

for port in range(start_point, end_point + 1):
    try:
        connections = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connections.settimeout(1)
        establish_connection = connections.connect_ex((Ip_addr, port))
        if establish_connection == 0:
            print(f"Port {port} is open")
            open_ports.append(port)
        connections.close()
    except KeyboardInterrupt:
        print("\nKeyboard interrupted!")
        break

if not open_ports:
    print("No open ports found in the given range.")

Scan_end_time = datetime.now()
print(f"Scan ended at: {Scan_end_time}")
print(f"Total time: {Scan_end_time - Scan_start_time}")
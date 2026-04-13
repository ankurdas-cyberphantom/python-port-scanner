import socket
import threading
import argparse
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False

try:
    from tabulate import tabulate
    TABULATE = True
except ImportError:
    TABULATE = False

lock = threading.Lock()
open_ports = []
scanned_count = 0

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    27017: "MongoDB"
}

def green(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}" if COLOR else text

def red(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}" if COLOR else text

def cyan(text):
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}" if COLOR else text

def yellow(text):
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}" if COLOR else text

def grab_banner(s):
    try:
        s.send(b"Hello\r\n")
        banner = s.recv(1024).decode(errors="ignore").strip()
        return banner[:100] if banner else "No banner"
    except:
        return "No banner"

def resolve_service(port):
    if port in COMMON_PORTS:
        return COMMON_PORTS[port]
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def scan_port(target, port, total):
    global scanned_count
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            service = resolve_service(port)
            banner = grab_banner(s)
            with lock:
                print(f"\r{green('[OPEN]')} Port {port:<6} | Service: {cyan(service):<15} | Banner: {banner}")
                open_ports.append((port, service, banner))
        s.close()
    except:
        pass
    finally:
        with lock:
            scanned_count += 1
            progress = int((scanned_count / total) * 40)
            bar = f"[{'#' * progress}{'.' * (40 - progress)}] {scanned_count}/{total}"
            print(f"\r{yellow('Scanning:')} {bar}", end="", flush=True)

def parse_ports(port_range):
    try:
        start, end = map(int, port_range.split("-"))
        if not (0 < start <= 65535 and 0 < end <= 65535 and start <= end):
            raise ValueError
        return start, end
    except:
        print(red("Invalid port range. Use format: 1-1000 (max 65535)"))
        sys.exit(1)

def resolve_host(target):
    try:
        ip = socket.gethostbyname(target)
        hostname = socket.gethostbyaddr(ip)[0] if ip == target else target
        return ip, hostname
    except socket.gaierror:
        print(red(f"Could not resolve host: {target}"))
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Advanced Python Port Scanner")
    parser.add_argument("-t", "--target",  default="127.0.0.1", help="Target IP or hostname")
    parser.add_argument("-p", "--ports",   required=True,       help="Port range e.g. 1-1000")
    parser.add_argument("-o", "--output",  help="Save results to CSV file")
    parser.add_argument("--threads",       type=int, default=100, help="Max concurrent threads (default: 100)")
    args = parser.parse_args()

    ip, hostname = resolve_host(args.target)
    start_port, end_port = parse_ports(args.ports)
    total = end_port - start_port + 1

    print(cyan("\n=== Advanced Python Port Scanner ==="))
    print(f"Target   : {green(ip)} ({hostname})")
    print(f"Range    : {start_port} - {end_port}  ({total} ports)")
    print(f"Threads  : {args.threads}")
    print(f"Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    start_time = datetime.now()

    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = [
                executor.submit(scan_port, ip, port, total)
                for port in range(start_port, end_port + 1)
            ]
            for _ in as_completed(futures):
                pass
    except KeyboardInterrupt:
        print(f"\n{red('Scan interrupted by user.')}")

    end_time = datetime.now()
    print(f"\n\n{cyan('--- Scan Summary ---')}")

    if open_ports:
        open_ports.sort(key=lambda x: x[0])
        if TABULATE:
            print(tabulate(open_ports, headers=["Port", "Service", "Banner"], tablefmt="simple"))
        else:
            for port, service, banner in open_ports:
                print(f"  {green(str(port)):<8} {service:<15} {banner}")
        print(f"\n{green(str(len(open_ports)))} open port(s) found.")
    else:
        print(red("No open ports found in the given range."))

    print(f"Time taken: {end_time - start_time}\n")

    if args.output:
        with open(args.output, "w") as f:
            f.write("port,service,banner\n")
            for port, service, banner in open_ports:
                f.write(f"{port},{service},{banner}\n")
        print(f"Results saved to {green(args.output)}")

if __name__ == "__main__":
    main()
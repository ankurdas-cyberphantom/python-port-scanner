# 🔍 CyberPhantom Port Scanner

A multithreaded Python port scanner with banner grabbing, service detection, colored output, and optional CSV export. Built for educational use and authorized penetration testing.

---

## ⚠️ Disclaimer

> This tool is intended **only for use on systems you own or have explicit written permission to test.**
> Unauthorized scanning is illegal under the Computer Fraud and Abuse Act (CFAA) and equivalent laws worldwide.
> The author is not responsible for any misuse.

---

## 📋 Features

- ⚡ Multithreaded scanning via `ThreadPoolExecutor`
- 🎯 Banner grabbing on open ports
- 🔎 Service detection (built-in map + `socket.getservbyport` fallback)
- 🌈 Colored terminal output (via `colorama`)
- 📊 Clean summary table (via `tabulate`)
- 💾 CSV export with headers
- 🖥️ Hostname resolution (IP ↔ hostname)
- 📈 Live progress bar during scan

---

## 🛠️ Requirements

**Python 3.6+**

Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install colorama tabulate
```

| Package | Purpose | Required? |
|---|---|---|
| `colorama` | Colored terminal output | Optional |
| `tabulate` | Formatted summary table | Optional |

> The scanner works without these — output just won't have colors or a table layout.

---

## 🚀 Usage

### Interactive mode (recommended for beginners)

```bash
python advanced_port_scanner.py
```

You'll be prompted to enter:

```
Enter target IP (default 127.0.0.1): 192.168.1.1
Enter port range (e.g. 1-1000): 1-1000
Max threads (default 100): 100
Save to file? (leave blank to skip): results.csv
```

### CLI / Argparse mode

```bash
python advanced_port_scanner.py -t <target> -p <start>-<end> [--threads N] [-o output.csv]
```

**Flags:**

| Flag | Long form | Description | Default | Required |
|---|---|---|---|---|
| `-t` | `--target` | Target IP address or hostname | `127.0.0.1` | No |
| `-p` | `--ports` | Port range in `start-end` format | — | **Yes** |
| `--threads` | `--threads` | Max concurrent threads | `100` | No |
| `-o` | `--output` | Save results to a `.csv` file | — | No |

**Examples:**

```bash
# Scan localhost ports 1–1000
python advanced_port_scanner.py -p 1-1000

# Scan a specific IP with custom thread count
python advanced_port_scanner.py -t 192.168.1.1 -p 1-65535 --threads 200

# Scan and save results to file
python advanced_port_scanner.py -t 10.0.0.5 -p 20-445 -o results.csv

# Scan using a hostname
python advanced_port_scanner.py -t scanme.nmap.org -p 1-100
```

---

## 📤 Output

### Terminal output (during scan)

```
=== Advanced Python Port Scanner ===
Target   : 127.0.0.1 (localhost)
Range    : 1 - 1000  (1000 ports)
Threads  : 100
Started  : 2025-01-15 22:34:01

[OPEN] Port 22     | Service: SSH            | Banner: OpenSSH_9.0
[OPEN] Port 80     | Service: HTTP           | Banner: No banner
[OPEN] Port 443    | Service: HTTPS          | Banner: No banner
```

### Summary table (after scan)

```
--- Scan Summary ---
Port    Service    Banner
------  ---------  ----------------
22      SSH        OpenSSH_9.0
80      HTTP       No banner
443     HTTPS      No banner

3 open port(s) found.
Time taken: 0:00:04.213
```

### CSV output (when `-o` is used)

```
port,service,banner
22,SSH,OpenSSH_9.0
80,HTTP,No banner
443,HTTPS,No banner
```

---

## 🗂️ Built-in Service Map

The scanner recognizes these common ports out of the box. Unknown ports fall back to `socket.getservbyport`.

| Port | Service |
|---|---|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 135 | RPC |
| 139 | NetBIOS |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8080 | HTTP-Alt |
| 8443 | HTTPS-Alt |
| 27017 | MongoDB |

---

## 📁 Project Structure

```
python-port-scanner/
│
├── advanced_port_scanner.py   # Advanced multithreaded scanner
├── port_scanner.py            # Original basic scanner
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🧠 How It Works

1. **Resolves** the target hostname to an IP (and reverse-resolves if possible)
2. **Spawns** a thread pool with `ThreadPoolExecutor` — avoids OS-level thread exhaustion from unlimited threading
3. **Each thread** attempts a TCP `connect_ex()` on its assigned port
4. **On success** — grabs the service name and sends a `Hello\r\n` probe to capture a banner
5. **Progress bar** updates live in the terminal as ports are scanned
6. **Results** are collected thread-safely via a `Lock`, sorted by port, and printed as a summary table

---

## 👤 Author

**CyberPhantom** — MCA Student | Cybersecurity Enthusiast | Bug Bounty Hunter

- HackerOne / Intigriti: `inti_youknowwhoiam_`
- HTB: Active VIP Member

---

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

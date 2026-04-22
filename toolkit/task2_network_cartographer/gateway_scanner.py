import argparse
import json
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


# ─────────────────────────────────────────────
# ARGUMENTS
# ─────────────────────────────────────────────

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TCP connect scanner with banner grabbing."
    )

    parser.add_argument("target", help="Target IP address")

    parser.add_argument(
        "--ports",
        default="1-1024",
        help="Port(s) to scan (e.g. 80, 1-1024, 22,80,443)"
    )

    parser.add_argument("--threads", type=int, default=50)
    parser.add_argument("--timeout", type=float, default=0.5)
    parser.add_argument("--output", default="scan.json")

    return parser.parse_args()


# ─────────────────────────────────────────────
# PORT PARSING
# ─────────────────────────────────────────────

def parse_port_input(port_str: str) -> list[int]:
    ports = []

    for part in port_str.split(","):
        part = part.strip()

        if "-" in part:
            start, end = part.split("-", 1)
            start, end = int(start), int(end)

            if start > end:
                raise ValueError("Invalid port range")

            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))

    return sorted(set(ports))


# ─────────────────────────────────────────────
# PORT CHECK
# ─────────────────────────────────────────────

def check_port(target: str, port: int, timeout: float) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.settimeout(timeout)
        return sock.connect_ex((target, port)) == 0
    finally:
        sock.close()


# ─────────────────────────────────────────────
# BANNER GRABBING
# ─────────────────────────────────────────────

def grab_banner(target: str, port: int, timeout: float) -> str:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))

        time.sleep(0.5)
        banner = sock.recv(1024).decode("utf-8", errors="ignore")
        sock.close()

        return banner.strip()

    except Exception:
        return ""


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main() -> None:
    args = parse_arguments()

    # Validate ports
    try:
        ports = parse_port_input(args.ports)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    open_ports = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {
            executor.submit(check_port, args.target, p, args.timeout): p
            for p in ports
        }

        for future in futures:
            port = futures[future]

            if future.result():
                banner = grab_banner(args.target, port, args.timeout)
                open_ports.append({
                    "port": port,
                    "banner": banner
                })

    open_ports.sort(key=lambda x: x["port"])

    output = {
        "target": args.target,
        "open_ports": open_ports
    }

    print(json.dumps(output, indent=2))
    Path(args.output).write_text(json.dumps(output, indent=2))

    print(f"[*] {len(open_ports)} port(s) found.", file=sys.stderr)


if __name__ == "__main__":
    main()
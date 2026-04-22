import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

# Regex patterns
FAILED_PASSWORD = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"|[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})"
    r".*?Failed password for (?:invalid user )?"
    r"(?P<username>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)

INVALID_USER = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"|[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})"
    r".*?[Ii]nvalid user (?P<username>\S+) (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)

PATTERNS = [
    ("sshd", "failed_password", FAILED_PASSWORD),
    ("sshd", "invalid_user", INVALID_USER),
]


def normalize_timestamp(raw: str) -> str:
    if raw[0].isdigit():
        return raw[:19]

    cleaned = " ".join(raw.split())
    try:
        dt = datetime.strptime(cleaned, "%b %d %H:%M:%S")
        return dt.replace(year=datetime.now().year).strftime("%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return raw


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parse log file for suspicious login attempts"
    )
    parser.add_argument("input_file", help="Path to log file")
    parser.add_argument("-o", "--output", default="suspect.csv")
    return parser.parse_args()


def parse_log(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    records = []
    seen = set()

    with path.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            for service, event_type, pattern in PATTERNS:
                match = pattern.search(line)
                if match:
                    record = (
                        normalize_timestamp(match.group("timestamp")),
                        match.group("ip"),
                        match.group("username"),
                        service,
                        event_type,
                    )

                    if record not in seen:
                        seen.add(record)
                        records.append({
                            "timestamp": record[0],
                            "ip_address": record[1],
                            "username": record[2],
                            "service": record[3],
                            "event_type": record[4],
                        })
                    break

    return records


def write_csv(records, output_path):
    fieldnames = ["timestamp", "ip_address", "username", "service", "event_type"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[+] Written {len(records)} records to {output_path}")


def main():
    args = parse_arguments()
    records = parse_log(args.input_file)

    if not records:
        print("[-] No matching records found.")
        sys.exit(0)

    write_csv(records, args.output)


if __name__ == "__main__":
    main()
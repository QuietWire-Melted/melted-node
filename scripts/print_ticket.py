#!/usr/bin/env python3
import os, subprocess, sys
from pathlib import Path

def find_ticket(att_id: str) -> Path | None:
    base = Path("attestations")
    matches = list(base.rglob(f"{att_id}.ticket.txt"))
    return matches[0] if matches else None

def main():
    if len(sys.argv) < 2:
        print("Usage: print_ticket.py <ATT_ID>")
        sys.exit(1)

    att_id = sys.argv[1]
    tfile = find_ticket(att_id)
    if not tfile:
        print(f"Ticket file not found for ID: {att_id}")
        sys.exit(1)

    printer = os.environ.get("MELTED_PRINTER")  # if unset, use system default
    print(f"🖨️  Printer target: {printer or '<system-default>'}")
    cmd = ["lp"] + (["-d", printer] if printer else []) + [str(tfile)]
    r = subprocess.run(cmd, capture_output=True, text=True)

    if r.returncode != 0:
        print("lp error:", r.stderr.strip())
        if printer:  # retry on system default
            print("↪️  Retrying on system default…")
            subprocess.run(["lp", str(tfile)], check=False)
    else:
        print(r.stdout.strip())

if __name__ == "__main__":
    main()

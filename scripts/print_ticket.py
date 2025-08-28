#!/usr/bin/env python3
import os, subprocess, sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: print_ticket.py <ATT_ID>")
        sys.exit(1)

    att_id = sys.argv[1]
    tfile = Path("attestations") / Path(att_id[0:4]) / Path(att_id[5:7]) / Path(att_id[8:10]) / f"{att_id}.ticket.txt"

    if not tfile.exists():
        print(f"Ticket file not found: {tfile}")
        sys.exit(1)

    # Which printer to use
    printer = os.environ.get("MELTED_PRINTER")
    print(f"🖨️  Requested printer: {printer or '<system-default>'}")

    # Build lp command
    cmd = ["lp"] + (["-d", printer] if printer else []) + [str(tfile)]
    r = subprocess.run(cmd, capture_output=True, text=True)

    if r.returncode != 0:
        print("lp error:", r.stderr.strip())
        if printer:
            print("↪️  Retrying on system default…")
            subprocess.run(["lp", str(tfile)], check=False)
    else:
        print(r.stdout.strip())

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
import os, sys, json, subprocess, pathlib
BASE = pathlib.Path(__file__).resolve().parents[1]
aid = sys.argv[1]
glob = list((BASE/"attestations").rglob(f"{aid}.json"))
assert glob, "No such attestation"
rec = json.load(open(glob[0]))
tfile = glob[0].with_suffix(".ticket.txt")
printer = os.environ.get("MELTED_PRINTER","melted_printer")
subprocess.run(["lp","-d",printer,str(tfile)], check=False)

python - <<'PY'
from pathlib import Path
p = Path("scripts/print_ticket.py")
s = p.read_text()
if "print(" not in s or "lp -d" in s:
    s = s.replace(
        'printer = os.environ.get("MELTED_PRINTER","melted_printer")\nsubprocess.run(["lp","-d",printer,str(tfile)], check=False)\n',
        'printer = os.environ.get("MELTED_PRINTER")\n'
        'print(f"🖨️  Requested printer: {printer or \"<system-default>\"}")\n'
        'cmd = ["lp"] + (["-d", printer] if printer else []) + [str(tfile)]\n'
        'r = subprocess.run(cmd, capture_output=True, text=True)\n'
        'if r.returncode != 0:\n'
        '    print("lp error:", r.stderr.strip())\n'
        '    # Fallback to system default if a specific queue failed\n'
        '    if printer:\n'
        '        print("↪️  Retrying on system default…")\n'
        '        subprocess.run(["lp", str(tfile)], check=False)\n'
    )
    p.write_text(s)
    print("Patched scripts/print_ticket.py (debug + default fallback)")
PY

git add scripts/print_ticket.py
git commit -m "print_ticket: log selected printer and fallback to system default if queue missing"
git push


# 🌿 Melted Civic Node — Windows Setup

Run the Melted Node on a Windows PC at the shop. Two clean paths:

* **Option A (Recommended): Native Windows** — simplest; uses Canon’s Windows driver.
* **Option B: WSL2 (Ubuntu on Windows)** — mirrors Linux behavior; a bit more setup for printing/camera.

---

## Option A — Native Windows (Recommended)

### 0) What you’ll need

* **Windows 10/11**
* **Canon TR4700** driver installed (set as Windows default if you like)
* **Python 3.12+** (checked “Add to PATH” during install)
* **Git + Git LFS**
* (Optional) **FFmpeg** for nightly reels

### 1) Clone & initialize (PowerShell)

```powershell
# Open PowerShell as the Melted user
cd $env:USERPROFILE
git clone https://github.com/QuietWire-Melted/melted-node.git
cd melted-node

py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install python-dotenv pywin32
copy .env.example .env
notepad .env    # set MELTED_PRINTER=Canon_TR4700_series  (or leave blank to use Windows default)
```

> **Note:** On Windows, use full **OpenCV** for camera capture later.

```powershell
pip uninstall -y opencv-python-headless
pip install opencv-python
```

### 2) Add a Windows print shim

Create `scripts/win_print.py`:

```python
# scripts/win_print.py
import sys, win32print, win32api

def print_file(path, printer=None):
    if printer:
        # set default for this process; Windows uses the default device for shell print
        win32print.SetDefaultPrinter(printer)
    # Use the shell 'print' verb so the installed driver handles formatting
    win32api.ShellExecute(0, "print", path, None, ".", 0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: win_print.py <file> [PrinterName]")
        sys.exit(1)
    f = sys.argv[1]
    p = sys.argv[2] if len(sys.argv) > 2 else None
    print_file(f, p)
```

### 3) Make `print_ticket.py` Windows-aware

Edit `scripts/print_ticket.py` (only the bottom half changes):

```python
#!/usr/bin/env python3
import os, subprocess, sys, platform
from pathlib import Path

IS_WIN = platform.system() == "Windows"

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

    printer = os.environ.get("MELTED_PRINTER")  # if unset, use OS default
    print(f"🖨️  Printer target: {printer or '<system-default>'}")

    if IS_WIN:
        # Use Windows shell print via our shim
        cmd = ["python", "scripts/win_print.py", str(tfile)] + ([printer] if printer else [])
        subprocess.run(cmd, check=False)
    else:
        # Linux/mac: CUPS lp
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
```

### 4) Run it

```powershell
# Web UI on port from .env (default 8090 if you set it)
.\venv\Scripts\Activate.ps1
python scripts\web.py    # visit http://localhost:8090

# First capture (audio-only while camera gets set up)
python scripts\capture.py --text "Let the waters flow." --visibility public --no-photo

# Reprint any ticket by ID
python scripts\print_ticket.py <ATT_ID>
```

### 5) Auto-start on login (Task Scheduler)

Create `run-web.ps1`:

```powershell
# run-web.ps1
Set-Location "$env:USERPROFILE\melted-node"
.\venv\Scripts\Activate.ps1
python scripts\web.py
```

Schedule it:

* Open **Task Scheduler** → **Create Task…**
* Triggers: **At log on**
* Actions:

  * Program: `powershell.exe`
  * Args: `-NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\melted-node\run-web.ps1"`

*(Optional)* Create `run-capture.ps1` similarly if you add a background capture loop later.

### 6) Camera & Mic on Windows

* With `opencv-python` installed, the capture script can use cameras (`--camera 0`, `1`, etc.).
* `sounddevice` uses Windows audio devices; you can list devices later and pick by index if needed.

---

## Option B — WSL2 (Ubuntu on Windows)

### 1) Enable WSL2 + Ubuntu

* In PowerShell (Admin):
  `wsl --install`
* Reboot if prompted; launch **Ubuntu** from the Start menu.

### 2) Install stack inside Ubuntu

```bash
sudo apt update
sudo apt install -y git git-lfs ffmpeg cups python3-venv python3-pip
git clone https://github.com/QuietWire-Melted/melted-node.git
cd melted-node
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt python-dotenv opencv-python
cp .env.example .env
nano .env    # MELTED_PRINTER=<IPP queue if you add one to CUPS>
```

### 3) Printing options in WSL

* **Preferred**: keep Canon installed in Windows and print via Windows from WSL:

  * Create a tiny shim that calls Windows PowerShell to print (similar to `win_print.py`, but invoked via `powershell.exe` from WSL).
* **Alternative**: add Canon as an IPP queue inside WSL CUPS:

  * Enable CUPS web UI: `sudo cupsctl --remote-admin`
  * Visit `http://localhost:631`, add printer via IPP (may need Avahi/IPP Everywhere).
  * Then `MELTED_PRINTER=<CUPS queue>`.

### 4) Web UI

* Run in WSL: `python scripts/web.py`
* Access from Windows browser at `http://localhost:<PORT>`.

---

## Environment & Defaults

* `.env` controls the Node runtime:

  ```ini
  MELTED_HOST=0.0.0.0
  MELTED_PORT=8090
  MELTED_PRINTER=Canon_TR4700_series    # leave empty to use OS default
  MELTED_TICKET_TEMPLATE=tickets/ticket_template.txt
  ```

* Scripts will read `.env` automatically if `python-dotenv` is installed.

* On Windows, leaving `MELTED_PRINTER` empty uses the **Windows default** printer.

---

## Quick Bootstrap (PowerShell one-liner)

```powershell
cd $env:USERPROFILE; `
git clone https://github.com/QuietWire-Melted/melted-node.git; `
cd melted-node; `
py -m venv venv; .\venv\Scripts\Activate.ps1; `
pip install -r requirements.txt python-dotenv pywin32 opencv-python; `
copy .env.example .env; `
(Get-Content .env) -replace 'MELTED_PRINTER=.*','MELTED_PRINTER=Canon_TR4700_series' | Set-Content .env; `
python scripts\web.py
```

*(Adjust the printer name if Windows shows it differently.)*

---

## Troubleshooting

**Ticket doesn’t print on Windows**

* Ensure Canon TR4700 is installed and can print from Notepad.
* Set Windows default (optional): **Settings → Bluetooth & devices → Printers → Canon TR4700 → Set as default**.
* Run: `python scripts\print_ticket.py <ID>` and watch for the “Printer target” log line.

**Web port in use**

* Change `MELTED_PORT` in `.env` (e.g., `8090`), then restart `web.py`.

**No camera yet**

* Use `--no-photo` flag (already supported).
* Later remove the flag; if multiple cameras, try `--camera 1`, `2`, etc.

**Audio capture errors**

* Plug in a simple USB mic; Windows will expose it to Python via PortAudio (`sounddevice`).
* We can add a device picker later if needed.

---

## Commit suggestion

```
PATH: docs/Windows_Setup.md

BODY:
Add Windows setup guide: native Windows (recommended) and WSL2, with print shim, script diffs, bootstrap, and Task Scheduler instructions.

EXTENDED COMMIT MESSAGE:
This document enables Melted to run the Civic Node on a Windows PC:
- Native Windows path with win32 printing shim (win_print.py) and Windows-aware print_ticket.py.
- WSL2 option for a Linux-like stack.
- PowerShell bootstrap and auto-start instructions.
- Camera/mic notes, env defaults, and troubleshooting.
```

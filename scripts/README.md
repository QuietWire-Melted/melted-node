## 📂 Melted Civic Node`scripts/` — Runtime Utilities

**Purpose:** This folder contains the helper scripts that power the Melted Civic Node.

**Highlights**

* `capture.py` – record, hash, commit, print ticket.
* `print_ticket.py` – reprint a ticket by Attestation ID (Windows‑aware).
* `win_print.py` – Windows print shim (uses `pywin32`).
* `web.py` – local viewer/UI for recent attestations.
* `shortid.py` – ID generator.

---

## Ticket Printing

### `print_ticket.py`

* Main entry point for printing attestation tickets.
* Accepts an **Attestation ID** (e.g., `OL5I-H663`).
* Looks up the matching `.ticket.txt` file under `attestations/`.
* Chooses the correct printing backend depending on the system:

**On Linux/macOS (CUPS):**

```bash
python scripts/print_ticket.py OL5I-H663
```

* Uses `lp` under the hood.
* Honors the `MELTED_PRINTER` environment variable if set, otherwise defaults to the system printer.
* Falls back to system default if the chosen printer is missing.

**On Windows:**

```powershell
python scripts\print_ticket.py OL5I-H663
```

* Detects Windows automatically.
* Calls `win_print.py` to hand off the file to Windows printing APIs.

---

### `win_print.py`

* Windows-only shim using `win32print` and `win32api`.
* Prints the given file to the default Windows printer, or to a named printer if supplied.

Usage:

```powershell
python scripts\win_print.py attestations\2025\08\27\OL5I-H663.ticket.txt
```

Or with explicit printer:

```powershell
python scripts\win_print.py attestations\2025\08\27\OL5I-H663.ticket.txt "Canon TR4700 series"
```

---

## Notes

* Always ensure `.env` sets the correct printer if you want to override defaults:

  ```
  MELTED_PRINTER=Canon_TR4700_series
  ```
* If `.env` is missing or `MELTED_PRINTER` unset, the system default printer is used.
* On Windows, make sure the required Python package is installed:

  ```powershell
  pip install pywin32
  ```

---

## Other Scripts

* **`capture.py`** – handles recording attestations (audio, photo if enabled, metadata).
* **`web.py`** – serves the local web UI (default port: 8090 on Foundry).
* **`shortid.py`** – generates short unique attestation IDs.
* **`print_ticket.py`** – described above.

## 🗂️ Root files

* `.env.example` – baseline environment variables.
* `requirements.txt` – Python dependencies.
* `README.md` – project overview and quick start.

**Root README quick‑start (suggested snippet)**

````markdown
# Melted Civic Node (Six Nations)

Offline‑first attestation point at the Melted Dispensary: capture → hash → commit → ticket → local serve → sync.

## Quick start
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt python-dotenv
cp .env.example .env && nano .env   # set MELTED_PRINTER, port, etc.
python scripts/capture.py --text "You are remembered." --visibility public --no-photo
python scripts/web.py   # open http://localhost:8090
````

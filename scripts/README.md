# Melted Civic Node – Scripts

This folder contains the helper scripts that power the Melted Civic Node.

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

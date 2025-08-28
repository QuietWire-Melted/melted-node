# 📄 Staff Guide: Printing Tickets

This guide is for Melted staff who may need to reprint attestation tickets for customers.

---

## Reprinting a Ticket

1. **Find the Attestation ID**

   * IDs look like: `OL5I-H663`
   * Each attestation has a ticket file stored in the repo under `attestations/YYYY/MM/DD/`.

2. **Run the reprint command**

   ```bash
   python scripts/print_ticket.py <ATT_ID>
   ```

   Example:

   ```bash
   python scripts/print_ticket.py OL5I-H663
   ```

3. **Printer Selection**

   * If the system is set up with multiple printers, the software will:

     * First try the one in `.env` (`MELTED_PRINTER=Canon_TR4700_series`)
     * If not found, fall back to the system default.

4. **Confirm output**

   * A message will appear in the console:
     `🖨️  Printer target: Canon_TR4700_series`
     If it fails, it will retry on the system default printer.

---

## Troubleshooting

* **Nothing prints** → Check that the Canon TR4700 is powered on and online.

* **Wrong printer** → Update `.env` to set `MELTED_PRINTER` to the correct CUPS queue name.

* **Test print** → Run:

  ```bash
  echo "test page" | lp
  ```

  This should print immediately.

* **Windows staff** → Use the `win_print.py` script. Example:

  ```powershell
  python scripts\win_print.py OL5I-H663
  ```


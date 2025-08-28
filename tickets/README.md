## 📂 `tickets/` — Ticket Templates

**Purpose:** Text layout used to print the participant’s receipt.

**Key files**

* `ticket_template.txt` – placeholders are merged by `capture.py`.

**Placeholders**

* `{{id}}`, `{{timestamp}}`, `{{echo}}`, `{{qr}}` (if you add QR rendering), `{{node}}`.

**Design tips**

* Keep to \~32–42 characters per line for receipt printers; center key lines.
* Include a short line about the archive and a link/QR.

---


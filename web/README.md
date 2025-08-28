## 📂 `web/` — Local Viewer UI

**Purpose:** Minimal UI for browsing recent attestations on the Node device.

**Key files**

* `templates/index.html` – landing page.
* `templates/attestation.html` – single attestation view.
* `static/style.css` – small stylesheet.

**Running**

```bash
python scripts/web.py   # serves on port from .env / config
```

**Notes**

* Keep it lightweight; the Node is offline‑first and may run on small hardware.

---


---

## 📂 `config/` — Node Configuration

**Purpose:** Central runtime configuration for the Melted Civic Node.

**Key files**

* `node.yaml` – primary settings used by `capture.py` and `web.py`.
* (optional) `secrets.yaml` – if you later keep private tokens/keys out of `.env`.

**Example: `node.yaml`**

```yaml
web:
  host: 0.0.0.0
  port: 8090

capture:
  duration_sec: 5
  reel_enabled: false

camera:
  enabled: true        # set false if no camera yet
  device: auto         # or 0, 1, 2 …

printer:
  queue: Canon_TR4700_series  # or leave blank to use system default
```

**Notes**

* Values in `.env` can override parts of this file (e.g., `MELTED_PORT`, `MELTED_PRINTER`).
* Keep configuration small and readable so staff can adjust without code edits.

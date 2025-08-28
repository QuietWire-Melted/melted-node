## 📂 `system/` — Services & Ops

**Purpose:** Unit files and operational scripts for running the Node as a service.

**Key files**

* `melted-web.service` – example systemd unit for Linux hosts.

**Example service**

```ini
[Unit]
Description=Melted Civic Node Web UI
After=network.target

[Service]
WorkingDirectory=/opt/melted-node
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/melted-node/venv/bin/python scripts/web.py
Restart=on-failure
User=melted
Group=melted

[Install]
WantedBy=multi-user.target
```

**Notes**

* On Windows, use **Task Scheduler** instead (see `docs/Windows_Setup.md`).

---



## 📂 `schema/` — Data Contracts

**Purpose:** Canonical JSON Schemas for attestation records.

**Key files**

* `attestation.schema.json` – validates fields written by `capture.py`.

**Common fields**

* `id` (short id), `ts` (ISO timestamp), `text`, `visibility` (`public|first-name|anonymous`), `hash`, `media` (`audio`, optional `photo`).

**Why it matters**

* Schemas make long‑term archives reliable and portable across Civic Nodes.

---


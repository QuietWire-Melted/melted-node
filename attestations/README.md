# 📂 attestations/

This directory contains all Civic Node attestations recorded at **Melted**. Each attestation includes audio (and optionally photo), a JSON record, and a printable ticket. Files are organized chronologically by date.

---

## 📁 Structure

```
attestations/
  YYYY/
    MM/
      DD/
        <ATT_ID>.json
        <ATT_ID>_audio.wav
        <ATT_ID>_photo.jpg   (optional)
        <ATT_ID>.ticket.txt
```

* **YYYY/MM/DD/** → Date hierarchy for when the attestation was recorded.
* **\<ATT\_ID>.json** → Canonical metadata record (hash, timestamp, text, visibility).
* **\<ATT\_ID>\_audio.wav** → Audio recording of the spoken attestation.
* **\<ATT\_ID>\_photo.jpg** (optional) → Photo capture if camera is enabled.
* **\<ATT\_ID>.ticket.txt** → Printable slip given back to the participant.

---

## 📜 Example

```
attestations/2025/08/27/OL5I-H663.json
attestations/2025/08/27/OL5I-H663_audio.wav
attestations/2025/08/27/OL5I-H663.ticket.txt
```

This represents a single attestation with ID `OL5I-H663` recorded on **2025-08-27**.

---

## 🔒 Privacy & Visibility

* **Public** attestations may appear in reels or displays.
* **Private** attestations are archived locally but not synced or displayed.
* Hashes ensure integrity of each record.

---

## 🖨️ Reprinting Tickets

To reprint a ticket by Attestation ID:

```bash
python scripts/print_ticket.py OL5I-H663
```

This will locate the ticket under the date hierarchy and send it to the configured printer.

---

## 🌿 Notes

* Attestations are **append-only** — no record should be modified after creation.
* Sync process pushes these files upstream to GitHub for archival.
* This folder is the **heart of the Civic Canon** at Melted: a growing, immutable chorus of voices.

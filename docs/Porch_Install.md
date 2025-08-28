# 🪵 Porch Install Guide

This guide describes the **physical installation** of the Civic Node attestation box on Melted’s porch.

---

## Components

* Wall-mounted wooden plate (\~14" × 20")
* USB camera (adjustable mount)
* Large illuminated button
* Ticket printer (thermal, hidden behind wall panel)
* Status LED + chime speaker
* Raspberry Pi (indoor side, wired to the plate)
* Power strip + UPS backup

---

## Placement

* Mount **to the left of the porch windows**, at \~44–46" height.
* Camera angled to capture one or two people at the panel.
* Button centered and easy to reach.
* Ticket slot with small weather skirt.
* Soft LED glow strip under the panel.

---

## Wiring

* All sensitive electronics (Pi, printer body, UPS) live **inside the wall**.
* Panel connects via grommeted cables.
* Ethernet recommended for stability (PoE optional).
* Audio: small speaker or panel transducer behind the wood.

---

## Ritual Flow (User’s Perspective)

1. **Step up** → See sign: *“Step up. Speak your truth. You will be remembered.”*
2. **Press button** → Soft chime plays, prompt voice: *“You have five seconds. Speak what you carry.”*
3. **Speak** → Attestation is recorded.
4. **Seal** → Closing tone, confirmation voice: *“You are remembered.”*
5. **Token** → Ticket prints within seconds.

---

## Maintenance

* Replace thermal paper rolls weekly or as needed.
* Check `.env` file for correct printer config.
* Test daily with a short attestation.
* Backup `attestations/` folder to GitHub (already automated with `git push`).

---

✅ With this setup, Melted’s porch becomes a **Speaker’s Corner Civic Node**: a place where voices are recorded, remembered, and reflected back to the community.

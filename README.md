# Melted Civic Node (Six Nations)
Offline-first porch node for 5-second attestations: capture → hash → commit → ticket → local serve → (optional) sync.
## Quickstart
1) python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
2) cp .env.example .env
3) Configure CUPS printer queue name in .env (MELTED_PRINTER)
4) Test: `python scripts/capture.py --text "Let the waters flow."`
5) Serve local: `python scripts/web.py` then open http://localhost:8080

#!/usr/bin/env python3
import os, json, pathlib
from flask import Flask, render_template, send_from_directory, abort

BASE = pathlib.Path(__file__).resolve().parents[1]
app = Flask(__name__, template_folder=str(BASE/"web/templates"), static_folder=str(BASE/"web/static"))

def load_latest(n=100):
    items=[]
    for j in sorted(BASE.rglob("attestations/*/*/*/*.json"))[::-1]:
        rec = json.load(open(j))
        rec["media"]["photo_rel"] = "/media/"+"/".join(rec["media"]["photo"].split("attestations/")[1])
        items.append(rec)
        if len(items)>=n: break
    return items

@app.route("/")
def index():
    return render_template("index.html", items=load_latest())

@app.route("/a/<aid>")
def attestation(aid):
    js = list(BASE.rglob(f"attestations/*/*/*/{aid}.json"))
    if not js: abort(404)
    rec = json.load(open(js[0]))
    rec["media"]["photo_rel"] = "/media/"+"/".join(rec["media"]["photo"].split("attestations/")[1])
    return render_template("attestation.html", a=rec)

@app.route("/media/<path:sub>")
def media(sub):
    d = BASE/"attestations"
    return send_from_directory(d, sub)

if __name__=="__main__":
    app.run(host=os.getenv("MELTED_HOST","0.0.0.0"), port=int(os.getenv("MELTED_PORT","8080")))

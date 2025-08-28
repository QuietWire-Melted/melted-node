#!/usr/bin/env python3
import os, json, wave, datetime, pathlib, subprocess, argparse, yaml, hashlib
from shortid import make_short_id
from flask import Flask   # used only to reuse safe_join if desired
import sounddevice as sd
import soundfile as sf
import cv2

BASE = pathlib.Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(BASE/"config/node.yaml", "r"))
TZ  = CFG.get("timezone", "UTC")

def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

def ensure_day_dir(ts):
    d = datetime.datetime.fromisoformat(ts)
    p = BASE/ "attestations" / f"{d.year:04d}" / f"{d.month:02d}" / f"{d.day:02d}"
    p.mkdir(parents=True, exist_ok=True)
    return p

def take_photo(dev="auto", path="photo.jpg"):
    cam = cv2.VideoCapture(0 if dev=="auto" else dev)
    ok, frame = cam.read()
    cam.release()
    if not ok: raise RuntimeError("Camera capture failed")
    cv2.imwrite(path, frame)

def record_audio(seconds, path="audio.wav", samplerate=16000):
    audio = sd.rec(int(seconds*samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    sf.write(path, audio, samplerate)

def print_ticket(printer, textfile):
    # Use lp via CUPS
    subprocess.run(["lp","-d",printer,textfile], check=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="short utterance")
    ap.add_argument("--visibility", default="public", choices=["public","first-name","anonymous"])
    args = ap.parse_args()

    ts = now_iso()
    daydir = ensure_day_dir(ts)

    # capture media
    audio = daydir/"tmp_audio.wav"
    photo = daydir/"tmp_photo.jpg"
    record_audio(CFG.get("duration_sec",5), str(audio))
    take_photo(CFG["camera"]["device"], str(photo))

    # compute id/hash
    hasher = hashlib.blake2b(digest_size=16)
    for p in (audio, photo):
        with open(p,"rb") as f: hasher.update(f.read())
    hasher.update(args.text.encode())
    digest = hasher.hexdigest()
    sid = make_short_id(digest, ts)

    # final filenames
    a_id = sid
    final_audio = daydir/f"{a_id}_audio.wav"
    final_photo = daydir/f"{a_id}_photo.jpg"
    audio.rename(final_audio); photo.rename(final_photo)

    # write JSON record
    rec = {
        "id": a_id,
        "timestamp": ts,
        "visibility": args.visibility,
        "text": args.text.strip(),
        "media": {
            "audio": str(final_audio),
            "photo": str(final_photo)
        },
        "hash": digest,
        "tags":[]
    }
    with open(daydir/f"{a_id}.json","w") as f: json.dump(rec,f,indent=2)

    # write ticket text
    page_url = f"{CFG['web']['base_url_local']}/a/{a_id}"
    tfile = daydir/f"{a_id}.ticket.txt"
    with open(BASE/"tickets/ticket_template.txt") as tpl, open(tfile,"w") as out:
        s = tpl.read()
        dt = datetime.datetime.fromisoformat(ts)
        s = s.replace("{date}", dt.strftime("%Y-%m-%d"))
        s = s.replace("{time}", dt.strftime("%H:%M %Z"))
        s = s.replace("{id}", a_id)
        s = s.replace("{quote}", rec["text"])
        s = s.replace("{url}", page_url)
        out.write(s)

    # print
    printer = os.environ.get("MELTED_PRINTER","melted_printer")
    print_ticket(printer, str(tfile))

    # git commit
    subprocess.run(["git","add","."])
    subprocess.run(["git","commit","-m",f"Attestation {a_id}"], check=False)
    print(a_id)

if __name__ == "__main__":
    main()

import hashlib, base64
def make_short_id(*parts, length=10):
    h = hashlib.blake2b(("||".join(parts)).encode("utf-8"), digest_size=8).digest()
    s = base64.b32encode(h).decode("ascii").rstrip("=")
    # group as C3X8-A70D style
    s = s[:length]
    return f"{s[:4]}-{s[4:8]}"
if __name__ == "__main__":
    print(make_short_id("demo","2025-08-27T15:12:00Z"))

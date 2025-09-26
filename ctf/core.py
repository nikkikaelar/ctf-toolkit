import base64, binascii, re, math
from cryptography.hazmat.primitives import hashes
def analyze_text(s):
    out = {}
    out["length"] = len(s)
    out["entropy"] = _shannon(s)
    out["hex_like"] = bool(re.search(r"[0-9a-fA-F]{8,}", s))
    out["base64_like"] = bool(re.search(r"^[A-Za-z0-9+/=\\n\\r ]+$", s.strip()))
    out["suspicious_keywords"] = [k for k in ("flag","ctf","pico","key","secret") if k in s.lower()]
    return out
def decode_any(s, hint="auto"):
    s = s.strip()
    if hint=="hex" or re.fullmatch(r"[0-9a-fA-F\\s]+", s):
        try:
            h = s.replace(" ","")
            return binascii.unhexlify(h).decode("utf-8", "replace")
        except Exception:
            return ""
    if hint=="base64" or _looks_base64(s):
        try:
            return base64.b64decode(s).decode("utf-8","replace")
        except Exception:
            return ""
    if hint=="rot13":
        return s.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz","NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"))
    return _try_all(s)
def find_keys(s):
    out = []
    out += re.findall(r"FLAG\\{[^}]{3,200}\\}", s)
    out += re.findall(r"(?:AKIA|ASIA)[A-Z0-9]{16,40}", s)
    out += re.findall(r"([A-F0-9]{32})", s)
    return list(dict.fromkeys(out))
def _shannon(s):
    if not s:
        return 0.0
    freq={}
    for ch in s:
        freq[ch]=freq.get(ch,0)+1
    length=len(s)
    ent=0.0
    for v in freq.values():
        p=v/length
        ent -= p*(math.log(p,2))
    return round(ent,4)
def _looks_base64(s):
    s=s.replace("\\n","").replace("\\r","")
    return len(s)%4==0 and re.fullmatch(r"[A-Za-z0-9+/=]+", s) is not None
def _try_all(s):
    for method in ("utf8","hex","base64","rot13"):
        x = decode_any(s, method) if method!="utf8" else s
        if x and any(ch.isalpha() for ch in x):
            return x
    return ""

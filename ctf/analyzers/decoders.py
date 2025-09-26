import re, binascii, base64, codecs

_HEX_RE = re.compile(r"^[0-9a-fA-F\s]+$")
_B64_SET = re.compile(r"^[A-Za-z0-9+/=\r\n ]+$")

def decode_hex(s):
    try:
        return binascii.unhexlify(re.sub(r"\s+","", s)).decode("utf-8","replace")
    except Exception:
        return None

def decode_b64(s):
    try:
        raw = base64.b64decode(re.sub(r"\s+","", s), validate=False)
        return raw.decode("utf-8","replace")
    except Exception:
        return None

def decode_rot13(s):
    try:
        return codecs.decode(s, "rot_13")
    except Exception:
        return None

def decode_any(s):
    s = s.strip()
    if not s:
        return []
    out = []
    if _HEX_RE.fullmatch(s):
        v = decode_hex(s)
        if v: out.append({"method":"hex","decoded":v})
    if _B64_SET.fullmatch(s) and len(s.strip())%4==0:
        v = decode_b64(s)
        if v: out.append({"method":"base64","decoded":v})
    v = decode_rot13(s)
    if v and v != s:
        out.append({"method":"rot13","decoded":v})
    return out

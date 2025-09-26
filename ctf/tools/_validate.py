ALLOWED_NMAP_EXTRA = ["-sS","-sU","-Pn","-A","-T4","-sV"]
def sanitize_extra(extra):
    # keep tokens that look safe, drop the rest
    parts = extra.split()
    return " ".join([p for p in parts if p in ALLOWED_NMAP_EXTRA or p.startswith("-") and len(p)<=4])

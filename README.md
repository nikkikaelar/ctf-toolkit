# CTF Toolkit

Minimal Capture-the-Flag (CTF) assistant — a lightweight toolkit for quickly analyzing challenge data, decoding common encodings, and spotting hidden patterns. Designed for speed during competitions and clarity for learning, it gives you:

A web UI with a clean, minimal layout for pasting in challenge text
Automatic detection of common encodings (hex, base64, ROT13, etc.)
Entropy analysis and keyword spotting to hint at suspicious strings
Pattern finders for flags, keys, and other CTF artifacts
A modular design so you can extend it with your own analyzers
+more to be added

---

## Features
- **Analyze text** → length, entropy, keyword spotting
- **Decode** → auto-detects hex, base64, ROT13
- **Find patterns** → flags, API keys, hex strings
- **Web UI** → minimal dot-matrix style, easy copy/paste
- **External tools** → nmap scanning, john password cracking
- **Extensible** → add your own modules in `ctf/`

---

## Quickstart

Clone and install dependencies:
```bash
git clone https://github.com/nikkikaelar/ctf-toolkit.git
cd ctf-toolkit
pip install -r requirements.txt
```
---

File Layout:
```
ctf-toolkit/
├─ app.py                # Flask app entry
├─ requirements.txt      # Python dependencies
├─ config/               # tool configuration
│  └─ tools.yml
├─ ctf/                  # core logic
│  ├─ core.py
│  ├─ tasks.py
│  ├─ exec_tools.py      # safe subprocess wrapper
│  ├─ config.py          # config loader
│  └─ tools/             # external tool wrappers
│     ├─ nmap.py
│     ├─ john.py
│     └─ _validate.py
├─ templates/            # HTML templates
│  └─ index.html
├─ static/               # CSS and assets
│  └─ style.css
├─ tests/                # unit tests
│  └─ test_tools.py
└─ README.md
```

### Running external tools from the UI

**Nmap scanning:**
POST `/api/run/nmap` JSON: `{ "target":"1.2.3.4", "preset":"quick", "extra":"-sS" }`

**John password cracking:**
POST `/api/run/john` JSON: `{ "hashfile_path":"/tmp/uploads/h.txt", "wordlist":"/path/rockyou.txt", "format":"raw-md5" }`

**Upload hash files:**
POST `/api/upload/hashfile` with multipart form data containing the hash file

### Security Notes

- Tool invocations run with timeouts and output limits
- Input sanitization prevents command injection
- Extra arguments are whitelisted for safety
- Run these tool invocations as a limited user or inside containers to reduce blast radius

### Roadmap

- **Add XOR/stego brute-forcers**
- **Metadata extraction (images, PDFs)**
- **CLI version (python -m ctf.cli)**
- **Unit tests + GitHub Actions**

# CTF Toolkit — Educational Dashboard (MVP)

**Purpose**: Educational toolkit for offline/lab CTF practice. DO NOT use this software to scan or attack systems without explicit written permission.

Minimal Capture-the-Flag (CTF) assistant — a lightweight toolkit for quickly analyzing challenge data, decoding common encodings, and spotting hidden patterns. Designed for speed during competitions and clarity for learning, it gives you:

A web UI with a clean, minimal layout for pasting in challenge text
Automatic detection of common encodings (hex, base64, ROT13, etc.)
Entropy analysis and keyword spotting to hint at suspicious strings
Pattern finders for flags, keys, and other CTF artifacts
A modular design so you can extend it with your own analyzers
External tool integration with safety controls
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

## Quickstart (local, isolated VM)

1. Install dependencies: `pip install -r requirements.txt`
2. Start the backend: `uvicorn backend.app:app --reload --port 8080`
3. Open `frontend/index.html` in a browser and use dry-run options by default.

**Safety & Legal Notice**
- Runs that actually execute scanners are disabled by default (dry-run). To run live scans you must:
  - Enable Lab Mode in settings (manual config change).
  - Run inside an isolated VM / lab network.
  - Ensure you own or have permission for every target.

**Admin checklist**
- Do not enable live network scans on public or multi-tenant hosts.
- Enable containerized sandboxing before running active tools.
---

File Layout:
```
ctf-toolkit/
├─ backend/              # FastAPI backend
│  └─ app.py
├─ frontend/             # Static frontend
│  └─ index.html
├─ requirements.txt      # Python dependencies
├─ config/               # tool configuration
│  └─ tools.yml
├─ ctf/                  # core logic
│  ├─ core.py
│  ├─ tasks.py
│  ├─ exec_tools.py      # safe subprocess wrapper
│  ├─ config.py          # config loader
│  ├─ tools/             # external tool wrappers
│  │  ├─ nmap.py
│  │  └─ john.py
│  ├─ analyzers/         # pure Python analyzers
│  │  └─ decoders.py
│  └─ templates/         # template generators
│     └─ metasploit.py
├─ templates/            # Legacy Flask templates
│  └─ index.html
├─ static/               # CSS and assets
│  └─ style.css
├─ tests/                # unit tests
│  ├─ test_tools.py
│  └─ test_decoders.py
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

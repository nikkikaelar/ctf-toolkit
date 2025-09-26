from flask import Flask, render_template, request, jsonify
from ctf.core import analyze_text, decode_any, find_keys
from ctf.tasks import run_toggle
from ctf.tools import nmap as nmap_tool, john as john_tool
import tempfile, pathlib

app = Flask(__name__, static_folder="static", template_folder="templates")

# Setup upload directory for john hash files
UPLOAD_DIR = pathlib.Path("tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    payload = request.json or {}
    txt = payload.get("data", "")
    return jsonify({"report": analyze_text(txt)})

@app.route("/api/decode", methods=["POST"])
def api_decode():
    payload = request.json or {}
    typ = payload.get("type", "auto")
    txt = payload.get("data", "")
    return jsonify({"out": decode_any(txt, typ)})

@app.route("/api/find", methods=["POST"])
def api_find():
    payload = request.json or {}
    txt = payload.get("data", "")
    return jsonify({"matches": find_keys(txt)})

@app.route("/api/toggle", methods=["POST"])
def api_toggle():
    payload = request.json or {}
    name = payload.get("name", "")
    return jsonify({"status": run_toggle(name)})

@app.route("/api/run/nmap", methods=["POST"])
def api_run_nmap():
    body = request.json or {}
    target = body.get("target")
    preset = body.get("preset","quick")
    extra = body.get("extra","")
    if not target:
        return jsonify({"ok":False, "error":"missing target"}), 400
    # Input sanitization
    if len(target) > 200 or any(c in target for c in [";", "|", "&"]):
        return jsonify({"ok":False, "error":"invalid/too-long target"}), 400
    res = nmap_tool.run_nmap(target, preset=preset, extra_args=extra)
    return jsonify(res)

@app.route("/api/run/john", methods=["POST"])
def api_run_john():
    body = request.json or {}
    hashfile = body.get("hashfile_path")
    wordlist = body.get("wordlist")
    fmt = body.get("format")
    extra = body.get("extra","")
    if not hashfile:
        return jsonify({"ok":False, "error":"missing hashfile_path"}), 400
    res = john_tool.run_john(hashfile, wordlist=wordlist, fmt=fmt, extra_args=extra)
    return jsonify(res)

@app.route("/api/upload/hashfile", methods=["POST"])
def upload_hashfile():
    f = request.files.get("file")
    if not f:
        return jsonify({"ok":False,"error":"no file"}),400
    p = UPLOAD_DIR / f.filename
    f.save(str(p))
    return jsonify({"ok":True,"path":str(p)})

if __name__ == "__main__":
    app.run(port=8080)

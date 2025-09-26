from ..exec_tools import run_cmd
from ..config import load
import shlex, re

def build_nmap_cmd(target, preset="quick", extra_args=""):
    c = load().get("nmap", {})
    ports = c.get("port_presets", {}).get(preset, "1-1024")
    base = c.get("default_args", "")
    # sanitize extra by keeping tokens no longer than 16 chars and no shell metachars
    safe_extra = " ".join([t for t in shlex.split(extra_args) if len(t) < 17 and not re.search(r"[;&|`$<>]", t)])
    return f"nmap {base} -p {ports} {safe_extra} {shlex.quote(target)}".strip()

def run_nmap(target, preset="quick", extra_args="", timeout=None):
    cfg = load().get("nmap", {})
    timeout = timeout or cfg.get("max_runtime", 120)
    cmd = build_nmap_cmd(target, preset=preset, extra_args=extra_args)
    return run_cmd(cmd, timeout=timeout)

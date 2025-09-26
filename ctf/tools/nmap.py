from ..exec_tools import run_cmd
from ..config import load
from ._validate import sanitize_extra
import shlex

def build_nmap_cmd(target, preset="quick", extra_args=""):
    c = load().get("nmap", {})
    ports = c.get("port_presets", {}).get(preset, "1-1024")
    base = c.get("default_args", "")
    safe_extra = sanitize_extra(extra_args)
    args = f"nmap {base} -p {ports} {safe_extra} {shlex.quote(target)}"
    return args

def run_nmap(target, preset="quick", extra_args="", timeout=None):
    cfg = load().get("nmap", {})
    timeout = timeout or cfg.get("max_runtime", 120)
    cmd = build_nmap_cmd(target, preset=preset, extra_args=extra_args)
    return run_cmd(cmd, timeout=timeout)

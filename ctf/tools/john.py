from ..exec_tools import run_cmd
from ..config import load
import shlex, pathlib

def build_john_cmd(hashfile_path, wordlist=None, fmt=None, extra_args=""):
    c = load().get("john", {})
    wordlist = wordlist or c.get("default_wordlist","")
    fmt = fmt or c.get("default_format","")
    # keep extra limited
    safe_extra = " ".join([shlex.quote(p) for p in shlex.split(extra_args) if len(p) < 32])
    return f"john --wordlist={shlex.quote(wordlist)} --format={shlex.quote(fmt)} {safe_extra} {shlex.quote(str(hashfile_path))}".strip()

def run_john(hashfile_path, wordlist=None, fmt=None, timeout=None, extra_args=""):
    cfg = load().get("john", {})
    timeout = timeout or cfg.get("max_runtime", 3600)
    cmd = build_john_cmd(hashfile_path, wordlist=wordlist, fmt=fmt, extra_args=extra_args)
    return run_cmd(cmd, timeout=timeout)

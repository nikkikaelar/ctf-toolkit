from ..exec_tools import run_cmd
from ..config import load
import shlex, pathlib

def build_john_cmd(hashfile_path, wordlist=None, fmt=None, extra_args=""):
    c = load().get("john", {})
    wordlist = wordlist or c.get("default_wordlist")
    fmt = fmt or c.get("default_format")
    args = f"john --wordlist={shlex.quote(wordlist)} --format={shlex.quote(fmt)} {extra_args} {shlex.quote(str(hashfile_path))}"
    return args

def run_john(hashfile_path, wordlist=None, fmt=None, timeout=None, extra_args=""):
    cfg = load().get("john", {})
    timeout = timeout or cfg.get("max_runtime", 3600)
    cmd = build_john_cmd(hashfile_path, wordlist=wordlist, fmt=fmt, extra_args=extra_args)
    return run_cmd(cmd, timeout=timeout)

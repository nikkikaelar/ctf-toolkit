from ctf.tools.nmap import build_nmap_cmd
from ctf.tools.john import build_john_cmd
from ctf.tools._validate import sanitize_extra

def test_nmap_build():
    cmd = build_nmap_cmd("127.0.0.1", preset="quick")
    assert "nmap" in cmd and "127.0.0.1" in cmd

def test_john_build():
    cmd = build_john_cmd("/tmp/hash.txt")
    assert "john" in cmd and "/tmp/hash.txt" in cmd

def test_sanitize_extra():
    safe = sanitize_extra("-sS -A")
    assert "-sS" in safe and "-A" in safe
    
    unsafe = sanitize_extra("; rm -rf /")
    assert ";" not in unsafe and "rm" not in unsafe

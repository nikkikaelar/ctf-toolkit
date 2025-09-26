import shlex, subprocess, threading, tempfile, os

def run_cmd(cmd, timeout=30, cwd=None, env=None, max_output=200000):
    """
    Run an external command safely with timeout and output caps.
    Returns dict {ok, returncode, stdout, stderr, timed_out}
    """
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, env=env)
        timer = threading.Timer(timeout, proc.kill)
        timer.start()
        stdout, stderr = proc.communicate()
        timer.cancel()
        out = stdout.decode("utf-8", "replace")[:max_output]
        err = stderr.decode("utf-8", "replace")[:max_output]
        return {"ok": True, "returncode": proc.returncode, "stdout": out, "stderr": err, "timed_out": False}
    except Exception as e:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": str(e), "timed_out": False}

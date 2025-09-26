import threading, time
_state={}
def run_toggle(name):
    if name in _state and _state[name].get("running"):
        _state[name]["running"]=False
        return "stopped"
    _state[name] = {"running":True}
    t = threading.Thread(target=_worker, args=(name,), daemon=True)
    _state[name]["thread"]=t
    t.start()
    return "started"
def _worker(name):
    while _state.get(name,{}).get("running"):
        time.sleep(0.2)

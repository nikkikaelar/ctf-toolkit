import yaml, pathlib
_cfg = None
def load():
    global _cfg
    if _cfg is None:
        p = pathlib.Path("config/tools.yml")
        _cfg = yaml.safe_load(p.read_text()) if p.exists() else {}
    return _cfg

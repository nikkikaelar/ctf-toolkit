from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ctf.config import load
from ctf.tools import nmap as nmap_tool, john as john_tool
from ctf.exec_tools import run_cmd
import pathlib, uuid, shutil

app = FastAPI(title="GEARBOX (safe MVP)")

UPLOAD_DIR = pathlib.Path("tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class NmapReq(BaseModel):
    target: str
    preset: str = "quick"
    extra: str = ""
    dry_run: bool = True

class JohnReq(BaseModel):
    hashfile_path: str
    wordlist: str = None
    format: str = None
    dry_run: bool = True

@app.post("/api/run/nmap")
async def api_run_nmap(req: NmapReq):
    # validate target length and characters
    if len(req.target) > 200 or any(c in req.target for c in [";", "|", "&"]):
        raise HTTPException(status_code=400, detail="invalid/too-long target")
    cmd = nmap_tool.build_nmap_cmd(req.target, preset=req.preset, extra_args=req.extra)
    if req.dry_run:
        return {"ok": True, "cmd": cmd}
    res = nmap_tool.run_nmap(req.target, preset=req.preset, extra_args=req.extra)
    return JSONResponse(content=res)

@app.post("/api/run/john")
async def api_run_john(req: JohnReq):
    p = pathlib.Path(req.hashfile_path)
    if not p.exists():
        raise HTTPException(status_code=400, detail="missing hashfile_path")
    cmd = john_tool.build_john_cmd(p, wordlist=req.wordlist, fmt=req.format)
    if req.dry_run:
        return {"ok": True, "cmd": cmd}
    res = john_tool.run_john(p, wordlist=req.wordlist, fmt=req.format)
    return JSONResponse(content=res)

@app.post("/api/upload/hashfile")
async def upload_hashfile(file: UploadFile = File(...)):
    safe_name = f"{uuid.uuid4().hex}-{pathlib.Path(file.filename).name}"
    out = UPLOAD_DIR / safe_name
    with out.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"ok": True, "path": str(out)}

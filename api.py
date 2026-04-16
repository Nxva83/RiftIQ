"""
RiftIQ — API FastAPI
Sert les données JSON et les images PNG au dashboard React.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import json, os, glob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sert les images heatmap
app.mount("/heatmaps", StaticFiles(directory="output"), name="heatmaps")

DATA_DIR = "data"

@app.get("/api/player/{name}/{tag}")
def get_player(name: str, tag: str):
    path = f"{DATA_DIR}/player_{name}_{tag}.json"
    if not os.path.exists(path):
        return JSONResponse({"error": "not found"}, 404)
    return json.load(open(path))

@app.get("/api/matches/{name}/{tag}")
def get_matches(name: str, tag: str):
    path = f"{DATA_DIR}/matches_{name}_{tag}.json"
    if not os.path.exists(path):
        return JSONResponse({"error": "not found"}, 404)
    return json.load(open(path))

@app.get("/api/heatmaps/{name}/{tag}")
def get_heatmaps(name: str, tag: str):
    files = glob.glob("output/heatmap_*.png")
    maps = {}
    for f in sorted(files):
        base = os.path.basename(f).replace("heatmap_", "").replace(".png", "")
        parts = base.rsplit("_", 1)
        if len(parts) == 2:
            map_name, event_type = parts
            if map_name not in maps:
                maps[map_name] = {}
            maps[map_name][event_type] = f"/heatmaps/{os.path.basename(f)}"
    return maps

@app.get("/api/report/{name}/{tag}")
def get_report(name: str, tag: str):
    path = f"output/rapport_{name}_{tag}.txt"
    if not os.path.exists(path):
        return JSONResponse({"error": "not found"}, 404)
    return {"text": open(path).read()}

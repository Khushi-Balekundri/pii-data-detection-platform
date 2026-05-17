from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
from Pipeline.pipeline import run_pipeline
app = FastAPI()

# ---------------- CONFIG SCHEMA ----------------

class DBConfig(BaseModel):
    host: str
    user: str
    password: str
    db_name: str

class ScanConfig(BaseModel):
    paths: List[str]
    models: List[str]
    job_name: str
    db: DBConfig

# ---------------- API ----------------

@app.post("/scan")
def scan(config: ScanConfig):

    # Save config (optional)
    with open("config.json", "w") as f:
        json.dump(config.model_dump(), f, indent=2)

    # Run synchronously (BLOCK until complete)
    job_id = run_pipeline(config)
    return {
        "status": "completed",
        "job_id": job_id
    }
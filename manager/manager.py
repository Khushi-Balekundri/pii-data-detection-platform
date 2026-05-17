from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
from database.report_queries import fetch_report_data
from database.connection import get_connection

app = FastAPI()

SCANNER_URL = "http://localhost:8001"

# ---------------- REQUEST SCHEMA ----------------

class ScanRequest(BaseModel):
    paths: Optional[List[str]] = None
    models: List[str]
    job_name: str


class PathRequest(BaseModel):
    path: str

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "password"),
    "db_name": os.getenv("DB_NAME", "scanner_db")
}

@app.post("/add_path")
def add_path(request: PathRequest):

    path_input = request.path

    if not os.path.exists(path_input):
        raise HTTPException(status_code=400, detail="Path does not exist")

    try:
        conn = get_connection(db_config)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT IGNORE INTO path (name, path, allowed_flag) VALUES (%s, %s, 1)",
            (os.path.basename(path_input), path_input)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Path added", "path": path_input}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- API ----------------

@app.post("/start_scan")
def start_scan(payload: ScanRequest):

    paths = payload.paths

    # If no paths provided → fetch from DB
    if not paths:
        try:
            conn = get_connection(db_config)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT path FROM path WHERE allowed_flag = 1"
            )
            result = cursor.fetchall()

            paths = [row[0] for row in result]

            cursor.close()
            conn.close()

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    if not paths:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="No paths available for scanning")

    # EXACT CONFIG STRUCTURE (as required)
    config = {
        "paths": paths,
        "models": payload.models,
        "job_name": payload.job_name,
        "db": {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASS", "Sql@123"),
            "db_name": os.getenv("DB_NAME", "scanner_db")
        }
    }

    try:
        response = requests.post(f"{SCANNER_URL}/scan", json=config)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
    



@app.get("/report/{job_id}")
def get_report(job_id: int):
    return fetch_report_data(job_id, db_config)
        
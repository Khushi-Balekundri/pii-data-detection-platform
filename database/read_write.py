import mysql.connector
import joblib
from database.connection import get_connection

def start_scan_job(db_config):
    conn = get_connection(db_config)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scan_jobs (status) VALUES ('running')"
    )
    job_id = cursor.lastrowid

    conn.commit()
    cursor.close()
    conn.close()

    return job_id

def complete_scan_job(job_id, db_config):
    conn = get_connection(db_config)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE scan_jobs SET status = 'completed', ended_at = NOW() WHERE job_id = %s",
        (job_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

def load_all_models(db_config):
    conn = mysql.connector.connect(db_config)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT name, path FROM models")
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    models = {}
    for row in rows:
        with open(row["path"], "rb") as f:
            models[row["name"]] = joblib.load(f)
    
    return models



# def load_path():
#     conn = mysql.connector.connect(**DB_CONFIG)
#     cursor = conn.cursor(dictionary=True)
    
#     cursor.execute("SELECT name, path FROM path")
#     rows = cursor.fetchall()
    
#     cursor.close()
#     conn.close()
    
#     # path = {}
#     # for row in rows:
#     #         path[row["name"]] = row["path"]
    
#     return rows



def load_regex(db_config):
    conn = get_connection(db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, pattern FROM Regex")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    patterns = {row["name"]: row["pattern"] for row in rows}
    return patterns



def save_results_to_db(job_id, file_name, file_path, detection_counts, db_config):
    conn = get_connection(db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT file_id FROM files WHERE file_path = %s", (file_path,))
    row = cursor.fetchone()

    if row:
        file_id = row["file_id"]
    else:
        cursor.execute(
            "INSERT INTO files (file_name, file_path) VALUES (%s, %s)",
            (file_name, file_path)
        )
        file_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO scan_records (job_id, file_id) VALUES (%s, %s)",
        (job_id, file_id)
    )

    for datatype, sens_counts in detection_counts.items():
        for sensitivity, count in sens_counts.items():
            cursor.execute(
                """INSERT INTO scan_detections (file_id, job_id, datatype, sensitivity, count)
                VALUES (%s, %s, %s, %s, %s)""",
                (file_id, job_id, datatype, sensitivity, count)
            )

    conn.commit()
    cursor.close()
    conn.close()
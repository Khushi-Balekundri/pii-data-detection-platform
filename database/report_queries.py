from database.connection import get_connection

def fetch_report_data(job_id, db_config):
    conn = get_connection(db_config)
    cursor = conn.cursor(dictionary=True)

    # total files
    cursor.execute(
        "SELECT COUNT(*) as total_files FROM scan_records WHERE job_id = %s",
        (job_id,)
    )
    total_files = cursor.fetchone()["total_files"]

    # total detections
    cursor.execute(
        "SELECT SUM(count) as total_detections FROM scan_detections WHERE job_id = %s",
        (job_id,)
    )
    total_detections = cursor.fetchone()["total_detections"] or 0

    # top files
    cursor.execute(
        """SELECT f.file_name, f.file_path, r.score, r.category
           FROM risk_scores r
           JOIN files f ON r.file_id = f.file_id
           WHERE r.job_id = %s
           ORDER BY r.score DESC
           LIMIT 5"""
        ,
        (job_id,)
    )
    top_files = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_files": total_files,
        "total_detections": total_detections,
        "top_files": top_files
    }
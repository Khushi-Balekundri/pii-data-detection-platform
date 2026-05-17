import os
import math
from database.connection import get_connection


def calculate_risk_score(sensitivity_counts, volume, is_external, has_child_data, datatype_counts=None):
    # print("=== RISK calc ===", flush=True)
    SENS_WEIGHTS = {"low": 0.1, "mid": 0.5, "high": 1.0}
    
    total = float(sum(sensitivity_counts.values()))
    if total == 0:
        return 0.0 

    # weighted sum — more detections = higher score
    weighted_sum = sum(SENS_WEIGHTS.get(s, 0) * c for s, c in sensitivity_counts.items())

    # normalize by expected max (e.g. 5 high detections = max)
    base_score = min(1.0, weighted_sum / 5)

    # diversity multiplier — more datatype variety = higher risk
    if datatype_counts:
        unique_types      = len(datatype_counts)
        diversity_multiplier = min(2.0, 1.0 + (unique_types - 1) * 0.25)
    else:
        diversity_multiplier = 1.0

    # volume modifier
    volume_modifier     = min(1.0, math.log1p(volume) / math.log1p(10000))
    exposure_multiplier = 1.5 if is_external else 1.0
    child_multiplier    = 2.0 if has_child_data else 1.0

    score = base_score * diversity_multiplier * exposure_multiplier * child_multiplier
    score = min(1.0, score)

    return round(score, 2)


def categorize_risk(score):
    if score >= 0.75: return "critical"
    elif score >= 0.50: return "high"
    elif score >= 0.25: return "medium"
    else: return "low"


def calculate_and_save_risk(job_id, db_config):
    print("=== RISK started ===", flush=True)
    # conn   = mysql.connector.connect(db_config)
    conn = get_connection(db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """SELECT DISTINCT s.file_id, f.file_path
           FROM scan_records s
           JOIN files f ON s.file_id = f.file_id
           WHERE s.job_id = %s""",
        (job_id,)
    )
    files = cursor.fetchall()

    for file in files:
        # sensitivity counts
        cursor.execute(
            """SELECT sensitivity, SUM(count) as total
               FROM scan_detections
               WHERE job_id = %s AND file_id = %s
               GROUP BY sensitivity""",
            (job_id, file["file_id"])
        )
        sensitivity_counts = {row["sensitivity"]: float(row["total"]) for row in cursor.fetchall()}
        
        # datatype counts
        cursor.execute(
            """SELECT datatype, SUM(count) as total
               FROM scan_detections
               WHERE job_id = %s AND file_id = %s
               GROUP BY datatype""",
            (job_id, file["file_id"])
        )
        datatype_counts = {row["datatype"]: float(row["total"]) for row in cursor.fetchall()}

        # child flag
        # cursor.execute(
        #     """SELECT COUNT(*) as child_count
        #        FROM scan_detections
        #        WHERE job_id = %s AND file_id = %s AND child_flag = 1""",
        #     (job_id, file["file_id"])
        # )
        # has_child = cursor.fetchone()["child_count"] > 0
        has_child = False

        # calculate
        file_size_kb = os.path.getsize(file["file_path"]) / 1024
        score        = calculate_risk_score(sensitivity_counts, file_size_kb, True, has_child, datatype_counts)
        category     = categorize_risk(score)

        # save
        cursor.execute(
            """INSERT INTO risk_scores (job_id, file_id, score, category)
               VALUES (%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE score = VALUES(score), category = VALUES(category)""",
            (job_id, file["file_id"], score, category)
        )
        print("========RISK SAVED=======", flush=True)

    conn.commit()
    cursor.close()
    conn.close()
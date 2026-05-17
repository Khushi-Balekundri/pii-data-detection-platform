# import streamlit as st
# from database.connection import get_connection

# def get_report(job_id,db_config):
#     print("==========WRITING REP=========", flush=True)
#     conn = get_connection(db_config)
#     cursor = conn.cursor(dictionary=True)

#     # total files scanned
#     cursor.execute(
#         "SELECT COUNT(*) as total_files FROM scan_records WHERE job_id = %s",
#         (job_id,)
#     )
#     total_files = cursor.fetchone()["total_files"]

#     # total detections
#     cursor.execute(
#         "SELECT SUM(count) as total_detections FROM scan_detections WHERE job_id = %s",
#         (job_id,)
#     )
#     total_detections = cursor.fetchone()["total_detections"] or 0

#     # top 5 files with highest risk score
#     cursor.execute(
#         """SELECT f.file_name, f.file_path, r.score, r.category
#            FROM risk_scores r
#            JOIN files f ON r.file_id = f.file_id
#            WHERE r.job_id = %s
#            ORDER BY r.score DESC
#            LIMIT 5""",
#         (job_id,)
#     )
#     top_files = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return total_files, total_detections, top_files


# def show_report(job_id):
#     total_files, total_detections, top_files = get_report(job_id, config)

#     st.header("Scan Report")

#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("Total Files Scanned", total_files)
#     with col2:
#         st.metric("Total Detections", total_detections)

#     st.subheader("Top 5 Files by Risk Score")
#     for i, row in enumerate(top_files, 1):
#         st.write(f"{i}. **{row['file_name']}** — {row['category'].upper()} ({row['score']})")
#         st.caption(row["file_path"])
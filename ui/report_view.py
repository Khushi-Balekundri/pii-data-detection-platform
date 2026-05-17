import streamlit as st
import requests

MANAGER_URL = "http://localhost:8000"

def show_report(job_id):
    res = requests.get(f"{MANAGER_URL}/report/{job_id}")

    if res.status_code != 200:
        st.error("Failed to fetch report")
        return

    data = res.json()

    st.header("Scan Report")

    col1, col2 = st.columns(2)
    col1.metric("Total Files Scanned", data["total_files"])
    col2.metric("Total Detections", data["total_detections"])

    st.subheader("Top 5 Files by Risk Score")

    for i, row in enumerate(data["top_files"], 1):
        st.write(f"{i}. **{row['file_name']}** — {row['category'].upper()} ({row['score']})")
        st.caption(row["file_path"])
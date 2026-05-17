import streamlit as st
import requests
import os
import sys
from report_view import show_report

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


MANAGER_URL = "http://localhost:8000"

st.set_page_config(
    page_title="PII Data Scanner",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------

if "scanning" not in st.session_state:
    st.session_state.scanning = False

if "path" not in st.session_state:
    st.session_state.path = ""

if "job_id" not in st.session_state:
    st.session_state.job_id = None

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("🔐 PII Scanner")
    st.caption("Sensitive data detection and risk analysis")

    page = st.radio(
        "Navigation",
        ["Scan", "Reports"]
    )

    st.divider()

    if st.session_state.path:
        st.markdown("**Path selected**")
        st.caption(st.session_state.path)
    else:
        st.markdown("**No path selected**")

# ---------------- HEADER ----------------

st.title("PII Data Detection Platform")
st.caption("Machine learning + regex based sensitive data discovery")

# ==========================================================
# SCAN PAGE
# ==========================================================

if page == "Scan":

    col1, col2 = st.columns([2, 1], gap="large")

    # ---------------- LEFT PANEL ----------------

    with col1:

        with st.container(border=True):
            st.subheader("Select Folder")

            path_input = st.text_input(
                "Folder path",
                placeholder="C:/Users/yourname/Documents"
            )

            if st.button("Add Path", use_container_width=True):
                if path_input and os.path.exists(path_input):
                    st.session_state.path = path_input

                    requests.post(
                        f"{MANAGER_URL}/add_path",
                        json={"path": path_input}
                    )

                    st.success("Path added successfully")
                    st.rerun()

                else:
                    st.error("Invalid path")

        st.write("")

        with st.container(border=True):
            st.subheader("Run Scan")

            if not st.session_state.path:
                st.warning("Please select a valid folder first.")

            elif not st.session_state.scanning:

                if st.button("Start Scan", use_container_width=True):
                    st.session_state.scanning = True
                    st.rerun()

            else:
                st.info("Scanning in progress...")

    # ---------------- RIGHT PANEL ----------------

    with col2:

        with st.container(border=True):
            st.subheader("Current Status")

            if st.session_state.path:
                st.metric("Folder Selected", "Yes")
            else:
                st.metric("Folder Selected", "No")

            if st.session_state.scanning:
                st.metric("Scan State", "Running")
            else:
                st.metric("Scan State", "Idle")

# ==========================================================
# RUN SCAN
# ==========================================================

if st.session_state.scanning:

    with st.spinner("Scanning files..."):

        res = requests.post(
            f"{MANAGER_URL}/start_scan",
            json={
                "paths": [st.session_state.path],
                "models": [
                    "models/datatype_model_v2.pkl",
                    "models/sensitivity_model_v2.pkl"
                ],
                "job_name": "scan_001"
            }
        )

    if res.status_code == 200:
        st.session_state.job_id = res.json().get("job_id")
        st.session_state.scanning = False
        st.success("Scan complete")
        st.rerun()

    else:
        st.session_state.scanning = False
        st.error("Scan failed")

# ==========================================================
# REPORT PAGE
# ==========================================================

if page == "Reports":

    st.subheader("Scan Results")

    if st.session_state.job_id:
        show_report(st.session_state.job_id)
    else:
        st.info("No completed scans available yet.")
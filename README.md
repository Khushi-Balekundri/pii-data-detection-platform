# PII Data Detection System

An AI-powered sensitive data scanning and risk analysis platform designed to detect Personally Identifiable Information (PII) across files and directories using machine learning and regex-based analysis.

The system automates identification of confidential information such as names, phone numbers, email addresses, and other sensitive entities while generating structured risk reports for privacy auditing and compliance-oriented workflows.

---

# Features

- Automated directory and file scanning
-  Machine Learning + Regex-based PII detection
-  Risk scoring and file categorization
-  FastAPI-based backend architecture
-  Interactive Streamlit dashboard
-  MySQL-based persistent storage
-  Report generation for scanned files
-  Multithreaded file processing pipeline
-  Support for recursive directory traversal

---

## Sample Scan Results / Report
<img width="602" height="758" alt="Screenshot 2026-05-05 111955" src="https://github.com/user-attachments/assets/490bcb06-0539-4038-a697-45f7a19c9ea3" />


---

# System Architecture
<img width="1536" height="1024" alt="ChatGPT Image May 5, 2026, 10_56_46 AM" src="https://github.com/user-attachments/assets/2ab63d6b-61a5-4d44-8549-12103359cad4" />


---

#  Project Structure

```text
project/
│
├── .streamlit/              # Streamlit theme configuration
├── agent/                   # Scanning agent service
├── database/                # Database connection and queries, sql file
├── main_engine/             # Detection, sampling, and risk logic
├── manager/                 # API orchestration layer
├── models/                  # ML model files
├── Pipeline/                # Main scan execution pipeline
├── report_generator/        # Report generation module
├── scanner/                 # File scanning logic
├── ui/                      # Streamlit frontend
│
├── requirements.txt
├── README.md
└── .gitignore

```

---

#  System Workflow

1. User selects a directory through the Streamlit UI.
2. UI sends scan request to the Manager API.
3. Manager validates paths and builds scan configuration.
4. Configuration is forwarded to the Scanning Agent.
5. Agent launches the scanning pipeline in the background.
6. Files are recursively scanned and analyzed.
7. Detection results are stored in MySQL.
8. Risk scores are computed for scanned files.
9. Reports are generated and displayed on the dashboard.

---

#  Detection Approach

The system combines:

## 1. Rule-Based Detection
Regex patterns are used to identify:
- Email addresses
- Phone numbers
- Structured identifiers
- Pattern-based sensitive information

## 2. Machine Learning Detection
ML models classify:
- Datatypes
- Sensitivity levels
- Contextual textual entities

Sentence embeddings are generated using:

- `sentence-transformers/all-MiniLM-L6-v2`

---

#  Risk Analysis

Each scanned file is assigned a risk score based on:

- Number of sensitive detections
- Sensitivity level
- File characteristics
- Detection severity

Files are categorized as:
- Low Risk
- Medium Risk
- High Risk
- Critical Risk

This enables prioritization for privacy audits and remediation workflows.

---

# Privacy & Compliance

The project was developed with a focus on:

- Personally Identifiable Information (PII) discovery
- Privacy-aware data classification
- Compliance-oriented risk assessment
- Support for governance workflows

The system aligns conceptually with data protection requirements such as the:

- Digital Personal Data Protection Act (DPDP Act), India

---

# Installation

## 1. Clone Repository

```bash
git clone <your-repo-link>
cd <repo-name>
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Database Setup

1. Create a MySQL database

2. Import:

```text
database_model.sql
```
located in 'database' folder.

3. Configure database credentials using environment variables or `.env`

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASS=your_password
DB_NAME=scanner_db
```

---

# Running the Application

## Step 1 — Start Manager API

```bash
uvicorn manager.manager:app --port 8000 --reload
```

---

## Step 2 — Start Agent API

```bash
uvicorn agent.agent:app --port 8001 --reload
```

---

## Step 3 — Launch Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

---

# API Endpoints

## Manager Service

| Endpoint | Method | Description |
|---|---|---|
| `/add_path` | POST | Add scan directory |
| `/start_scan` | POST | Start scanning job |
| `/login` | POST | User login |
| `/signup` | POST | User registration |

---

## Agent Service

| Endpoint | Method | Description |
|---|---|---|
| `/scan` | POST | Execute scanning pipeline |

---

# Key Modules

## UI Layer
- Streamlit frontend
- Dashboard and reporting
- User interaction

## Manager Layer
- Request orchestration
- Authentication
- Path management
- API coordination

## Agent Layer
- Background scanning execution
- Pipeline management
- Model loading

## Database Layer
- Persistent scan storage
- Risk data
- Reports
- User management

---

#  Future Enhancements

- Login and authentication
- Real-time scan progress tracking
- OCR support for image-based files
- Cloud storage scanning
- Role-based access control
- Exportable PDF reports
- Incremental scanning
- Advanced analytics dashboard

---

# Author

> Khushi Balekundri

- Backend Development
- Machine Learning
- Privacy & Compliance Systems

---

# License

This project is intended for academic, internship, and educational purposes.

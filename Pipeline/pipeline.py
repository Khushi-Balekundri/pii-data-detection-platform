from scanner.file_scanner import scan_directory
from main_engine.sampler import sample_file_contents
from main_engine.classification import analyze_content
from main_engine.risk import calculate_and_save_risk
from main_engine.model_loader import load_models
from database.read_write import save_results_to_db, load_regex, start_scan_job, complete_scan_job
import os

def process_file(file_path, job_id, models, patterns, embedder, config):
    print("=== PROCESS FILES STARTED ===", flush=True)
    text = sample_file_contents(file_path)
    if not text:
        return None
    detection_counts = analyze_content(embedder, text, models, patterns)
    save_results_to_db(job_id,os.path.basename(file_path),file_path,detection_counts, config)

def run_pipeline(config):
    print("=== PIPELINE STARTED ===", flush=True)
    job_id = start_scan_job(config.db)

    # Load from config
    paths = config.paths
    model_paths = config.models
    models = load_models(model_paths)

    # Still okay from DB
    patterns = load_regex(config.db)

    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    for path in paths:
        scan_directory(
            path,
            lambda fp: process_file(fp, job_id, models, patterns, embedder, config.db)
        )

    complete_scan_job(job_id, config.db)
    calculate_and_save_risk(job_id, config.db)

    return job_id
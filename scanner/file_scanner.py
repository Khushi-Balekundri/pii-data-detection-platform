import os
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed



MAX_FILE_SIZE_MB = 100
ALLOWED_EXTENSIONS = {
    ".csv", ".txt", ".pdf", ".docx", ".xlsx", ".json"
}



def compute_file_hash(file_path, chunk_size=8192):
    """
    Compute SHA256 hash for deduplication.
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None



def extract_metadata(file_path):
    """
    Extracting lightweight metadata only.
    """
    try:
        stat = os.stat(file_path)
        file_size_mb = stat.st_size / (1024 * 1024)

        return {
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "extension": os.path.splitext(file_path)[1].lower(),
            "size_mb": round(file_size_mb, 2),
            "last_modified": datetime.fromtimestamp(stat.st_mtime),
        }

    except Exception:
        return None



def metadata_risk_hint(metadata):
    """
    Quick filename/folder heuristic scoring.
    """
    keywords = [
        "aadhaar", "pan", "passport",
        "salary", "finance", "hr",
        "kyc", "student", "medical"
    ]

    name_path = (
        metadata["file_name"].lower() +
        metadata["file_path"].lower()
    )

    for word in keywords:
        if word in name_path:
            return "high"

    if metadata["size_mb"] > 50:
        return "medium"

    return "low"



def process_file(file_path):
    """
    Process a single file at metadata-level only.
    """

    metadata = extract_metadata(file_path)
    if not metadata:
        return None

    # Skip unsupported types
    if metadata["extension"] not in ALLOWED_EXTENSIONS:
        return None

    # Skip very large files
    if metadata["size_mb"] > MAX_FILE_SIZE_MB:
        metadata["scan_status"] = "skipped_large_file"
        return metadata

    # Add hash for dedup
    metadata["file_hash"] = compute_file_hash(file_path)

    # Metadata risk
    metadata["metadata_risk"] = metadata_risk_hint(metadata)

    metadata["scan_status"] = "metadata_scanned"

    return metadata



def scan_directory(root_path, process_fn, max_workers=os.cpu_count()):
    print("=== SCAN DIR STARTED ===", flush=True)   
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, _, files in os.walk(root_path): 
            for file in files:
                file_path = os.path.join(root, file)
                futures.append(executor.submit(process_fn, file_path))
        for future in as_completed(futures):
            future.result()


# OG

# def scan_directory(root_path, max_workers=8):
#     """
#     Walk directory and scan files concurrently.
#     """

#     results = []

#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = []

#         for root, _, files in os.walk(root_path):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 futures.append(executor.submit(sample_file_contents, file_path))

#         for future in as_completed(futures):
#             result = future.result()
#             if result:
#                 results.append(result)

#     return result


# for root, _, files in os.walk(root_path):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 futures.append(executor.submit(process_file, file_path))
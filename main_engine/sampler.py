import os
import random

_SMALL_FILE = 512000  # 500KB
SKIP_EXTENSIONS = {".css", ".tsx", ".jsx", ".lock", ".map"}

def sample_file_contents(file_path, max_txt_bytes=102400):
    print("=== SAMPLE STARTED ===", flush=True)
    ext  = os.path.splitext(file_path)[1].lower()
    if ext in SKIP_EXTENSIONS:
        return None
    size = os.path.getsize(file_path)
    try:
        handler = _HANDLERS.get(ext, _read_default)
        return handler(file_path, size, max_txt_bytes)
    except Exception:
        return None


def _read_text(file_path, size, max_bytes, **_):
    if size < _SMALL_FILE:
        with open(file_path, "r", errors="replace") as f:
            return f.read()
    return _sample_thirds(file_path, size, max_bytes)


def _read_csv(file_path, size, max_bytes, **_):
    if size < _SMALL_FILE:
        with open(file_path, "r", errors="replace") as f:
            return f.read()
    return _sample_thirds(file_path, size, max_bytes)


def _read_json(file_path, size, _, **__):
    max_bytes = 153600
    if size < _SMALL_FILE:
        with open(file_path, "r", errors="replace") as f:
            return f.read()
    return _sample_thirds(file_path, size, max_bytes)


def _read_pdf(file_path, size, _, **__):
    import pypdf
    max_bytes = 229376
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        total  = len(reader.pages)

        # full scan if small
        if size < _SMALL_FILE:
            return "\n".join(p.extract_text() or "" for p in reader.pages)

        # sampling if large
        third     = max(1, total // 3)
        mid_start = (total - third) // 2
        page_indices = (
            list(range(0, third)) +
            list(range(mid_start, mid_start + third)) +
            list(range(total - third, total))
        )
        return "\n".join(reader.pages[i].extract_text() or "" for i in page_indices)


def _read_default(file_path, size, max_bytes, **_):
    if size < _SMALL_FILE:
        with open(file_path, "r", errors="replace") as f:
            return f.read()
    return _sample_thirds(file_path, size, max_bytes)


def _sample_thirds(file_path, size, max_bytes):
    chunk  = max_bytes // 3
    sample = 102400  # 100KB random sample within each third

    third_ranges = [
        (0,                         chunk),
        ((size - chunk) // 2,       (size + chunk) // 2),
        (size - chunk,              size),
    ]

    chunks = []
    with open(file_path, "r", errors="replace") as f:
        for start, end in third_ranges:
            max_offset = max(start, end - sample)
            offset     = random.randint(start, max_offset)
            f.seek(offset)
            chunks.append(f.read(sample))

    return "\n---\n".join(chunks)


_HANDLERS = {
    ".txt":  _read_text,
    ".log":  _read_text,
    ".md":   _read_text,
    ".csv":  _read_csv,
    ".json": _read_json,
    ".pdf":  _read_pdf,
}
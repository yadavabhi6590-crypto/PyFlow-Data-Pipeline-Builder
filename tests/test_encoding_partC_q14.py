from pathlib import Path
import chardet
import pandas as pd


def process_csv_with_auto_encoding(file_path: str, chunk_size: int = 50000) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    # Sample bytes read karke encoding aur confidence detect karna
    sample_size = min(path.stat().st_size, 100_000)
    with open(path, "rb") as f:
        raw_sample = f.read(sample_size)

    detection = chardet.detect(raw_sample) or {}
    detected_encoding = detection.get("encoding") or "utf-8"
    confidence = float(detection.get("confidence") or 0.0)

    total_chunks = 0
    total_rows = 0

    for chunk in pd.read_csv(path, encoding=detected_encoding, chunksize=chunk_size, low_memory=False):
        total_chunks += 1
        total_rows += len(chunk)

    return {
        "detected_encoding": detected_encoding,
        "confidence": confidence,
        "total_chunks": total_chunks,
        "total_rows": total_rows,
    }
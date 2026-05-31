import hashlib
from pathlib import Path

def calculate_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    except (PermissionError, OSError) as e:
        raise OSError(f"Error reading file {file_path}: {e}") from e

    return sha256_hash.hexdigest()

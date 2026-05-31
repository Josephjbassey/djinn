import hashlib
from pathlib import Path
from typing import Union

def calculate_hash(data: Union[Path, bytes]) -> str:
    """Calculate SHA256 hash of a file or bytes."""
    sha256_hash = hashlib.sha256()

    if isinstance(data, Path):
        if not data.exists():
            raise FileNotFoundError(f"File not found: {data}")
        try:
            with open(data, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
        except (PermissionError, OSError) as e:
            raise OSError(f"Error reading file {data}: {e}") from e
    else:
        sha256_hash.update(data)

    return sha256_hash.hexdigest()

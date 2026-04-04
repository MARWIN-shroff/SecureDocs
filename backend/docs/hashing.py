import hashlib
from typing import BinaryIO

def calculate_file_hash(file_obj: BinaryIO) -> str:
    """Calculate SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    for chunk in iter(lambda: file_obj.read(4096), b""):
        hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def calculate_content_hash(content: str) -> str:
    """Calculate SHA-256 hash of text content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

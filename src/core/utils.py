import hashlib

def stable_hash(text: str) -> int:
    digest = hashlib.sha256(text.encode()).digest()
    return int.from_bytes(digest[:8], 'big')
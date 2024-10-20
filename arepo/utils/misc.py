import hashlib


def generate_id(string: str):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

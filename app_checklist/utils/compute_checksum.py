import hashlib


def compute_checksum(file_path):
    """
    Compute the checksum of the file.
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
    return hashlib.sha256(file_content).hexdigest()

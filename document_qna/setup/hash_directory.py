import os
import xxhash

def hash_file(filepath):
    """Calculate the XXH128 hash of a file."""
    h = xxhash.xxh128()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def hash_directory(directory):
    """Calculate a hash for the entire directory using XXHash."""
    h = xxhash.xxh128()

    for root, dirs, files in os.walk(directory):
        # Sort dirs and files to ensure consistent order
        dirs.sort()
        files.sort()

        # Update hash with directory path
        h.update(root.encode())

        # Update hash with file names and their contents
        for filename in files:
            filepath = os.path.join(root, filename)
            h.update(filename.encode())
            file_hash = hash_file(filepath)
            h.update(file_hash.encode())

        # Update hash with subdirectory names
        for dirname in dirs:
            h.update(dirname.encode())

    return h.hexdigest()
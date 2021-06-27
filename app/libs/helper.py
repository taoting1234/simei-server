import hashlib


def md5(raw):
    if isinstance(raw, str):
        raw = raw.encode()
    return hashlib.md5(raw).hexdigest()

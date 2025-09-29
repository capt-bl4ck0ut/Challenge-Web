import hashlib

def encoder(password):
    return hashlib.md5(password.encode("utf-8")).digest()
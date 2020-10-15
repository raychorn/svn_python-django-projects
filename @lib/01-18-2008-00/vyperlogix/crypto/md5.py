def md5(plain):
    import hashlib
    m = hashlib.md5()
    m.update(plain)
    return m.hexdigest()

def onexit(f):
    import atexit
    atexit.register(f)
    return f


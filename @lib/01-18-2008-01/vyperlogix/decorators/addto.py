def _addto(instance,f):
    import new
    f = new.instancemethod(f, instance, instance.__class__)
    setattr(instance, f.func_name, f)
    return f

def addto(instance):
    def decorator(f):
        import new
        f = new.instancemethod(f, instance, instance.__class__)
        setattr(instance, f.func_name, f)
        return f
    return decorator

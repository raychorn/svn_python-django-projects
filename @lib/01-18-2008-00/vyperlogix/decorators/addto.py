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

if (__name__ == '__main__'):
    class Foo:
        def __init__(self):
            self.x = 42
    
    foo = Foo()

    @addto(foo)
    def print_x(self):
        print self.x
    
    foo.print_x() # would print "42


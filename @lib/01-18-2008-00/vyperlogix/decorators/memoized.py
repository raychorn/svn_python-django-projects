from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.hash import lists

class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = lists.HashedLists2()
        self.objType = ObjectTypeName.typeName(self)
        
    def __call__(self, *args):
        _name = misc.callersName()
        _l = ['_'.join(str(c).split()) for c in args if ObjectTypeName.typeName(c).find('.') == -1]
        _key = '_'.join(_l)
        if (self.cache[_name] == None):
            self.cache[_name] = {}
        try:
            return self.cache[_name][_key]
        except KeyError:
            self.cache[_name][_key] = value = self.func(*args)
            return value
        except TypeError, e:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
        
    def __repr__(self):
        """Return the function's docstring."""
        return '(%s.%s) :: %s' % (self.objType,misc.funcName(),self.func.__doc__)

if (__name__ == '__main__'):
    @memoized
    def fibonacci(n):
        "Return the nth fibonacci number."
        if n in (0, 1):
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print fibonacci(12)


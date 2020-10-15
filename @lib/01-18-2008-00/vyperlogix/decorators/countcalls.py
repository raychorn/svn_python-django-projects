class countcalls(object):
    "Decorator that keeps track of the number of times a function is called."
    
    __instances = {}
    
    def __init__(self, f):
        self.__f = f
        self.__numCalls = 0
        countcalls.__instances[f] = self
    
    def __call__(self, *args, **kwargs):
        self.__numCalls += 1
        return self.__f(*args, **kwargs)
    
    @staticmethod
    def count(f):
        "Return the number of times the function f was called."
        return countcalls.__instances[f].__numCalls
    
    @staticmethod
    def counts():
        "Return a dict of {function: # of calls} for all registered functions."
        return dict([(f, countcalls.count(f)) for f in countcalls.__instances])
  
if (__name__ == '__main__'):
    pass

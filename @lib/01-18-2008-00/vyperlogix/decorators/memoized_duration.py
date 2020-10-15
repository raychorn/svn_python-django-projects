import time
from threading import Lock

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

from vyperlogix.decorators.synchronized import synchronized

_caches = {}

class MemoizeForDuration(object):
    """Memoize for a period of time.  Be sure to call the collect method on a regular basis to clear old entries,
    perhaps make this a background function that runs every 60 secs or so."""
    _timeouts = {}
    _lock = Lock()
    
    def __init__(self,timeout=60,interval=60,isDebug=False):
        '''
        timeout specifies the duration for the remembered item.
        interval specifies the period of time between collect events.
        '''
        self.interval = interval
        self.timeout = timeout
        self.isDebugging = isDebug
        
    @synchronized(_lock)
    def collect(self):
        """Clear cache of results which have timed out"""
        self.isCollecting = True
        for func in _caches:
            cache = {}
            for key in _caches[func]:
                if (time.time() - _caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = _caches[func][key]
            _caches[func] = cache
        self.isCollecting = False
    
    def __call__(self, f):
        if (_caches.has_key(f)):
            _cache = _caches[f]
        else:
            _cache = _caches[f] = {}
        self._timeouts[f] = self.timeout
        
        def func(*args, **kwargs):
            kw = kwargs.items()
            kw.sort()
            key = (args, tuple(kw))
            try:
                v = _cache[key]
                if (self.isDebugging):
                    print '\n%s :: cache :: "%s"' % (ObjectTypeName.objectSignature(self),key)
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                if (self.isDebugging):
                    print '\n%s :: new (%d) :: "%s"' % (ObjectTypeName.objectSignature(self),len(_cache),key)
                v = _cache[key] = f(*args,**kwargs),time.time()
            return v[0]
        func.func_name = f.func_name
        
        return func

class MemoizeStrictForDuration(MemoizeForDuration):
    def __call__(self, f):
        if (_caches.has_key(f)):
            _cache = _caches[f]
        else:
            _cache = _caches[f] = {}
        self._timeouts[f] = self.timeout
        
        def func(*args, **kwargs):
            kw = kwargs.items()
            kw.sort()
            key = (tuple([arg for arg in list(args) if (misc.isString(arg))]), tuple(kw))
            try:
                v = _cache[key]
                et = time.time() - v[1]
                if (self.isDebugging):
                    print '\n%s :: cache :: "%s"' % (ObjectTypeName.objectSignature(self),key)
                if (et) > self.timeout:
                    raise KeyError
            except KeyError:
                v = _cache[key] = f(*args,**kwargs),time.time()
                if (self.isDebugging):
                    print '\n%s :: new (%d) :: "%s"' % (ObjectTypeName.objectSignature(self),len(_cache),key)
            return v[0]
        func.func_name = f.func_name
        
        return func

if (__name__ == '__main__'):
    #The code below demonstrates usage of the MWT decorator. Notice how the cache is
    #cleared of some entries after the MWT().collect() method is called.
    
    @MemoizeForDuration()
    def z(a,b):
        return a + b
    
    @MemoizeForDuration(timeout=5)
    def x(a,b):
        return a + b
    
    z(1,2)
    x(1,3)
    
    print _caches
    #>>> {<function 'z'>: {(1, 2): (3, 1099276281.092)},<function 'x'> : {(1, 3): (4, 1099276281.092)}}
    
    time.sleep(3)
    MemoizeForDuration().collect()
    print _caches
    #>>> {<function 'z'>: {},<function 'x'> : {(1, 3): (4, 1099276281.092)}}
    
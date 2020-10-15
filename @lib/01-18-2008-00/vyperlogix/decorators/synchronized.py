def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap

if (__name__ == '__main__'):
    from threading import Lock
    myLock = Lock()
    
    @synchronized(myLock)
    def critical1(*args):
        # Interesting stuff goes here.
        pass
    
    @synchronized(myLock)
    def critical2(*args):
        # Other interesting stuff goes here.
        pass

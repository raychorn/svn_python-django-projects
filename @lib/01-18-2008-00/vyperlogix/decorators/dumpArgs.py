def dumpArgs(func):
    "This decorator dumps out the arguments passed to a function before calling it"
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name
    def echoFunc(*args,**kwargs):
        print fname, ":", ', '.join('%s=%r' % entry
                                    for entry in zip(argnames,args) + kwargs.items())
        return func(*args, **kwargs)
    return echoFunc

if (__name__ == '__main__'):
    @dumpArgs
    def f1(a,b,c):
        print a + b + c
    
    f1(1, 2, 3)

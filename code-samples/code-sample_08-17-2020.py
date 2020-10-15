if (0):
    import functools
    
    def f(x,y):
        print 'x=%s, y=%s' % (x,y)
        return 2 * x + y
    
    z = functools.reduce(f, [0,1,2,3])
    
    print z
    
    
    class a:
        x=1
        
    class b:
        x=2
        
    class c(a,b):
        pass
    
    y = c().x
    
    print y
    
    def f(x):
        print x
        
    for x in xrange(5):
        if 0 < f(x) < 10:
            continue
    
    
    y = {1,2,3,5,6,11}
    y.add(7)
    z=len(y)
    print z
    
    print isinstance(Exception, object)
    
    print (lambda x,y:2*x+y)(2,3)

    y = 0
    for x in xrange(10):
        if (4 < x < 8):
            y = y + x
            
    print y


    class cl:
        __x = 22
        
    c = cl()
    
    c._cl__x

    if None:
        x=1
    elif []:
        x=2
    elif -1:
        x=3
    else:
        x=4
        
    print x

y = {x:2*x+1 for x  in xrange(20)}
z = max(y.keys())
print z

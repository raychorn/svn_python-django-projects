from vyperlogix.misc import ObjectTypeName

class CooperativeAbstract(type):
    """Metaclass implementing cooperative methods. Works
    well for methods returning None, such as __init__"""
    def __init__(cls,name,bases,dic):
        for meth in getattr(cls,'__cooperative__',[]): 
            setattr(cls,meth,cls.coop_method(meth,dic.get(meth)))
    def coop_method(cls,name,method): # method can be None
        """Calls both the superclass method and the class method (if the 
        class has an explicit method). Implemented via a closure"""
        def _(self,*args,**kw):
            getattr(super(cls,self),name)(*args,**kw) # call the supermethod
            if method: method(self,*args,**kw) # call the method
        return _

class CooperativeBase(object):
    __metaclass__=CooperativeAbstract
    __cooperative__=['__init__']
    
if (__name__ == '__main__'):
    from vyperlogix.misc import ObjectTypeName
    
    class _A(object):
        def __init__(self, *args):
            print '_A.__init__',args
    
    class A(CooperativeBase):
        def __init__(self, *args):
            print 'A.__init__',args
    
    class B1(CooperativeBase):
        def __init__(self, *args):
            print 'B1.__init__',args

        def test(self, *args):
            print 'B1.%s.__init__' % (ObjectTypeName.objectSignature(self)),args
            
    class B2(CooperativeBase):
        def __init__(self, *args):
            print 'B2.__init__',args
    
    class B(A, B1, B2, _A):
        def __init__(self, *args):
            print 'B.__init__',args
    
    class C(B):
        def __init__(self, *args):
            print 'C.__init__',args
            super(C,self).test(1,2,3)
    
    C()

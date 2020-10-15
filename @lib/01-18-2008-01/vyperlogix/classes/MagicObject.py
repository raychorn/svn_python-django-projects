__copyright__ = """\
(c). Copyright 2008-2011, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
from vyperlogix import misc
from vyperlogix.classes.CooperativeClass import Cooperative

class MagicObject(Cooperative):

    def __call__(self,*args,**kwargs):
        return MagicObject.__dict__['_stop'](self,self.n,*args,**kwargs)

    def __getattr__(self,name):
        if name in ('__str__','__repr__'): return lambda:'instance of %s at %s' % (str(self.__class__),id(self))
        if not self.__dict__.has_key('n'):self.n=[]
        self.n.append(name)
        return self

    def _stop(self,n,*args,**kwargs):
        self.n=[]
        return self.default(n,*args,**kwargs)

    def default(self,n,*args,**kwargs):
        return 'stop',n,args,kwargs

class MagicObject2(MagicObject):
    '''
    This object knows how to deal with an arbitrary set of method invocations all the while making it possible to
    interpret the actions at a later time.
    
    self.__reset_magic__() should be called after the magic has been retrieved.
    
    The life-cycle is as follows:
    
    (1). Allow object to gather magic.
    (2). Tell object to interpret magic.
    (3). Issue self.__reset_magic__ to reset the magic for the next iteration.
    
    This is useful for XMLRPC applications where a proxy object handles an arbitrary number of method calls.
    
    The only down-side is that the consumer of this object must know when it can interpret the magic.  This is 
    not so much a problem when a Proxy object is using a MagicObject2 subclass because the primary proxy object
    will known when it is time to interpret the magic.
    
    A "simple" use-case scenario would be to simply implement the __call__() method in a sub-class to allow
    a single-level method call to be captured rather than an arbitrarily deep set of method invocations.
    
    You can either code the following to process the current level of magic:
    magic = super(SalesForceObjectProxy, self).__call__(*args,**kwargs)
    
    Or do the following to process only the current level of magic:
    self.n # this is the method name and *args,**kwargs has the arguments when the __call_() method is issued.
    '''
    
    def __init__(self, **kwargs):
        self.__reset_magic__()

    def __store_magic__(self,magic):
        self.__magic__ = magic

    def __reset_magic__(self):
        self.n = []
        self.__magic__ = None

    def __start__(self):
        self.__reset_magic__()

    def __stop__(self):
        self.__reset_magic__()

    def __call__(self,*args,**kwargs):
        items = []
        items.append(args)
        items.append(kwargs)
        n = self.n
        if (misc.isList(n)):
            self.__store_magic__({n[0]:{n[-1]:tuple(items)}})
        else:
            self.__store_magic__({n:tuple(items)})
        return self.__magic__

#############################################################333

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
import os, sys

from vyperlogix.misc import ObjectTypeName

_unpack_ = lambda s:s[0] if (isList(s) and len(s) == 1) else s
__unpack__ = lambda s:s[0] if (isList(s) and len(s) > 0) else s

def asCSV(item,allowEmptyCells=True):
    return ','.join(['"%s"'%(t) for t in item if (allowEmptyCells) or (len(str(t)) > 0)]) if (isinstance(item,tuple)) or (isinstance(item,list)) else item

#from vyperlogix.decorators import TailRecursive
#@TailRecursive.tail_recursion
#def flatten(s,t):
    #for item in s:
	#if (isList(item)) or (isIterable(item)):
	    #l = item
	    #if (not isList(item)):
		#l = list(item)
	    #flatten(l,t)
	#else:
	    #t.append(item)

def normalize_as_float(val):
    _val = val
    try:
	_val = float(_val)
    except:
	pass
    return _val

def isValidFolder(s):
    return isString(s) and os.path.exists(s) and os.path.isdir(s)

def isValidFile(s):
    return isString(s) and os.path.exists(s) and os.path.isfile(s)

def isString(s):
    return (isinstance(s,str)) or (isinstance(s,unicode))

def isBoolean(s):
    return (isinstance(s,bool))

def isBooleanString(s):
    d = {'True': True, 'False': False,}
    t = str(s).lower().capitalize()
    if (isString(t) and (t in d.keys())):
	return d[t]
    return False

def isInteger(s):
    return (isinstance(s,int))

def isDate(s):
    from datetime import date
    return isinstance(s,date)

def isSimpleDict(s):
    return (isinstance(s,dict))

def isDict(s):
    _has_key = False
    try:
	_has_key = callable(s.has_key)
    except:
	_has_key = False
    return (isSimpleDict(s)) or (_has_key)

def isList(obj):
    try:
        return callable(obj.append)
    except:
        pass
    return False

def isIterable(obj):
    try: 
        return hasattr(obj,'__iter__')
    except TypeError: 
        return False

def clone(l):
    return copy(l)

def append(l,item):
    l.append(item)
    return l

def copy(l):
    return [item for item in l]

def findAllContaining(lst,s_search,callback=None,returnIndexes=False,returnOne=False):
    def doCallback(_item,_callback):
        try:
            return _callback(_item,s_search)
        except:
            pass
        return False
    i = 0
    l = []
    if (isString(s_search)) or (ObjectTypeName.typeClassName(s_search) == '_sre.SRE_Pattern'):
        compare_func_string = lambda item,search:item.find(search) > -1
        compare_func_re = lambda item,search:search.search(item)
        compare_func = compare_func_string
        if (ObjectTypeName.typeClassName(s_search) == '_sre.SRE_Pattern'):
            compare_func = compare_func_re
        for item in lst:
            if ((compare_func(item,s_search)) if (not callable(callback)) else doCallback(item,callback)):
                l.append(item if (not returnIndexes) else i)
                if (returnOne):
                    break
            i += 1
    return l

def findFirstContaining(lst,s_search,callback=None,returnIndexes=True):
    r = findAllContaining(lst,s_search,callback=callback,returnIndexes=returnIndexes,returnOne=True)
    return -1 if (len(r) == 0) else r[0]

def findAllMatching(lst,s_search,callback=None,returnIndexes=False,returnOne=False):
    def doCallback(_item,_callback):
        try:
            return _callback(_item,s_search)
        except:
            pass
        return False
    i = 0
    l = []
    compare_func_string = lambda item,search:item == search
    compare_func_re = lambda item,search:search.search(item)
    if (isString(s_search)) or (ObjectTypeName.typeClassName(s_search) == '_sre.SRE_Pattern'):
        compare_func = compare_func_string
        if (ObjectTypeName.typeClassName(s_search) == '_sre.SRE_Pattern'):
            compare_func = compare_func_re
        for item in lst:
            if (compare_func(item,s_search) if (not callable(callback)) else doCallback(item,callback)):
                l.append(item if (not returnIndexes) else i)
                if (returnOne):
                    break
            i += 1
    elif (isList(s_search)):
        for i in xrange(0,len(lst)-len(s_search)):
            if (lst[i:i+len(s_search)] == s_search):
                l.append(s_search if (not returnIndexes) else i)
                if (returnOne):
                    break
    else: # to allow for any type of search to be performed even when strings are not being used...
        compare_func = compare_func_string
        if (ObjectTypeName.typeClassName(s_search) == '_sre.SRE_Pattern'):
            compare_func = compare_func_re
        for item in lst:
            if (compare_func(item,s_search) if (not callable(callback)) else doCallback(item,callback)):
                l.append(item if (not returnIndexes) else i)
                if (returnOne):
                    break
            i += 1
    return l

def findFirstMatching(lst,s_search,callback=None,returnIndexes=True):
    r = findAllMatching(lst,s_search,callback=callback,returnIndexes=returnIndexes,returnOne=True)
    return -1 if (len(r) == 0) else r[0]

def insert(lst,index,value):
    try:
        lst.insert(index,value)
        return lst
    except:
        pass
    return lst

def insertCopy(lst,index,value):
    try:
        _lst = [i for i in lst]
        return insert(_lst,index,value)
    except:
        pass
    return lst

def reverse(l):
    try:
        ll = copy(l)
        ll.reverse()
        return ll
    except:
        pass
    return l

def reverseCopy(l):
    try:
        _l = [i for i in l]
        return reverse(_l)
    except:
        pass
    return l

def reverseDigitsList(foo):
    try:
        return ''.join([t.strip() for t in str(reverse(eval(foo) if (isString(foo)) else foo)).split()])
    except:
        return None

def sort(l):
    try:
        l.sort()
        return l
    except:
        pass
    return l

def sortCopy(l):
    try:
        _l = [i for i in l]
        return sort(_l)
    except:
        pass
    return l

def funcName():
    """ get name of function """
    import sys
    return sys._getframe(1).f_code.co_name

def callersName():
    """ get name of caller of a function """
    import sys
    return sys._getframe(2).f_code.co_name

def findInListSafely(l,item):
    try:
        return l.index(item)
    except:
        pass
    return -1

def formattedException(details='',_callersName=None):
    _callersName = _callersName if (_callersName is not None) else callersName()
    import sys, traceback
    exc_info = sys.exc_info()
    info_string = '\n'.join(traceback.format_exception(*exc_info))
    return '(' + _callersName + ') :: "' + str(details) + '". ' + info_string

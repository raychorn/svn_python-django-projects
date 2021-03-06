__copyright__ = """\
(c). Copyright 1990-2008, Vyper Logix Corp., All Rights Reserved.

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

def getZipFilesAnalysis(_zip,prefix='',_acceptable_types=[]):
    import os
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix.hash import lists

    _analysis = lists.HashedLists()
    try:
	iterable = None
	if (ObjectTypeName.typeClassName(_zip) == 'zipfile.ZipFile'):
	    iterable = (f.filename for f in _zip.filelist)
	elif (lists.isDict(_zip)):
	    iterable = (f for f in _zip.keys())
	for f in iterable:
	    toks = os.path.splitext(f)
	    if (len(_acceptable_types) == 0) or (toks[-1].split('.')[-1] in _acceptable_types) or ( (len(prefix) > 0) and (toks[0].startswith(prefix)) ):
		_analysis[toks[0]] = toks[-1] if (len(toks) > 1) else ''
    except:
	pass
    return _analysis

def getZipFilesAnalysis2(_zip):
    import os
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix.hash import lists

    _analysis = lists.HashedLists2()
    try:
	iterable = None
	if (ObjectTypeName.typeClassName(_zip) == 'zipfile.ZipFile'):
	    iterable = (f.filename for f in _zip.filelist)
	elif (lists.isDict(_zip)):
	    iterable = (f for f in _zip.keys())
	for f in iterable:
	    _analysis[f] = f
    except:
	pass
    return _analysis

def unZipInto(_zip,target,isVerbose=False):
    import os
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix.hash import lists
    from vyperlogix.misc import _utils

    try:
	iterable = None
	typ = ObjectTypeName.typeClassName(_zip)
	if (typ == 'zipfile.ZipFile'):
	    iterable = (f.filename for f in _zip.filelist)
	else:
	    raise AttributeError('Invalid _zip attribute cann be of type "%s".' % (typ))
	print '*** iterable = %s' % (str(iterable))
	for f in iterable:
	    bytes = _zip.read(f)
	    fname = os.path.join(target,f.replace('/',os.sep))
	    if (isVerbose):
		print '%s -> %s' % (f,fname)
	    _utils.writeFileFrom(fname,bytes,mode='wb')
    except Exception, _details:
	if (isVerbose):
	    print _utils.formattedException(details=_details)

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__


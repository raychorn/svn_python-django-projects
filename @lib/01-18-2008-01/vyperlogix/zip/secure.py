from vyperlogix.enum import Enum
from vyperlogix.misc import _utils

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

class ZipType(Enum.Enum):
    none = 0
    zip = 2**0  # no encryption
    ezip = 2**1 # XTEAEncryption using Hex
    xzip = 2**2 # XTEAEncryption using No-Hex
    bzip = 2**3 # Blowfish

def zipper(top,archive_path,archive_type=ZipType.zip,_iv=None,passPhrase=None):
    '''archive_type can be one of ZipType where ezip is an encrypted ZIP file using XTEAEncryption.
    _iv is used for ezip only and must be no more than 8 chars.
    passPhrase is used for bzip only.
    '''
    import os, sys, zipfile
    from vyperlogix import misc
    from vyperlogix.misc import _utils
    from vyperlogix.crypto import XTEAEncryption
    from vyperlogix.crypto import blowfish
		
    print >>sys.stderr, 'archive_type.name=%s, archive_type.value=%s.' % (archive_type.name,archive_type.value)
    if (archive_type.value == ZipType.ezip.value):
	if ( (_iv is None) or (len(_iv) < 8) ):
	    print >>sys.stderr, 'Cannot run %s using source as "%s" and target as "%s" due to the _iv which is "%s".' % (misc.funcName(),top,archive_path,_iv)
	    return
    if (archive_type.value == ZipType.bzip.value):
	if ( (passPhrase is None) or (len(passPhrase) < 8) ):
	    print >>sys.stderr, 'Cannot run %s using source as "%s" and target as "%s" due to the passPhrase which is "%s".' % (misc.funcName(),top,archive_path,passPhrase)
	    return
    if (archive_type.value == ZipType.ezip.value):
	_iv = XTEAEncryption.iv(_iv)
    
    def add_to_zip(baton, dirname, names):
	'''Make this more efficient by using a list to hold all the file names.'''
	zp = baton[0]
	root = os.path.join(baton[1], '')
    
	for file in names:
	    path = os.path.join(dirname, file)
	    if os.path.isfile(path):
		if (archive_type.value == ZipType.ezip.value) or (archive_type.value == ZipType.xzip.value) or (archive_type.value == ZipType.bzip.value):
		    bytes = _utils.readFileFrom(path,mode='rb')
		    if (archive_type.value == ZipType.ezip.value):
			bytes = XTEAEncryption._encryptode(bytes,_iv)
		    elif (archive_type.value == ZipType.xzip.value):
			bytes = XTEAEncryption.f_encryptode(bytes,_iv)
		    elif (archive_type.value == ZipType.bzip.value):
			bytes = blowfish.encryptData(bytes,passPhrase)
		    print >>sys.stderr, '--> %s' % (path[len(root):])
		    zp.writestr(path[len(root):],bytes)
		elif (archive_type.value == ZipType.zip.value):
		    zp.write(path, path[len(root):])
	    elif os.path.isdir(path) and os.path.islink(path):
		os.path.walk(path, add_to_zip, (zp, path))
    
    parts = list(os.path.splitext(archive_path))
    parts[-1] = '.%s' % (archive_type.name)
    archive_path = ''.join(parts)
    zp = zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=_utils.isUsingWindows)
    try:
	os.path.walk(top, add_to_zip, (zp, top))
    finally:
	print >>sys.stderr, 'Closing %s' % (zp.filename)
	zp.close()
	
def unzipper(archive_path,dest,archive_type=ZipType.zip,_iv=None,passPhrase=None):
    '''archive_type can be one of ZipType where ezip is an encrypted ZIP file using XTEAEncryption.'''
    import os, sys, zipfile
    from vyperlogix import misc
    from vyperlogix.misc import _utils
    from vyperlogix.crypto import XTEAEncryption
    from vyperlogix.crypto import blowfish
		
    if (archive_type.value == ZipType.ezip.value) and ( (_iv is None) or (len(_iv) < 8) ):
	print >>sys.stderr, 'Cannot run %s using source as "%s" and target as "%s" due to the _iv which is "%s".' % (misc.funcName(),top,archive_path,_iv)
	return
    if (archive_type.value == ZipType.bzip.value) and ( (passPhrase is None) or (len(passPhrase) < 8) ):
	print >>sys.stderr, 'Cannot run %s using source as "%s" and target as "%s" due to the passPhrase which is "%s".' % (misc.funcName(),top,archive_path,passPhrase)
	return
    if (archive_type.value == ZipType.ezip.value):
	_iv = XTEAEncryption.iv(_iv)
    
    parts = list(os.path.splitext(archive_path))
    parts[-1] = '.%s' % (archive_type.name)
    archive_path = ''.join(parts)
    zp = zipfile.ZipFile(archive_path, 'r', zipfile.ZIP_DEFLATED, allowZip64=_utils.isUsingWindows)
    try:
	_files = zp.filelist
	i = 1
	n = len(_files)
	for f in _files:
	    bytes = zp.read(f.filename)
	    if (archive_type.value == ZipType.ezip.value):
		bytes = XTEAEncryption._decryptode(bytes,_iv)
	    elif (archive_type.value == ZipType.xzip.value):
		bytes = XTEAEncryption.f_decryptode(bytes,_iv)
	    elif (archive_type.value == ZipType.bzip.value):
		bytes = blowfish.decryptData(bytes,passPhrase)
	    print >>sys.stderr, '%s of %s --> %s' % (i,n,f.filename)
	    _utils.writeFileFrom(os.sep.join([dest,f.orig_filename.replace('/',os.sep)]),bytes,mode='wb')
	    i += 1
    except Exception, details:
	print >>sys.stderr, 'ERROR: Cannot read the file named "%s" due to "%s".' % (archive_path,str(details))
	import traceback
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	print >>sys.stderr, info_string
    finally:
	print >>sys.stderr, 'Closing %s' % (zp.filename)
	zp.close()

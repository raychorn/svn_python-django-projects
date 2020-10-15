import gzip, zlib, base64

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

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

def decompress_zlib(s):
    return zlib.decompress(base64.decodestring(s), 15)

def zlib_compress(s):
    return base64.encodestring(zlib.compress(s, 9))

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    #print 'Test #1'
    #s = 'This is the source string.'
    #z = zlib_compress(s)
    #sz = decompress_zlib(z)
    #assert s == sz, 'Oops, something went horribly wrong with the system.'
    #print z
    #print sz
    
    #print '='*80

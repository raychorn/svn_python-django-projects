from vyperlogix.oodb import *

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

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    val = 'FF'*100
    print "hex2dec('%s')\n=%s" % (val,hex2dec(val))

    import cProfile
    
    def test01():
        val = ''.join([dec2hex(n) for n in xrange(255)])
        for i in xrange(10000):
            bool = isHexDigits(val)
            if (not bool):
                print 'Test Failed !'
                break
        print 'isHexChars(%s)=(%s)' % (val,isHexDigits(val))
    
    print "dec2hex(255)  =", dec2hex(255)    # FF
    print "hex2dec('FF') =", hex2dec('FF')   # 255

    print "dec2hex(0)  =", dec2hex(0)    # 00
    print "dec2hex(1)  =", dec2hex(1)    # 01
    
    cProfile.run('test01()')
    print
    
    print "hex(255) =", hex(255)                # 0xff
    print "hex2dec('0xff') =", hex2dec('0xff')  # 255


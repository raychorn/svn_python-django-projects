from vyperlogix.oodb import *
import random

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

    d = {}
    d['../spam-useStrings.db'] = PickleMethods.useStrings
    d['../spam-useBsdDbShelf.db'] = PickleMethods.useBsdDbShelf
    d['../spam-useMarshal.db'] = PickleMethods.useMarshal
    d['../spam-useSafeSerializer.db'] = PickleMethods.useSafeSerializer
    
    for k,v in d.iteritems():
	ph = PickledHash(k,v)
	print 'ph=(%s)' % str(ph)
	for k, v in ph.iteritems():
	    del ph[k]
	assert len(ph) == 0, 'Oops, something went wrong with the initialization because there should not be any keys in this database at this time.'
	for i in xrange(100):
	    k = '%d'%random.choice(xrange(10))
	    ph[k] = ph.listify(k,str(i))
	for k, v in ph.iteritems():
	    assert isinstance(v,list), 'Oops, something is wrong with the listification process because the key "%s" should have stored a list of values but it stored a type of "%s".' % (k,v.__class__)
	    print '%s=(%s)\t\t(%s)' % (k, v, str(v.__class__))
	print '='*80
	for i in xrange(11):
	    ph['%d'%i] = '%d'% (i*i)
	for i in xrange(11,15):
	    ph['%d'%i] = [i*i]
	print 'ph.keys()=(%s)' % str(ph.keys())
	for k, v in ph.iteritems():
	    print '%s=(%s)\t\t(%s)' % (k, v, str(v.__class__))
	del ph['11']
	assert not ph.has_key('11'), 'Oops, something went wrong with the record deletion function.'
	print '+'*50
	print 'Record at key # 11 should be gone.'
	print '+'*50
	for k, v in ph.iteritems():
	    print '%s=(%s)\t\t(%s)' % (k, v, str(v.__class__))
	ph.sync()
	ph.close()

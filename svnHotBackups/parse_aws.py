import os, sys

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix import misc
from vyperlogix.misc import _utils

import math
from vyperlogix.classes.SmartObject import SmartFuzzyObject

__path__ = ''  #'./sample-aws-ls.txt'

__data__ = []

def is_valid_file(fname):
    _isString_ =  misc.isString(fname)
    _fname_ =  os.path.abspath(fname) if (_isString_) else fname
    return  _fname_ if (_isString_ and os.path.exists(_fname_) and  os.path.isfile(_fname_)) else None

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--source=?':'path to the source.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
	
	_isVerbose = __args__.get_var('isVerbose',misc.isBooleanString,False)
	_isDebug = __args__.get_var('isDebug',misc.isBooleanString,False)
	_isHelp = __args__.get_var('isHelp',misc.isBooleanString,False)

	print 'DEBUG: _isVerbose=%s' % (_isVerbose)
	print 'DEBUG: _isDebug=%s' % (_isDebug)
	print 'DEBUG: _isHelp=%s' % (_isHelp)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	_source_path = __args__.get_var('source',is_valid_file,__path__)
	__path__ = _source_path

	print 'DEBUG: __path__=%s' % (__path__)
	
	if (os.path.exists(__path__)):
	    if (os.path.isfile(__path__)):
		_lines_ =  [l for l in _utils.readFileFrom(__path__, noCRs=False).split('\n') if (len(l) > 0)]
		_guide_ =  _lines_[0].split('+')
		_columns_ =  _lines_[1].split('|')
		_num_columns_ =  len(_columns_)
		if (len(_guide_) == _num_columns_):
		    _columns_ =  [c.strip() for c in _columns_]  # if (len(c.strip()) > 0)
		    _num_lines_ = len(_lines_)
		    _width_ = int(math.floor(math.log10(_num_lines_)))
		    _fmt_ = '#%' + ('0%d' % (_width_ + 1)) + 'd'
		    for lineNum in xrange(3, _num_lines_-1):
			aLine =  _lines_[lineNum]
			_aLine_ =  [c.strip() for c in aLine.split('|')]
			if (_num_columns_ == len(_aLine_)):
			    _tt_ = []
			    for i in xrange(0, len(_aLine_)):
				if (len(_columns_[i]) > 0):
				    _tt_.append(tuple([_columns_[i], _aLine_[i]]))
			    __data__.append(SmartFuzzyObject(args=dict(_tt_)))
			else:
			    print 'WARNING: Looks like "%s" is not a valid aws ls file at line #%d.' % (__path__, lineNum)
		else:
		    print 'WARNING: Looks like "%s" is not a valid aws ls file.' % (__path__)
		pass
	    else:
		print 'WARNING: Looks like "%s" is not a file.' % (__path__)
	else:
	    print 'WARNING: Cannot determine the location of "%s".' % (__path__)
	print __data__
	
import re
import os, sys

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix import misc
from vyperlogix.misc import _utils

__path__ = '/var/local/svn/#svn_backups/repo1'

__re__ = re.compile("_(0[1-9]|[12][0-9]|3[01])[- /.]([0-9][0-9])[- /.](19|20)[0-9]{2}_[0-9]{2}[0-9]{2}[0-9]{2}_")

#__archiveTypes__ = ['.tar.gz', '.tar.bz2', '.zip', '.ezip', '.bzip', '.xzip']

if (__name__ == '__main__'):
    def ppArgs():
        pArgs = [(k,args[k]) for k in args.keys()]
        pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
        pPretty.pprint()

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff.',
            '--reduce':'reduce the number of files by one.',
            '--repo-path=?':'path to the SVN repo.',
            }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
        ppArgs()
    else:
        _progName = __args__.programName

        _isVerbose = __args__.get_var('isVerbose',misc.isBooleanString,False)
        _isDebug = __args__.get_var('isDebug',misc.isBooleanString,False)
        _isReduce = __args__.get_var('isReduce',misc.isBooleanString,False)
        _isHelp = __args__.get_var('isHelp',misc.isBooleanString,False)

        print 'DEBUG: _isVerbose=%s' % (_isVerbose)
        print 'DEBUG: _isDebug=%s' % (_isDebug)
        print 'DEBUG: _isReduce=%s' % (_isReduce)
        print 'DEBUG: _isHelp=%s' % (_isHelp)

        if (_isHelp):
            ppArgs()
            sys.exit()

        _repo_path = __args__.get_var('repo-path',misc.isString,__path__)
        __path__ = _repo_path

        print 'DEBUG.1: __path__=%s' % (__path__)

        if (os.path.exists(__path__)):
            if (os.path.isdir(__path__)):
                __count__ = 0
                __retirees__ = []
                print 'DEBUG.2: __path__=%s' % (__path__)
                for top, dirs, files in _utils.walk(__path__, topdown=True, onerror=None, rejecting_re=None):
                    if (top == __path__):
                        print 'BEGIN: dirs'
                        for d in dirs:
                            print '%s' % (d)
                        print 'END!:  dirs'
                        _dirs = [d for d in dirs if __re__.match(d)]
                        print 'DEBUG.2.1: top=%s, _dirs=%s, files=%s, __count__=%d' % (top, _dirs, files, __count__)
                        for d in _dirs:
                            _top = os.sep.join([top, d])
                            _files = os.listdir(_top)
                            print 'DEBUG.2.2: _top=%s, _files=%s' % (_top, _files)
                            if (len(_files) == 0):
                                print 'DEBUG.3: Remove this folder "%s" because there are no files.' % (_top)
                                __retirees__.append(_top)
                            else:
                                print 'DEBUG.4: len(_files)=%s' % (len(_files))
                                if (_isReduce) and (len(_files) == 1):
                                    print 'DEBUG.4.1: _isReduce=%s' % (_isReduce)
                                    for f in _files:
                                        _fname = os.sep.join([_top, f])
                                        print 'DEBUG.5: Reducing "%s".' % (_fname)
                                        os.remove(_fname)
                                    _isReduce = False
                                __count__ += len(files)
                                print 'DEBUG.6: top=%s, dirs=%s, files=%s, __count__=%d' % (top, dirs, files, __count__)
                    else:
                        break
                print 'DEBUG.7: There are %s files that will remain.' % (__count__)
                print 'BEGIN:'
                for f in __retirees__:
                    try:
                        if (os.path.exists(f)) and (os.path.isdir(f)):
                            print 'Removing "%s".' % (f)
                            os.rmdir(f)
                        else:
                            print 'DEBUG.8: Cannot locate "%s" or is not a directory.' % (f)
                    except Exception, ex:
                        print 'WARNING: %s' % (_utils.formattedException(details=ex))
                print 'END!'
            else:
                print 'WARNING: Looks like "%s" is not a directory.' % (__path__)
        else:
            print 'WARNING: Cannot determine the location of "%s".' % (__path__)

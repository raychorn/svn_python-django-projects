import os
import sys
from vyperlogix.hash import lists

from vyperlogix.classes import SmartObject
from vyperlogix.classes.CooperativeClass import Cooperative

__copyright__ = """\
(c). Copyright 1990-2008, Vyper Logix Corp., 

                   All Rights Reserved.

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

def ppArgs(self):
    from vyperlogix.misc import PrettyPrint
    
    pArgs = [(k,self.args[k]) for k in self.args.keys()]
    pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
    pPretty.pprint()

class Args(Cooperative):
    def __init__(self,args):
        self.args = lists.HashedLists2(args) if (isinstance(args,dict)) else args
        self.dArgs = lists.HashedLists2()
        self.arguments = lists.HashedLists2()
        self.dValues = lists.HashedLists2()
        self.booleans = lists.HashedLists2()
        self.programName = sys.argv[0].split(os.sep)[-1]
        self._programName = (self.programName.split('.'))[0]
        self.__vars__ = SmartObject.SmartFuzzyObject()
        for k,v in self.args.iteritems():
            toks = k.split('=')
            if ( (len(toks) == 2) or (k.endswith('=')) ):
                self.arguments[toks[0].lower()] = ''
                self.dArgs[toks[0].lower()] = toks[-1]
                b = v.find('[')
                e = v.find(']')
                if (b > -1) and (e > -1):
                    _v = v[b+1:e-1]
                    t_v = _v.split(',')
                    v = '[%s]' % ','.join(['"%s"' % (t) for t in t_v])
                self.dValues[toks[0].lower()] = v
            else:
                self.arguments['is'+toks[0].replace('--','').title()] = ''
        for arg in sys.argv[1:]:
            toks = arg.split('=')
            if ( (len(toks) == 2) or (arg.endswith('=')) ):
                # Arguments...
                argName = self.stripBeginningNonAlphaNumericsFrom(toks[0]).lower()
                self.arguments[argName] = toks[-1]
                self.__vars__[argName] = self.arguments[argName]
            else:
                # Booleans...
                argName = 'is'+self.upperCaseLikeTitle(toks[0].replace('--',''))
                self.booleans[argName] = True
                self.__vars__[argName] = True

    def upperCaseLikeTitle(self,s):
        if (len(s) < 2):
            return s[0].upper()
        return s[0].upper()+s[1:]

    def stripBeginningNonAlphaNumericsFrom(self,s):
        while ( (len(s) > 0) and (not s[0].isalpha()) and (not s[0].isdigit()) ):
            s = s[1:]
        return s

    def __repr__(self):
        return 'Args for "%s"\n\t%s\n\t%s' % (self.programName,str(self.arguments),str(self.booleans))

    def vars():
        doc = "vars - the variables for the various options being tested."
        def fget(self):
            return self.__vars__
        return locals()
    vars = property(**vars())

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    #from vyperlogix import misc
    
    #def main():
        #print '%s' % (misc.funcName())

    #from vyperlogix.misc import _psyco
    #_psyco.importPsycoIfPossible(func=main)

    #from vyperlogix.misc import Args

    #args = {'--help':'show some help.',
            #'--verbose':'output more stuff.',
            #'--delete':'delete the specified keypath.',
            #'--input=?':'the name of the file being read.',
            #}
    #_argsObj = Args.Args(args)

    #_progName = _argsObj.programName

    #if (_argsObj.vars.isVerbose):
        #print '_argsObj=(%s)' % str(_argsObj)

    #if (_argsObj.vars.isHelp):
        #Args.ppArgs()
    #else:
        #main()

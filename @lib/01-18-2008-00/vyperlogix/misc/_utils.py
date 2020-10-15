import os, sys, stat
from vyperlogix.decorators import TailRecursive

isBeingDebugged = False if (not os.environ.has_key('WINGDB_ACTIVE')) else int(os.environ['WINGDB_ACTIVE']) == 1
isVerbose = False

isUsingWindows = (sys.platform.find('win') > -1)
isNotUsingLocalTimeConversions = not isUsingWindows
isUsingLocalTimeConversions = not isNotUsingLocalTimeConversions

seconds_per_hour = 60 * 60

isComputerAllowed = True

ascii_only = lambda s:''.join([ch for ch in s if (ord(ch) >= 32) and (ord(ch) <= 127)])

alpha_numeric_only = lambda s:''.join([ch for ch in str(s) if (str(ch).isalnum())])

numerics_only = lambda s:''.join([ch for ch in str(s) if (str(ch).isdigit())])

quote_it = lambda arg:'"' if (not str(arg).isdigit()) and ( (not isinstance(arg,(list,tuple))) and (not lists.isDict(arg)) ) else ''

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

from vyperlogix.hash import lists
windows_modes = ['S_IREAD','S_IWRITE']
all_modes = lists.HashedLists({'S_ISUID':stat.S_ISUID,
                               'S_ISGID':stat.S_ISGID,
                               'S_ENFMT':stat.S_ENFMT,
                               'S_ISVTX':stat.S_ISVTX,
                               'S_IREAD':stat.S_IREAD,
                               'S_IWRITE':stat.S_IWRITE,
                               'S_IEXEC':stat.S_IEXEC,
                               'S_IRWXU':stat.S_IRWXU,
                               'S_IRUSR':stat.S_IRUSR,
                               'S_IWUSR':stat.S_IWUSR,
                               'S_IXUSR':stat.S_IXUSR,
                               'S_IRWXG':stat.S_IRWXG,
                               'S_IRGRP':stat.S_IRGRP,
                               'S_IWGRP':stat.S_IWGRP,
                               'S_IXGRP':stat.S_IXGRP,
                               'S_IRWXO':stat.S_IRWXO,
                               'S_IROTH':stat.S_IROTH,
                               'S_IWOTH':stat.S_IWOTH,
                               'S_IXOTH':stat.S_IXOTH
                               })
if (sys.platform == 'win32'):
    retire = set(all_modes.keys()) - set(windows_modes)
    for k in retire:
        del all_modes[k]
_all_modes = lists.HashedLists(all_modes.asDict(insideOut=True,isCopy=True))

windows_mask = 0
for item in windows_modes:
    v = all_modes[item]
    if (isinstance(v,list)):
        for _item in v:
            windows_mask |= _item
    else:
        windows_mask |= v

parse_key_value_pairs_as_dict = lambda params:lists.HashedLists2(dict([tuple(t) for t in [p.split('=') for p in params.split('\n') if (len(p) > 0)] if (len(t) == 2)]))

def is_ip_address_valid(ip):
    '''127.0.0.1 is the general form of an IP address'''
    toks = ip.split('.')
    return (len(toks) == 4) and all([str(n).isdigit() for n in toks])

def eat_leading_token_if_empty(url,delim='/'):
    toks = [t for t in url.split(delim) if (len(t) > 0)]
    return '/'.join(toks)

def get_dict_as_pairs(toks):
    try:
        from vyperlogix.iterators.iterutils import itergroup
        n = len(toks)
        i = int(n / 2) * 2
        d = lists.HashedLists2(dict([t for t in itergroup(toks[n-i:],2)]))
        if ((n % 2) != 0):
            d = lists.HashedLists2({toks[0]:lists.HashedLists2(d.asDict())})
        return d
    except:
        return lists.HashedLists2({})

def asMessage(reason):
    from vyperlogix import misc
    return '(%s) %s.' % (misc.callersName(),reason)

def getVersionNumber():
    import sys
    return int(''.join(sys.version.split()[0].split('.')))

def cleanup_sqlautocode(fname):
    '''Cleans-up the sqlautocode process by removing all those "\r" chars that get in the way of consuming the code.'''
    from vyperlogix import misc
    fIn = open(fname,'r')
    ext = fname.split('.')[-1]
    fOut = open(fname.replace(ext,ext+'_bak'),'w')
    _count = 0
    try:
        while (1):
            l = fIn.readline()
            if (l == ''):
                break
            toks = l.split('\r')
            fOut.writelines([''.join(toks)])
            _count += 1
    finally:
        fOut.flush()
        fOut.close()
        fIn.close()
        print '%s :: Processed %d lines.' % (misc.funcName(),_count)
        os.remove(fIn.name)
        os.rename(fOut.name,fIn.name)
        print '%s :: Done !' % (misc.funcName())

@TailRecursive.tail_recursion
def safely_remove(fname_or_dirname):
    import os
    if (os.path.isdir(fname_or_dirname)):
        files = [os.sep.join([fname_or_dirname,f]) for f in os.listdir(fname_or_dirname)]
        for f in files:
            safely_remove(f)
    else:
        if (os.path.exists(fname_or_dirname)):
            os.remove(fname_or_dirname)

def safely_mkdir(fpath='.',dirname='logs'):
    import os

    _path = os.path.abspath(os.sep.join([fpath,dirname]))
    if (not os.path.exists(_path)):
        try:
            os.mkdir(_path)
        except:
            os.makedirs(_path)
    return _path

def safely_mkdir_logs(fpath='.'):
    return safely_mkdir(fpath=fpath,dirname='logs')

def getFloatVersionNumber():
    import sys
    v = sys.version.split()[0].split('.')
    v.insert(1,'.')
    return float(eval(''.join(v)))

def getProgramName():
    import os, sys
    return os.path.basename(sys.argv[0]).split('.')[0]

def getComputerName():
    import socket
    return socket.gethostbyname_ex(socket.gethostname())[0]

def isComputerAllowed(domain_name):
    '''domain_name is either a name (string) or list of names...'''
    from vyperlogix import misc
    global _isComputerAllowed
    domain_names = domain_name if (misc.isList(domain_name)) else [domain_name]
    cname = getComputerName().lower()
    _isComputerAllowed = (any([cname.find(c.lower()) > -1 for c in domain_names]))
    return _isComputerAllowed

def listify(maybe_list):
    """
    Ensure that input is a list, even if only a list of one item
    @maybeList: Item that shall join a list. If Item is a list, leave it alone
    """
    try:
        return list(maybe_list)
    except:
        return list(str(maybe_list))

    return maybe_list

def failUnlessEqual(first, second, msg=None):
    """Fail if the two objects are unequal as determined by the '=='
       operator.
    """
    if not first == second:
        raise AssertionError, (msg or '%r != %r' % (first, second))

def failIfEqual(first, second, msg=None):
    """Fail if the two objects are equal as determined by the '=='
       operator.
    """
    if first == second:
        raise AssertionError, (msg or '%r == %r' % (first, second))

def booleanize(data):
    return True if str(data).lower() in ['true','1','yes'] else False

def environ_copy():
    _env = {}
    for k,v in os.environ.iteritems():
        _env[k] = v
    return _env

def expandEnvMacro(p):
    import os

    toks = p.split(os.sep)
    _toks = []
    for t in toks:
        if (t.startswith('%') and t.endswith('%')):
            _t = t.replace('%','')
            if (os.environ.has_key(_t)):
                t = os.environ[_t]
        _toks.append(t)
    return os.sep.join(_toks)

def homeFolder():
    """ home folder for current user """
    import os, sys
    f = os.path.abspath(os.curdir)
    toks = f.split(os.sep)
    if (sys.platform == 'win32'):
        t = toks[0:2]
    else:
        t = toks[0:3]
    return os.sep.join(t)

from vyperlogix.enum.Enum import Enum

class FileFolderSearchOptions(Enum):
    none = 0
    callback_files = 2**0
    callback_folders = 2**1
    skip_svn = 2**2

def containsSvnFolders(top):
    import re
    svn_regex = re.compile('[._]svn')
    for root, dirs, files in os.walk(top, topdown=True):
	if (svn_regex.search(root)):
	    return True
    return False

def _searchForFileOrFolderNamed(fname,top='/',isFile=False,callback=None,options=FileFolderSearchOptions.none):
    """ Search for a folder of a specific name """
    import os, re
    _target = '.'+fname.split('.')[-1]
    svn_regex = re.compile('[._]svn')
    for root, dirs, files in os.walk(top, topdown=True):
        if (options.value & FileFolderSearchOptions.skip_svn.value) and (svn_regex.search(root)):
            continue
        if (options.value & FileFolderSearchOptions.callback_folders.value) and (callable(callback)):
            try:
                callback(root)
            except Exception, details:
                import sys
                from vyperlogix.misc import _utils
                print >>sys.stderr, _utils.formattedException(details=details)
        if (not isFile):
            if (fname in dirs):
                return os.sep.join([root,fname])
        else:
            if (fname in files):
                return os.sep.join([root,fname])
            elif (fname.startswith('*.')):
                for f in files:
                    if (options.value & FileFolderSearchOptions.callback_files.value) and (callable(callback)):
                        try:
                            callback(root, files)
                        except Exception, details:
                            import sys
                            from vyperlogix.misc import _utils
                            print >>sys.stderr, _utils.formattedException(details=details)
                    if (f.endswith(_target)):
                        return os.sep.join([root,f])
    return ''

def searchForFolderNamed(fname,top='/',callback=None,options=FileFolderSearchOptions.none):
    """ Search for a folder of a specific name """
    return _searchForFileOrFolderNamed(fname,top,False,callback=None,options=options)

def searchForFileNamed(fname,top='/',callback=None,options=FileFolderSearchOptions.none):
    """ Search for a folder of a specific name, fname can contain '*.typ' to search for a file based on a wildcard. """
    return _searchForFileOrFolderNamed(fname,top,True,callback=callback,options=options)

def formatDate_YYYY():
    return '%Y'

def formatDate_MMYYYY():
    return '%m-%Y'

def formatDate_YYYYMMDD_dashes():
    return '%Y-%m-%d'

def formatDate_MMDDYYYY_dashes():
    return '%m-%d-%Y'

def formatDate_MMDDYYYY_slashes():
    return '%m/%d/%Y'

def formatTimeStr():
    return '%Y-%m-%dT%H:%M:%S.000Z'

def formatApacheDateTimeStr():
    return '%d/%b/%Y:%H:%M:%S'

def formatSimpleTimeStr():
    return '%H:%M:%S'

def _formatTimeStr():
    return '%Y-%m-%dT%H:%M:%S'

def _formatShortTimeStr():
    return '%Y-%m-%dT%H:%M'

def formatSalesForceTimeStr():
    return '%Y-%m-%dT%H:%M:%S'

def format_mySQL_DateTimeStr():
    '''2008-11-28 09:52:00'''
    return '%Y-%m-%d %H:%M:%S'

def format_PHPDateTimeStr():
    '''11.28.2008 09:52:00'''
    return '%m.%d.%Y %H:%M:%S'

def formatDjangoDateTimeStr():
    '''01 May 2009 15:26:41 GMT'''
    return u"%d %b %Y %H:%M:%S %Z"

def formatSalesForceDateStr():
    return '%Y-%m-%d'

def formatMySQLDateTimeStr():
    return '%d-%b-%Y %H:%M:%S'

def formatSalesForceDateTimeStr():
    return '%d-%b-%Y %H:%M:%S'

def formatShortDateTimeStr():
    '''Jun 12 04:41'''
    return '%b %d %y %I:%M'

def formatShortDateStr():
    '''Jun 12 2008'''
    return '%b %d %y'

def formatShortBlogDateStr():
    '''Wed, 12 Jun 2008'''
    return '%A, %d %B %Y'

def formatSimpleBlogTimeStr():
    return '%I:%M %p'

def formatMetaHeaderExpiresOn():
    return '%a, %d %b %Y %H:%M:%S'

def reformatSalesForceTimeStr(sTime):
    toks = sTime.split('T')
    toks[-1] = toks[-1].split('.')[0]
    return "%sT%s.000Z" % tuple(toks) # yyyy-MM-ddTHH:mm:ss.SSSZ

def getDatetimeFromApexDatetime(value):
    try:
	return getFromDateTimeStr(value.isoformat().split('+')[0],formatSalesForceTimeStr())
    except:
	pass
    return value

def getSimpleDateFromApexDatetime(value):
    try:
	return value.isoformat().split('+')[0].split('T')[0]
    except:
	pass
    return value

def reformatSalesForceDateStrAsMMDDYYYY(sDate,useSlashes=True):
    from vyperlogix import misc
    sDate = sDate if (misc.isString(sDate)) else str(sDate)
    ts = getFromDateTimeStr(sDate,format=formatSalesForceDateStr())
    _fmt = formatDate_MMDDYYYY_slashes if (useSlashes) else formatDate_MMDDYYYY_dashes
    return getAsSimpleDateStr(ts,fmt=_fmt())

def parms_dict_from_url(s_url):
    '''This function converts a URL that has parms to the right of the "?" into a dict.'''
    try:
        return lists.HashedLists2(dict([tuple(t.split('=')) for t in s_url.split('?')[-1].split('&')]))
    except ValueError, details:
        return lists.HashedLists2()

def utcDelta():
    import datetime, time
    _uts = datetime.datetime.utcfromtimestamp(time.time())
    _ts = datetime.datetime.fromtimestamp(time.time())
    # This time conversion fails under Linux for some odd reason so let's just stick with UTC when this happens.
    _zero = datetime.timedelta(0)
    return _zero if (isNotUsingLocalTimeConversions) else (_uts - _ts if (_uts > _ts) else _ts - _uts)

def localFromUTC(utc):
    d = utcDelta()
    return utc - d

def timeDeltaAsSeconds(td):
    from datetime import timedelta
    if (isinstance(td,timedelta)):
        return float(td.seconds) + float(td.days * 86400) + (float(td.microseconds) / (10**6))
    else:
        logging.warning('Unable to convert timedelta to seconds due to type mismatch, type "%s" should be "%s".' % (type(td),timedelta))
    return -1

def timeDeltaAsReadable(td):
    from vyperlogix import misc
    from datetime import timedelta
    if (isinstance(td,timedelta)):
        s = str(td)
        toks = s.split(':')
        toks[0] = toks[0].split()
        hms = [int(n) for n in [toks[0][-1]]+toks[len(toks)-2:]]
        del toks[len(toks)-2:]
        toks = toks[0]
        del toks[-1]
        for i in [0,2,4]:
            hms.insert(i+1,'s' if (hms[i] == 0) or (hms[i] > 1) else '')
        hms = tuple(hms)
        t = [t for t in ' '.join(toks).split(',') if len(t) > 0]
        if (misc.isList(t)) and (len(t) > 0):
            t = t[0]
        else:
            t = ''
        return t + '%d hour%s %d minute%s %d second%s' % hms
    else:
        logging.warning('Unable to use timedelta due to type mismatch, type "%s" should be "%s".' % (type(td),timedelta))
    return str(td)

def getFromApexDateTime(apex_date_time,fmt=formatSalesForceDateTimeStr()):
    dt = getFromSalesForceDateTimeStr(str(apex_date_time))
    dt = localFromUTC(dt)
    return getAsDateTimeStr(dt,fmt=fmt)

def getFromDateTimeStr(ts,format=_formatTimeStr()):
    from datetime import datetime
    try:
        return datetime.strptime(ts,format)
    except ValueError:
        return datetime.strptime('.'.join(ts.split('.')[0:-1]),format)

def getFromDateStr(ts,format=_formatTimeStr()):
    return getFromDateTimeStr(ts,format=format)

def getFromSimpleDateStr(ts):
    _fmt = formatDate_MMDDYYYY_dashes() if (ts.find('-') > -1) else formatDate_MMDDYYYY_slashes()
    return getFromDateTimeStr(ts,format=_fmt).date()

def getFromSalesForceDateStr(ts):
    _fmt = formatSalesForceTimeStr()
    return getFromDateTimeStr(ts.split('+')[0],format=_fmt).date()

def getFromSalesForceDateTimeStr(ts):
    _fmt = formatSalesForceTimeStr()
    return getFromDateTimeStr(ts.split('+')[0],format=_fmt)

def days_timedelta(num_days=0):
    import datetime
    return datetime.timedelta(num_days)

def strip_time_drom_datetime(dt):
    '''Normalizes the datetime to be the date beginning at midnight.'''
    import datetime
    tm = dt.time()
    delta = datetime.timedelta(days=0, hours=tm.hour, minutes=tm.minute, seconds=tm.second)
    return (dt - delta)

def today_localtime(_timedelta=None,begin_at_midnight=False):
    dt = getFromNativeTimeStamp(timeStampLocalTime())
    begin_at_midnight = False if (not isinstance(begin_at_midnight,bool)) else begin_at_midnight
    if (begin_at_midnight):
        dt = strip_time_drom_datetime(dt)
    try:
        if (_timedelta is not None):
            return dt - _timedelta
    except Exception, details:
        info_string = formattedException(details=details)
        print >>sys.stderr, info_string
    return dt

def todayForSalesForce_localtime(_timedelta=None,begin_at_midnight=False):
    '''begin_at_midnight = True when the goal is to make the date begin at midnight otherwise the local time is used.'''
    dt = today_localtime(_timedelta=_timedelta,begin_at_midnight=begin_at_midnight)
    return reformatSalesForceTimeStr(dt.isoformat())

def truncate_if_necessary(s,max_width=40):
    if (max_width > -1):
        elipsis = '...'
        l_elipsis = len(elipsis)
        normalized_width = max_width - l_elipsis
        is_truncating = s > normalized_width
        return s[0:normalized_width].replace(elipsis,'') + '...' if (is_truncating) else ''
    return s

def isStrDate(ts,format=formatSalesForceDateStr()):
    try:
        dt = getFromDateTimeStr(ts,format=format)
        return True
    except ValueError:
        pass
    return False

def getAsSimpleDateStr(dt,fmt=formatDate_MMDDYYYY_slashes()):
    return dt.strftime(fmt)

def getAsDateTimeStr(value, offset=0,fmt=_formatTimeStr()):
    """ return time as 2004-01-10T00:13:50.000Z """
    import sys,time
    import types
    from datetime import datetime

    strTypes = (types.StringType, types.UnicodeType)
    numTypes = (types.LongType, types.FloatType, types.IntType)
    if (not isinstance(offset,strTypes)):
        if isinstance(value, (types.TupleType, time.struct_time)):
            return time.strftime(fmt, value)
        if isinstance(value, numTypes):
            secs = time.gmtime(value+offset)
            return time.strftime(fmt, secs)

        if isinstance(value, strTypes):
            try: 
                value = time.strptime(value, fmt)
                return time.strftime(fmt, value)
            except Exception, details: 
                info_string = formattedException(details=details)
                print >>sys.stderr, 'ERROR :: getDateTimeTuple Could not parse "%s".\n%s' % (value,info_string)
                _fmt = get_format_from(value)
                secs = time.gmtime(time.time()+offset)
                return time.strftime(fmt, secs)
        elif (isinstance(value,datetime)):
            from datetime import timedelta
            if (offset is not None):
                value += timedelta(offset)
            ts = time.strftime(fmt, value.timetuple())
            return ts
    else:
        print >>sys.stderr, 'ERROR :: offset must be a numeric type rather than string type.'
# END getAsDateTimeStr

def getDayOfYear(dt):
    try:
        return int(dt.strftime("%j"))
    except:
        return -1

def getWeekday(dt):
    try:
        return int(dt.strftime("%w"))
    except:
        return -1

def getWeekdayName(dt):
    try:
        return dt.strftime("%a")
    except:
        return ''

def getFullWeekdayName(dt):
    try:
        return dt.strftime("%A")
    except:
        return ''

def getMonthName(dt):
    try:
        return dt.strftime("%B")
    except:
        return ''

def isWorkWeekDay(dt):
    return (getWeekday(dt) not in [0,6])

def time_to_secs(s):
    hms = s.split(":")     # [hh, mm, ss]
    secs = 0
    for t in hms[0:3]:
        secs = secs * 60 + int(t)
    return secs

def secs_to_time(secs):
    hms = ['00','00','00']
    while secs:
        hms.append('%02d' % (secs % 60))
        secs = secs // 60
    return ":".join(hms[(len(hms)-3):])

def timeSeconds(month=-1,day=-1,year=-1,format=formatSalesForceTimeStr()):
    """ get number of seconds """
    import time, datetime
    fromSecs = datetime.datetime.fromtimestamp(time.time())
    s = getAsDateTimeStr(fromSecs,fmt=format)
    _toks = s.split('T')
    toks = _toks[0].split('-')
    if (month > -1):
	toks[0] = '%02d' % (month)
    if (day > -1):
	toks[1] = '%02d' % (day)
    if (year > -1):
	toks[-1] = '%04d' % (year)
    _toks[0] = '-'.join(toks)
    s = 'T'.join(_toks)
    fromSecs = getFromDateStr(s,format=format)
    return time.mktime(fromSecs.timetuple())

def dateTime(month=-1,day=-1,year=-1,format=formatSalesForceTimeStr()):
    """ dateTime from month,day,time """
    import time, datetime
    fromSecs = datetime.datetime.fromtimestamp(time.time())
    s = getAsDateTimeStr(fromSecs,fmt=format)
    _toks = s.split('T')
    toks = _toks[0].split('-')
    if (month > -1):
	toks[0] = '%02d' % (month)
    if (day > -1):
	toks[1] = '%02d' % (day)
    if (year > -1):
	toks[-1] = '%04d' % (year)
    _toks[0] = '-'.join(toks)
    s = 'T'.join(_toks)
    return getFromDateStr(s,format=format)

def daysInMonth(month=-1,year=-1,format=formatSalesForceTimeStr()):
    """ days in Month """
    import datetime, time
    dt = dateTime(month=month+1,day=1,year=year,format=formatDate_MMDDYYYY_dashes())
    _minus1 = datetime.timedelta(-1)
    dt += _minus1
    return dt.day

def timeSecondsFromTimeStamp(ts):
    """ get number of seconds """
    import time
    return time.mktime(ts.timetuple())

def timeStamp(tsecs=0,format=_formatTimeStr(),useLocalTime=isUsingLocalTimeConversions):
    """ get standard timestamp """
    useLocalTime = isUsingLocalTimeConversions if (not isinstance(useLocalTime,bool)) else useLocalTime
    secs = 0 if (not useLocalTime) else -utcDelta().seconds
    tsecs = tsecs if (tsecs > 0) else timeSeconds()
    t = tsecs+secs
    return getAsDateTimeStr(t if (tsecs > abs(secs)) else tsecs,fmt=format)

def getAsDateTimeStrFromTimeSeconds(secs,useLocalTime=isUsingLocalTimeConversions):
    return timeStamp(tsecs=secs,useLocalTime=useLocalTime)

def dateFromSeconds(ts,format=_formatTimeStr(),useLocalTime=isUsingLocalTimeConversions):
    useLocalTime = isUsingLocalTimeConversions if (not isinstance(useLocalTime,bool)) else useLocalTime
    ts = timeStamp(tsecs=ts,format=format,useLocalTime=useLocalTime)
    return getFromDateTimeStr(ts)

def timeStampForFileName(format=_formatTimeStr(),useLocalTime=isUsingLocalTimeConversions,delimiters=('_','')):
    ''' delimiters is a tuple that contains the replacement for 'T' and replacement for ':' in that order. '''
    import sys
    from vyperlogix import misc
    try:
        delimiters = delimiters if (isinstance(delimiters,tuple)) and (len(delimiters) == 2) else (delimiters,'')
        if (':' not in delimiters):
            useLocalTime = isUsingLocalTimeConversions if (not isinstance(useLocalTime,bool)) else useLocalTime
            return timeStamp(format=format,useLocalTime=useLocalTime).replace('T',delimiters[0]).replace(':',delimiters[-1])
        else:
            print >>sys.stderr, '%s :: Invalid use of delimiters parameter, cannot use ":" as a delimiter, double-check your work.' % (misc.funcName())
    except:
        print >>sys.stderr, '%s :: Invalid use of parameters, double-check your work.' % (misc.funcName())
    return None

def only_float_digits(aString):
    aString = str(aString)
    return ''.join([ch for ch in aString if (ch.isdigit()) or (ch in ['.','+','-'])])

def _float(aString):
    aString = only_float_digits(aString)
    return float(aString)

def only_digits(aString):
    aString = str(aString)
    return ''.join([ch for ch in aString if (ch.isdigit())])

def _int(aString):
    aString = only_digits(aString)
    return int(aString)

def isTimeStamp(ts):
    tests = [str(t).isdigit() or (t in ['_','-']) for t in ts]
    return (all(tests))

def isTimeStampForFileName(ts):
    return isTimeStamp(ts)

def isNativeTimeStamp(ts):
    tests = [str(t).isdigit() or (t in ['-','T',':']) for t in ts]
    return (all(tests))

def isNativeTimeStampForFileName(ts):
    return isNativeTimeStamp(ts)

def getFromNativeTimeStamp(ts,format=None):
    format = _formatTimeStr() if (format is None) else format
    if (':' not in ts):
        format = format.replace(':','')
    if ('T' not in ts):
        format = format.split('T')[0]
    return getFromDateTimeStr(ts,format=format)

def getFromTimeStampForFileName(ts):
    if (isTimeStampForFileName(ts)):
        toks = ts.split('_')
        t = toks[1:]
        if (len(t) == 1):
            tt = []
            for i in xrange(0,len(t[0]),2):
                tt.append(t[0][i:i+2])
            t = tt
        _ts = toks[0:1][0] + 'T' + ':'.join(t)
        return getFromDateTimeStr(_ts)
    elif (isNativeTimeStampForFileName(ts)):
        return getFromNativeTimeStamp(ts)
    else:
        return None

def isSometimeToday(ts):
    '''ts is a timeStamp in the form of a datetime object'''
    from vyperlogix import misc
    today = getFromNativeTimeStamp(timeStamp().split('T')[0])
    format = _formatTimeStr().split('T')[0]
    mm_dd_yyyy = getAsDateTimeStr(today,fmt=format)
    if (misc.isString(ts)):
        if (isNativeTimeStamp(ts)):
            other_day = getFromNativeTimeStamp(ts.split('T')[0])
        elif (isTimeStamp(ts)):
            other_day = getFromNativeTimeStamp(ts.split('_')[0])
        else:
            print >>sys.stderr, '(%s) :: Unknown format for "%s".' % (misc.funcName(),ts)
    else:
        other_day = ts
    other_mm_dd_yyyy = getAsDateTimeStr(other_day,fmt=format)
    return mm_dd_yyyy == other_mm_dd_yyyy

def timeStampLocalTime(tsecs=0,format=_formatTimeStr()):
    """ get standard timestamp adjusted to local time """
    return timeStamp(tsecs=tsecs,format=format,useLocalTime=isUsingLocalTimeConversions)

def timeStampLocalTimeForFileName(format=_formatTimeStr(),delimiters=('_','')):
    ''' delimiters is a tuple that contains the replacement for 'T' and replacement for ':' in that order. '''
    return timeStampForFileName(format=format,useLocalTime=isUsingLocalTimeConversions,delimiters=delimiters)

def timeStampSalesForce(offset_secs=None):
    """ get sales force timestamp using UTC """
    is_offset_secs_invalid = False
    if (offset_secs is not None):
        try:
            v = eval('%s' % (offset_secs))
        except ValueError:
            is_offset_secs_invalid = True
    return timeStamp(tsecs=timeSeconds() + (0 if (offset_secs is None) or (is_offset_secs_invalid) else offset_secs),format=formatSalesForceTimeStr(),useLocalTime=False)

def timeStampSimple(format=formatDate_MMDDYYYY_slashes(),useLocalTime=False):
    """ get simple timestamp using UTC """
    return timeStamp(tsecs=timeSeconds(),format=format,useLocalTime=useLocalTime)

def timeStampApache(useLocalTime=True):
    return timeStampSimple(format=formatApacheDateTimeStr(),useLocalTime=useLocalTime) + ' %04d' % ((utcDelta().seconds / 3600) * 100)

def timeStampMySQL(useLocalTime=True):
    return timeStampSimple(format=formatMySQLDateTimeStr(),useLocalTime=useLocalTime)

def callersContext():
    """ get context of caller of a function """
    import sys
    return sys._getframe(2).f_code

def logPrint(s):
    """ log a line to a file """
    import os, sys
    from vyperlogix import misc
    if (sys.platform == 'win32'):
        logPath = 'log'
    else:
        logPath = searchForFolderNamed('log',homeFolder())
    tstamp = timeStamp()
    folder = ''.join(tstamp.split('T')[0]).replace(':','-').replace('.','_')
    if (os.path.exists(logPath) == False):
        os.mkdir(logPath)
    logPath = os.sep.join([logPath,'details'])
    if (os.path.exists(logPath) == False):
        os.mkdir(logPath)
    logPath = os.sep.join([logPath,folder])
    if (os.path.exists(logPath) == False):
        os.mkdir(logPath)
    logFile = '%s.log' % (os.sep.join([logPath,sys.argv[0].split(os.sep)[-1]]).replace('.','_'))
    fOut = open(logFile,'a')
    fOut.write('%s::%s -- %s\n' % (tstamp,misc.callersName(),s))
    fOut.flush()
    fOut.close()
# END logPrint

def read_lines_simple(aFileName,mode):
    fIn = open(aFileName,mode)
    try:
        lines = [line.strip() for line in fIn.readlines() if (len(line.strip()) > 0)]
    finally:
        fIn.close()
    return lines

def _readFileFrom(fname,mode='r'):
    '''read-raw and return the lines via a list'''
    fIn = open(fname,mode)
    try:
        lines = fIn.readlines()
        return lines
    finally:
        fIn.close()
    return []

def readFileFrom(fname,mode='r',noCRs=False):
    '''mode='rb' then noCRs is not used otherwise the content is treated like text with line delimiters'''
    fIn = open(fname,mode)
    try:
        if (mode.find('b') == -1):
            lines = fIn.readlines()
            ch = '' if (noCRs) else '\n'
            if (noCRs):
                lines = [l.strip() for l in lines]
            data = ch.join(lines)
        else:
            data = fIn.read()
    finally:
        fIn.close()
    return data

def readBinaryFileFrom(fname):
    return readFileFrom(fname,mode='rb')

def writeFileFrom(fname,contents,mode='w'):
    dname = os.path.dirname(fname)
    safely_mkdir(fpath=dname,dirname='')
    fOut = open(fname,mode)
    try:
        fOut.write(contents)
    finally:
        fOut.flush()
        fOut.close()

def filesAsDict(top,deBias=False,asZip=False):
    import re
    svn_regex = re.compile('[._]svn')
    d = lists.HashedLists2()
    for root, dirs, files in walk(top, topdown=True, rejecting_re=svn_regex):
        for f in files:
            _fname = os.sep.join([root,f])
	    if (deBias):
		_fname = _fname.replace(top,'')
	    if (asZip):
		_fname = '/'.join([t for t in _fname.replace(os.sep,'/').split('/') if (len(t) > 0)])
	    d[_fname] = _fname
    return d

def analysisFromFilesDict(d):
    '''Performs a detailed analysis to determine the common parts of all the file paths.
    Useful in determining the bias of a heap of paths.
    The bias is that which appears in all the files equally.
    Knowing the bias can help us compare the contents of a zip file with the contents of a folder tree on a file-by-file basis.
    '''
    d_analysis = lists.HashedLists()
    for k,v in d.iteritems():
	toks = k.split(os.sep)
	bias = []
	for t in toks[0:-1]:
	    bias.append(t)
	    d_analysis[os.sep.join(bias)] = v
    to_be_retired = []
    for k,v in d_analysis.iteritems():
	if (not all([(kk.find(k) > -1) for kk in d_analysis.keys()])):
	    to_be_retired.append(k)
    return d_analysis

def crc32(top, isVerbose=False, isObfuscated=False):
    '''Walk the files and compute the crc from the bytes in the files...'''
    import binascii
    from vyperlogix.products import keys
    crc = 0
    for root, dirs, files in walk(top, topdown=True, rejecting_re=None):
        for f in files:
            _fname = os.sep.join([root,f])
	    _bytes = readBinaryFileFrom(_fname)
	    if (isVerbose):
		print '%s' % (_fname)
	    crc = binascii.crc32(_bytes,crc)
    return crc if (not isObfuscated) else keys._encode('%d' % (crc))

def stringIO(*args, **kwargs):
    try:
        from cStringIO import StringIO as StringIO
    except ImportError:
	try:
	    from StringIO import StringIO as StringIO
	except ImportError:
	    pass
    return StringIO(*args, **kwargs)

__symbol_InternetShortcut__ = '[InternetShortcut]'

def parse_InternetShortcut(fname):
    _url = ''
    if (fname.lower().endswith('.url')):
        if (os.path.exists(fname)):
            fIn = open(fname, 'rb')
            try:
                bytes = fIn.read()
            finally:
                fIn.close()
            l_bytes = bytes.split('\r\n')
            if (l_bytes[0] == __symbol_InternetShortcut__):
                toks = ''.join(l_bytes[1:]).split('=')
                toks = ''.join(toks[1:]).split('http://')
                _url = ','.join(['http://%s' % (t) for t in toks])
    return _url

def formattedException(details=''):
    from vyperlogix import misc
    return misc.formattedException(details=details,_callersName=misc.callersName())

def spawnProcessWithDetails(progPath,env=None,shell=False,fOut=None,pWait=True):
    """ spawn a background process with environment and shell options, when pWait is False the process object is returned """
    import os
    import subprocess
    import logging

    try:
        if (not fOut):
            _details_symbol = os.path.abspath('@details')
            if (not os.path.exists(_details_symbol)):
                os.mkdir(_details_symbol)
            _fOut = open('%s_%s.txt' % (os.sep.join([_details_symbol,'.'.join(timeStamp().replace(':','').split('.')[0:-1])]),os.path.basename(progPath).replace('.','_')),'w')
            logFname = _fOut.name
        elif (os.path.isdir(fOut)):
            _details_symbol = os.path.abspath(fOut)
            _fOut = open('%s_%s.txt' % (os.sep.join([_details_symbol,'.'.join(timeStamp().replace(':','').split('.')[0:-1])]),os.path.basename(progPath).replace('.','_')),'w')
            logFname = _fOut.name
        else:
            _fOut = fOut
    except:
        _fOut = fOut
    e = os.environ if env == None else env
    _isError = False
    _details = ''
    try:
        p = subprocess.Popen([progPath], env=e, stdout=_fOut, shell=shell)
        if (pWait):
            p.wait()
        else:
            return p
    except Exception, details:
        from vyperlogix import misc
        _isError = True
        _details = misc.formattedException(details=details)
        logging.warning('ERROR in "%s" caused "%s".' % (progPath,_details))
    if (_fOut != fOut):
        _fOut.flush()
        _fOut.close()
        if (not _isError):
            _details = readFileFrom(logFname)
        if (os.path.exists(logFname)):
            try:
                os.remove(logFname)
            except Exception, details:
                from vyperlogix import misc
                _details = misc.formattedException(details=details)
                logging.warning('WARNING :: Unable to remove the "%s" file in "%s" due to a Windows Error which is "%s".' % (logFname,_details_symbol,details))
        if (os.path.exists(_details_symbol)):
            try:
                os.rmdir(_details_symbol)
            except Exception, details:
                from vyperlogix import misc
                _details = misc.formattedException(details=details)
                logging.warning('WARNING :: Unable to remove the "%s" folder in "%s" due to a Windows Error which is "%s".' % (logFname,os.curdir,details))
    return _details

def expandInSubstr(t,args={}):
    """ expand all occurences of a macro bounded by %item% with a value from the dict passed via args """
    x = 0
    while (x > -1):
        x = t.find('%')
        if (x > -1):
            y = t[x+1:].find('%')
            if (y > -1):
                xx = t[x+1:x+y+1]
                if (args.has_key(xx)):
                    _t = args[xx]
                    t = t.replace('%'+xx+'%',_t)
                    x = y+1
    return t

def expandMacro(p,args={}):
    """ expand a macro bounded by %item% with a value from the dict passed via args """
    import os
    toks = p.split(',')
    _toks = []
    for t in toks:
        if (t.startswith('%') and t.endswith('%')):
            _t = t.replace('%','')
            if (args.has_key(_t)):
                t = args[_t]
        else:
            t = expandInSubstr(t,args)
        _toks.append(t)
    return _toks

def args(*args,**kwargs):
    kw = []
    for k,v in kwargs.iteritems():
	q = quote_it(v)
	kw.append('%s=%s%s%s' % (k,q,v,q))
    value = '%s%s%s' % (','.join(['%s%s%s' % (quote_it(arg),arg,quote_it(arg)) for arg in args]),',' if (len(args) > 0) and (len(kw) > 0) else '',','.join(kw))
    return value

def walk(top, topdown=True, onerror=None, rejecting_re=None):
    import os
    from vyperlogix.misc import ObjectTypeName

    isRejectingRe = ObjectTypeName.typeClassName(rejecting_re) == '_sre.SRE_Pattern'

    try:
        names = [n for n in os.listdir(top) if (not isRejectingRe) or (isRejectingRe and not rejecting_re.search(n))]
    except os.error, err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = os.path.join(top, name)
        if not os.path.islink(path):
            for x in walk(path, topdown, onerror, rejecting_re):
                yield x
    if not topdown:
        yield top, dirs, nondirs

def removeAllFilesUnder(top,rejecting_re=None,matching_re=None):
    """ remove all files under top including folders """
    import os
    from vyperlogix.misc import ObjectTypeName
    isMatchingRe = ObjectTypeName.typeClassName(matching_re) == '_sre.SRE_Pattern'
    for root, dirs, files in walk(top, topdown=False, rejecting_re=rejecting_re):
        for f in files:
            _fname = os.sep.join([root,f])
            if (not isMatchingRe):
                os.remove(_fname)
            elif (isMatchingRe) and (matching_re.search(_fname)):
                os.remove(_fname)
        if (not isMatchingRe) and (os.path.exists(root)) and (os.listdir(root) == []):
            try:
                os.rmdir(root)
            except WindowsError, details:
                print 'ERROR due to %s' % details
                pass

def validatePathEXE(eVar=['PATH','PYTHONPATH'],fname='python.exe',verbose=False):
    """
    finds the specified fname from PATH.
    eVar can be a string or a list of strings that specify a path or list of paths.
    """
    import os
    from vyperlogix import misc
    eVar = eVar if (misc.isList(eVar)) else [eVar]
    for e in eVar:
	if (misc.isString(e)) and (os.environ.has_key(e)):
	    toks = os.environ[e].split(';')
	    for t in toks:
		f = searchForFileNamed(fname,t)
		if (verbose):
		    print '(%s)=[%s in %s]' % (f,fname,t)
		if (len(f) > 0):
		    return os.sep.join([t,fname])
    return ''

def validatePathEXE_using_environ(fname='python.exe'):
    import os, sys
    _paths = sys.path
    fname = str(fname).lower()
    if (os.environ.has_key('PYTHONPATH')):
        _paths = os.environ['PYTHONPATH'].split(';')
        _top = '%s%s' % (':' if (sys.platform == 'win32') else '',os.sep)
        ex_paths = []
        for n in _paths:
            while (len(n) > 0) and (n[len(n)-2:] != _top):
                n = os.path.dirname(n)
                if (len(n) > 0) and (n[len(n)-2:] != _top):
                    ex_paths.append(n)
                else:
                    break
        _paths += ex_paths
    elif (os.environ.has_key('PATH')):
        _paths = os.environ['PATH'].split(';')
    _path = [n for n in _paths if (os.path.isdir(n)) and (os.path.exists(os.sep.join([n,fname])))]
    return '' if (len(_path) == 0) else _path[0]

def _makeDirs(_dirName):
    """ make all folders for a path, front to back, without considering the _dirName to be a fully qualified file path. """
    import os
    if (not os.path.exists(_dirName)):
        try:
            os.makedirs(_dirName)
        except:
            pass

def makeDirs(fname):
    """ make all folders for a path, front to back, fname is considered to be a fully qualified file path name rather than the name of a folder. """
    import os
    _dirName = fname if (os.path.isdir(fname)) else os.path.dirname(fname)
    _makeDirs(_dirName)

def explain_stat(st,delim=','):
    s = []
    try:
        s.append('ST_ATIME is %s' % (st[stat.ST_ATIME]))
    except:
        pass
    try:
        s.append('ST_CTIME is %s' % (st[stat.ST_CTIME]))
    except:
        pass
    try:
        s.append('ST_DEV is %s' % (st[stat.ST_DEV]))
    except:
        pass
    try:
        s.append('ST_GID is %s' % (st[stat.ST_GID]))
    except:
        pass
    try:
        s.append('ST_INO is %s' % (st[stat.ST_INO]))
    except:
        pass
    try:
        st_mode = st[stat.ST_MODE]
        _mode = stat.S_IMODE(st_mode)
        r_mode = 0
        a = []
        for k,v in _all_modes.iteritems():
            if (_mode & k):
                a += v
                r_mode |= k
        s.append('ST_MODE is %o or "%s"' % (r_mode,','.join(a)))
    except Exception, details:
        print '%s' % (str(details))
        pass
    try:
        s.append('ST_MTIME is %s' % (st[stat.ST_MTIME]))
    except:
        pass
    try:
        s.append('ST_NLINK is %s' % (st[stat.ST_NLINK]))
    except:
        pass
    try:
        s.append('ST_SIZE is %s' % (st[stat.ST_SIZE]))
    except:
        pass
    try:
        s.append('ST_UID is %s' % (st[stat.ST_UID]))
    except:
        pass
    return delim.join(s)

# Chmod recursively on a whole subtree
def chmod_tree(path, mode, mask):
    '''Chmod the tree at path'''
    import os, sys, stat
    def visit(arg, dirname, names):
        mode, mask = arg
        for name in names:
            fullname = os.path.join(dirname, name)
            if not os.path.islink(fullname):
                new_mode = (os.stat(fullname)[stat.ST_MODE] & ~mask) | mode
                m = '%o' % (new_mode)
                os.chmod(fullname, eval(m[len(m)-4:]))
    if (os.path.isfile(path)):
        path = os.path.dirname(path)
    os.path.walk(path, visit, (mode, mask))

# For clearing away read-only directories
def safe_rmtree(dirname, retry=0):
    '''Remove the tree at DIRNAME'''
    import os, sys, stat, shutil, time
    def rmtree(dirname):
        chmod_tree(dirname, 0666, 0666)
        shutil.rmtree(dirname)

    if (os.path.isfile(dirname)):
        dirname = os.path.dirname(dirname)

    if (sys.platform == 'win32'):
        m = stat.S_IREAD | stat.S_IWRITE
        chmod_tree(dirname, m, m)
        return removeAllFilesUnder(dirname)

    if not os.path.exists(dirname):
        return

    if retry:
        for delay in (0.5, 1, 2, 4):
            try:
                rmtree(dirname)
                break
            except:
                time.sleep(delay)
        else:
            rmtree(dirname)
    else:
        rmtree(dirname)

def locateRootContaining(top,fname):
    '''Locate a specific file using a recursive function that melts a path to nothing unless the file is found in the list of files at that level.'''
    import os
    while (1):
        d = dict([(k,os.sep.join([top,k])) for k in os.listdir(top)])
        if (d.has_key(fname)):
            return os.sep.join([top,fname])
        top = os.path.dirname(top)
        if (not os.path.exists(top)):
            break
    return None

def copyFile(src,dst,func=None):
    """ copies a binary file from src to dst """
    import os
    import types
    if (os.path.exists(src)):
        makeDirs(dst)
        fIn = open(src,'rb')
        fOut = open(dst,'wb')
        _failed = True
        try:
            if (callable(func)):
                try:
                    data = '\n'.join(fIn.readlines())
                    fOut.write(func(data))
                    _failed = False
                except:
                    _failed = True
            if (_failed):
                [fOut.write(ch) for l in fIn for ch in l]
        finally:
            fOut.flush()
            fOut.close()
            fIn.close()
    else:
        print 'ERROR :: Cannot find the file named "%s".' % src

def fileSize(fname):
    if (os.path.exists(fname)):
        st = os.stat(fname)
        return st.st_size
    return -1

def tempFile(prefix,useTemporaryFile=False):
    '''Get the name of a temp file based on where such files are being kept. See also appDataFolder() for a similar use.'''
    import os
    import tempfile as tfile
    from vyperlogix import misc
    common = ''
    prefix = str(prefix) if not misc.isString(prefix) else prefix
    if (os.environ.has_key('TEMP')):
        common = os.environ['TEMP']
    elif (os.environ.has_key('TMP')):
        common = os.environ['TMP']
    if (len(common) == 0) or (useTemporaryFile):
        f = tfile.TemporaryFile()
        common = os.path.abspath(os.sep.join(f.name.split(os.sep)[0:-1]))
        f.close()
    return os.sep.join([common,prefix])

def appDataFolder(prefix='',useTemporaryFile=True):
    '''Get the name of a temp file based on where application specific files are being kept.'''
    from vyperlogix import misc
    if (sys.platform == 'win32'):
        t = tempFile('',useTemporaryFile=useTemporaryFile)
        toks = [_t_ for _t_ in t.lower().split(os.sep) if (len(_t_.strip()) > 0)]
        if (len(toks) > 0):
            _popped_too_many = False
            _toks = misc.copy(toks)
            while (toks[-1].replace('location ','') != 'appdata'):
                toks.pop()
                if (len(toks) == 0):
                    _popped_too_many = True
                    break
            if (_popped_too_many):
                toks = misc.copy(_toks)
        if (misc.findFirstContaining(toks,'local') == -1):
            toks.append('local')
        if (len(prefix) > 0):
            toks.append(prefix)
        return os.sep.join(toks)
    return tempFile(prefix=prefix,useTemporaryFile=useTemporaryFile)

def _findUsingPath(t,p):
    from vyperlogix import misc
    ptoks = p.split(';')
    if (len(ptoks) == 1):
        ptoks = p.split(':')
    for f in ptoks:
        for root, dirs, files in os.walk(f, topdown=True):
            for f in files:
                if (f.split(os.sep)[-1] == t) or (f.find(t) > -1):
                    return os.sep.join([root,f])
    return None

def findUsingPath(fname):
    '''Allows findUsingPath(r"@SVN_BINDIR@/svnlook") to be used as a way to execute a macro.'''
    from vyperlogix import misc
    toks = fname.split('/')
    t = toks[0]
    if (t.startswith('@')) and (t.endswith('@')) and (len(toks) > 1):
        tx = t.replace('@','')
        t = toks[1]
    else:
        tx = toks[1]
    t += '.' if (sys.platform == 'win32') else ''
    p = os.environ["PATH"] if (not os.environ.has_key(tx)) else os.environ[tx]
    #print '%s :: tx=%s, t=%s, p=%s' % (misc.funcName(),tx,t,p)
    tf = _findUsingPath(t,p)
    #print '%s :: tf=%s' % (misc.funcName(),tf)
    if (tf == None):
        try:
            p = os.environ["windir"]
            p = p.split(os.sep)[0]+os.sep
        except:
            p = '%s' % (os.sep)
        tf = _findUsingPath(t,p)
    return tf

def print_stderrout(msg):
    import sys
    print >>sys.stdout, msg
    print >>sys.stderr, msg

def strip(s):
    return ''.join([ch for ch in s if (ord(ch) != 0)]).strip()

def expand_template(string,context):
    s = string
    for k,v in context.iteritems():
        _k = '{{ %s }}' % (k)
        s = s.replace(_k,str(v))
    return s

def parseBetween(s,i,tok1,tok2):
    foundIt1 = -1
    for x in xrange(i,0,-1):
        if (s[x] == '?'):
            foundIt1 = x
            break
    foundIt2 = -1
    for x in xrange(i,len(s)):
        if (s[x] == '"'):
            foundIt2 = x
            break
    return foundIt1,foundIt2

class DeCamelCaseMethods(Enum):
    default = 2**0
    force_lower_case = 2**1

def de_camel_case(stringAsCamelCase,delim=' ',method=DeCamelCaseMethods.default):
    """Adds spaces to a camel case string.  Failure to space out string returns the original string.
    >>> space_out_camel_case('DMLSServicesOtherBSTextLLC')
    'DMLS Services Other BS Text LLC'
    """
    import re
    from vyperlogix import misc
    
    def get_matches(subject):
	matches = [match for match in pattern.finditer(subject)]
	if (subject[0].isupper()) and (len(matches) > 0) and (matches[0].start() == 0):
	    del matches[0]
	return matches
    
    if stringAsCamelCase is None:
        return None
    _stringAsCamelCase = stringAsCamelCase

    normalize = lambda s:s
    if (method == DeCamelCaseMethods.force_lower_case):
	normalize = lambda s:s.lower()
	
    is_lowerUpper = lambda group:group[0].islower() and group[-1].isupper()
    isUpper_lower = lambda group:group[0].isupper() and group[-1].islower()
    isUpperUpper = lambda group:group[0].isupper() and group[-1].isupper()
    is_lowerUpperUpper = lambda group:group[0].islower() and group[1].isupper() and group[1].isupper()
    
    pattern = re.compile('([a-z][A-Z][A-Z][_])|([A-Z][A-Z])|([a-z][A-Z])|([A-Z][a-z])')
    while (1):
	matches = get_matches(_stringAsCamelCase)
	if (len(matches) == 0):
	    break
	aMatch = matches.pop()
	if (is_lowerUpper(aMatch.group())):
	    b = (aMatch.group()[0:1] != '_')
	    _stringAsCamelCase = _stringAsCamelCase[0:aMatch.start()] + aMatch.group()[0:1] + (delim if (b) else '') + aMatch.group()[1:].lower() + _stringAsCamelCase[aMatch.end():]
	elif (isUpper_lower(aMatch.group())):
	    b = (_stringAsCamelCase[0:aMatch.start()][-1] != '_')
	    _stringAsCamelCase = _stringAsCamelCase[0:aMatch.start()] + (delim if (b) else '') + aMatch.group().lower() + _stringAsCamelCase[aMatch.end():]
	elif (isUpperUpper(aMatch.group())):
	    b = (aMatch.group()[0:1] != '_')
	    _stringAsCamelCase = _stringAsCamelCase[0:aMatch.start()] + (delim if (b) else '') + aMatch.group()[0:1].lower() + aMatch.group()[1:].lower() + _stringAsCamelCase[aMatch.end():]
	elif (is_lowerUpperUpper(aMatch.group())):
	    _stringAsCamelCase = _stringAsCamelCase[0:aMatch.start()] + aMatch.group()[0:1] + delim + aMatch.group()[1:].lower() + _stringAsCamelCase[aMatch.end():]
    return normalize(_stringAsCamelCase)
	
if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
    
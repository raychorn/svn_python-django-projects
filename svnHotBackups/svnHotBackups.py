#
#  hot-backup.py: perform a "hot" backup of a Subversion repository
#                 and clean any old Berkeley DB logfiles after the
#                 backup completes, if the repository backend is
#                 Berkeley DB.
#
#  Subversion is a tool for revision control. 
#  See http://subversion.tigris.org for more information.
#    
# ====================================================================
# Copyright (c) 2000-2007 CollabNet.  All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
#
# This software consists of voluntary contributions made by many
# individuals.  For exact contribution history, see the revision
# history and logs, available at http://subversion.tigris.org/.
# ====================================================================

# ====================================================================
# Defects:
# (1). Not tossing out old backups to reduce disk space.
# (2). Not moving backups into the carbonite folder.
# (3). Not tossing-out old carbonite backups to reduce space.
# ====================================================================
# AWS Commands
# aws ls __vyperlogix_svn_backups__/backups
# aws delete __vyperlogix_svn_backups__/backups/repo1-14761.tar.gz
#
# $HeadURL$
# $LastChangedDate$
# $LastChangedBy$
# $LastChangedRevision$

######################################################################

import sys, os, getopt, stat, string, re, time, shutil
import traceback
from vyperlogix import _utils

__version__ = _utils.get_version_decimal(precision=1)
if (__version__ < 2.5) or (__version__ >= 3.0):
    print 'ERROR: Please use Python 2.x but not version %s.' % (__version__)
    sys.exit(1)

print 'BEGIN:'
for f in sys.path:
    print f
print 'END!'

import locale

locale.setlocale(locale.LC_ALL, "")

format_with_commas = lambda value:locale.format('%d', int(value), True)

from vyperlogix.enum.Enum import Enum

from vyperlogix import misc
from vyperlogix.process import Popen
from vyperlogix.misc import _utils
from vyperlogix.hash.lists import HashedFuzzyLists, HashedFuzzyLists2

from vyperlogix.lists.ListWrapper import ListWrapper

__is_platform_not_linux = sys.platform.count('linux') == 0
if (__is_platform_not_linux):
    from vyperlogix import oodb
from vyperlogix.hash import lists
from vyperlogix.classes import SmartObject

from vyperlogix.crypto import XTEAEncryption

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix import boto
from boto.s3 import connection

from vyperlogix.misc import ioTimeAnalysis

__pid__ = None

_iv = XTEAEncryption.iv(_utils.getProgramName())

s_passPhrase = [110,111,119,105,115,116,104,101,116,105,109,101,102,111,114,97,108,108,103,111,111,100,109,101,110,116,111,99,111,109,101,116,111,116,104,101,97,105,100,111,102,116,104,101,105,114,99,111,117,110,116,114,121]
_passPhrase = ''.join([chr(ch) for ch in s_passPhrase])

__url__ = 'www.vyperlogix.com'

__bucket_name__ = '__vyperlogix_svn_backups__'

# Try to import the subprocess mode.  It works better then os.popen3
# and os.spawnl on Windows when spaces appear in any of the svnadmin,
# svnlook or repository paths.  os.popen3 and os.spawnl are still used
# to support Python 2.3 and older which do not provide the subprocess
# module.  have_subprocess is set to 1 or 0 to support older Python
# versions that do not have True and False.
try:
    import subprocess
    have_subprocess = 1
except ImportError:
    have_subprocess = 0

######################################################################
# Global Settings

# Archive types/extensions
#archive_map = {
    #'none': '',
    #'gz'  : ".tar.gz",
    #'bz2' : ".tar.bz2",
    #'zip' : ".zip",
    #'ezip' : ".ezip", # XTEAEncryption using Hex
    ##'xzip' : ".xzip", # XTEAEncryption using No-Hex ??? there seems to be a bug here...
    #'bzip' : ".bzip", # blowfish
#}

class ArchiveTypes(Enum):
    none = ''
    gz = '.tar.gz'
    bz2 = '.tar.bz2'
    zip = '.zip'
    ezip = '.ezip' # XTEAEncryption using Hex
    bzip = '.bzip' # blowfish
    xzip = '.xzip'

class BackupTypes(Enum):
    A = 0
    Alt = 0
    Alternate = 0
    Primary = 1
    Pri = 1
    P = 1
is_type_alternate = lambda value:(value in [BackupTypes.A,BackupTypes.Alt,BackupTypes.Alternate])

def other_backup_type(t):
    if (is_type_alternate(t)):
	return BackupTypes.Primary
    return BackupTypes.Alternate

######################################################################
# Helper functions

def date_comparator(a, b):
    a_statinfo = os.stat(a)
    b_statinfo = os.stat(b)
    return -1 if (a_statinfo.st_mtime < b_statinfo.st_mtime) else 0 if (a_statinfo.st_mtime == b_statinfo.st_mtime) else 1

def s3_date_comparator(a, b):
    '''a and b are both key objects that have metadata'''
    try:
	val = -1 if (a.metadata['ST_MTIME'].split('=')[0] < b.metadata['ST_MTIME'].split('=')[0]) else 0 if (a.metadata['ST_MTIME'].split('=')[0] == b.metadata['ST_MTIME'].split('=')[0]) else 1
    except Exception, ex:
	info_string = _utils.formattedException(details=ex)
	print >>sys.stderr, info_string
	val = 0 # just call them equal in case of a problem...
    return val

def comparator(a, b):
    # We pass in filenames so there is never a case where they are equal.
    regexp = re.compile("-(?P<revision>[0-9]+)(-(?P<increment>[0-9]+))?" + ext_re + ("$" if (len(ext_re) > 0) else ''))
    matcha = regexp.search(a)
    matchb = regexp.search(b)
    reva = int(matcha.groupdict()['revision'])
    revb = int(matchb.groupdict()['revision'])
    if (reva < revb):
        return -1
    elif (reva > revb):
        return 1
    else:
        inca = matcha.groupdict()['increment']
        incb = matchb.groupdict()['increment']
        if not inca:
            return -1
        elif not incb:
            return 1;
        elif (int(inca) < int(incb)):
            return -1
        else:
            return 1

def get_youngest_revision():
    """Examine the repository REPO_DIR using the svnlook binary
  specified by SVNLOOK, and return the youngest revision."""

    if have_subprocess:
        p = subprocess.Popen([svnlook, 'youngest', repo_dir],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        infile, outfile, errfile = p.stdin, p.stdout, p.stderr
    else:
        infile, outfile, errfile = os.popen3(svnlook + " youngest " + repo_dir)

    stdout_lines = outfile.readlines()
    stderr_lines = errfile.readlines()
    outfile.close()
    infile.close()
    errfile.close()

    if stderr_lines:
        raise Exception("Unable to find the youngest revision for repository '%s'"
                        ": %s" % (repo_dir, string.rstrip(stderr_lines[0])))

    return string.strip(stdout_lines[0])

######################################################################
# Main

from vyperlogix.decorators import onexit

@onexit.onexit
def on_exit():
    try:
	try:
	    if (__pid__ is not None):
		from vyperlogix.process import killProcByPID
		killProcByPID(p.pid)
	except KeyboardInterrupt, SystemExit:
	    pass
	finally:
	    __pid__ = None
    except:
	pass

def walk_and_collect_files_from(_target_path_,topdown=True,onerror=None,rejecting_re=None):
    _files_ = {}
    try:
	for folder,dirs,files in _utils.walk(_target_path_, topdown=topdown, onerror=onerror, rejecting_re=rejecting_re):
	    for f in files:
		_files_[f] = os.sep.join([folder,f])
    except:
	pass
    return _files_
	    
if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--skip':'skip the actual backup process.',
	    '--specific':'consider only those backups that match the currently selected method otherwise consider them all.',
	    '--restore=?':'must be a valid archive file that can be restored (bzip).',
	    '--archive-type=?':'must be one of %s.' % (','.join(['"%s"' % (i.value) for i in ArchiveTypes._items_])),
	    '--num-backups=?':'the number of backups to keep.',
	    '--repo-path=?':'path to the SVN repo.',
	    '--backup-dir=?':'path to the folder where backups are to be placed, this folder can reside on a resource accessible by SSH+SFTP.',
	    '--s3=?':'path to the AWS_CREDENTIAL_FILE (ala. boto) or "default" or "improved".',
	    '--carbonite=?':'path to the carbonite folder.',
	    '--carbonite-alt=?':'alternate path to the carbonite folder.',
	    '--carbonite-hours=?':'the number of hours between carbonite backups.',
	    '--carbonite-files=?':'the number of files to maintain in carbonite backups.',
	    '--carbonite-optimize=?':'(1/True) once the file is copied into the carbonite folder the source is removed to free-up disk-space.',
	    '--carbonite-schedule=?':'schedule for issuing carbonite backups ?type=Primary&days=M-F&hours=0-20&type=Alt&days=Sa-Su&hours=*.',
	    '--username=?':'username for SSH if using a folder path from a foreign resource otherwise leave this blank.',
	    '--password=?':'password for SSH if using a folder path from a foreign resource otherwise leave this blank.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
	
	_isVerbose = __args__.get_var('isVerbose',bool,False)
	_isDebug = __args__.get_var('isDebug',bool,False)
	_isSkip = __args__.get_var('isSkip',bool,False)
	_isSpecific = __args__.get_var('isSpecific',bool,False)
	_isHelp = __args__.get_var('isHelp',bool,False)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	__archive_type_default = 'none'
	__archive_type = ArchiveTypes(__args__.get_var('archive-type',misc.isString,__archive_type_default))
	    
	try:
	    if (__archive_type is None):
		__archive_type = __archive_type_default
		print 'Invalid --archive-type of "%s"; must be one of "%s" instead.' % (__archive_type,l)
	except:
	    __archive_type = __archive_type_default
	_archive_type = __archive_type
	
	print '_archive_type=%s' % (_archive_type)

	num_backups = __args__.get_var('num-backups',int,int(os.environ.get("SVN_HOTBACKUP_BACKUPS_NUMBER", 64)))
	
	_repo_path = __args__.get_var('repo-path',misc.isString,'')
	_restore_path = __args__.get_var('restore',misc.isString,'')
	_backup_dir = __args__.get_var('backup-dir',misc.isString,'')
	_s3 = __args__.get_var('s3',misc.isValidFile,'')
	if (len(_s3) > 0):
	    _s3 = os.path.abspath(_s3)
	else:
	    _s3 = __args__.get_var('s3',misc.isString,'')
	_carbonite = __args__.get_var('carbonite',misc.isString,'')
	_carbonite_alt = __args__.get_var('carbonite-alt',misc.isString,'')

	_is_carbonite = os.path.exists(_carbonite)
	_is_s3 = os.path.exists(_s3)
	
	anS3Connection = None
	print '(DEBUG).1 _is_s3=%s, _s3=%s' % (_is_s3,_s3)
	if (_is_s3):
	    # BEGIN: This only works for Windows - see the /etc/boto.cfg for Linux and others.
	    if (_utils.isUsingWindows):
		os.environ['AWS_CREDENTIAL_FILE'] = _s3
	    anS3Connection = connection.S3Connection()
	    print '(DEBUG).2 _s3=%s, anS3Connection=%s' % (_s3,anS3Connection)
	    # END!   This only works for Windows - see the /etc/boto.cfg for Linux and others.
	elif (_s3 in ['default']):
	    soCredentials = boto.get_aws_credentials(url=boto._url_(),filename=None,method=boto.Methods.default)
	    print '(DEBUG).3 Method.default !!'
	elif (_s3 in ['improved']):
	    soCredentials = boto.get_aws_credentials(url=boto._url2_(),filename=None,method=boto.Methods.improved)
	    print '(DEBUG).4 Method.improved !!'
	if (anS3Connection is None):
	    try:
		anS3Connection = connection.S3Connection(aws_access_key_id=soCredentials.AWSAccessKeyId, aws_secret_access_key=soCredentials.AWSSecretKey)
		_is_s3 = True
		print '(DEBUG).5 Method Default !!'
	    except:
		pass
	print '(DEBUG).6 anS3Connection=%s' % (anS3Connection)

	_carbonite_hours = __args__.get_var('carbonite-hours',int,int(os.environ.get("CARBONITE_HOURS", 12)))
	_carbonite_files = __args__.get_var('carbonite-files',int,int(os.environ.get("CARBONITE_FILES", 60)))

	_carbonite_optimize = __args__.get_var('carbonite-optimize',lambda value:(value == '1') or (value== 'True'),False,is_filter=True)
	
	__carbonite_schedule = __args__.get_var('carbonite-schedule',misc.isDict,HashedFuzzyLists({ }))

	ioTimeAnalysis.initIOTime(__name__)
	ioTimeAnalysis.ioBeginTime(__name__)
	
	try: # ?type1=Primary&days1=M-F&hours1=0-20&type2=Alt&days2=Sa-Su&hours2=*
	    from vyperlogix import sets
	    def choose_schedule_days_options(_dict_):
		try:
		    specs = dict([(k,_utils.days_range(misc._unpack_(v)['days'])) for k,v in _dict_.iteritems() if (misc._unpack_(v)['days'])])
		except:
		    specs = dict()
		__specs__ = {}
		_specs_ = specs.values()
		for k,v in specs.iteritems():
		    specs[k] = [v,list(sets.diff(_specs_,v))]
		if (len(specs) == 2):
		    _keys = misc.sortCopy(specs.keys())
		    _a_ = dict({_keys[0]:_keys[-1],_keys[-1]:_keys[0]})
		    for k,v in specs.iteritems():
			for n in v[-1]:
			    __specs__['%d'%(n)] = _a_[k]
		return HashedFuzzyLists2(__specs__)
	    def proper_backup_type(d):
		_type_ = d['type'] if (d.has_key('type')) else None
		_l_ = ListWrapper([i.name for i in BackupTypes._items_])
		try:
		    _i_ = _l_.findFirstContaining(_type_.name)
		except:
		    _i_ = _l_.findFirstContaining(_type_)
		return BackupTypes._items_[_i_] if (_i_ > -1) else None
	    def map_schedule_days(days,_sched_):
		for k,v in days.iteritems():
		    d = misc._unpack_(_sched_[v]).asDict()
		    dR = _utils.days_range(d['days']) if (d.has_key('days')) else []
		    hR = ListWrapper(_utils.hours_range(d['hours']) if (d.has_key('hours')) else [])
		    t = proper_backup_type(d)
		    del days[k]
		    days[k] = {'days':dR,'hours':hR,'type':t}
		_d_ = HashedFuzzyLists()
		for k,v in days.iteritems():
		    d = v
		    dR = d['days'] if (d.has_key('days')) else []
		    hR = ListWrapper(d['hours'] if (d.has_key('hours')) else [])
		    t = proper_backup_type(d)
		    for dd in dR:
			for hh in xrange(0,24):
			    _f_ = hR.findFirstMatching(hh)
			    kk = '%d.%d'%(dd,hh)
			    if (_d_.has_key(kk)):
				del _d_[kk]
			    if (_f_ > -1):
				_d_[kk] = t
			    else:
				_d_[kk] = other_backup_type(t)
			pass
		    pass
		return _d_
	    _d_ = choose_schedule_days_options(__carbonite_schedule)
	    _map_ = map_schedule_days(_d_,HashedFuzzyLists(__carbonite_schedule.asDict()))
	    _day_ = _utils.day_of_week()
	    _s_ = _d_['%d'%(_day_.value)]
	    if (misc.isDict(_s_)):
		_s_['_day_'] = _day_
		__carbonite_schedule = _s_
	except Exception, ex:
	    info_string = _utils.formattedException(details=ex)
	    print >>sys.stderr, info_string
	    __carbonite_schedule = None
	_carbonite_schedule = __carbonite_schedule
	
	_username = __args__.get_var('username',misc.isString,'')
	_password = __args__.get_var('password',misc.isString,'')
	
	svnlook = ''
	
	_program_name = _utils.getProgramName()
	_data_path = _utils.appDataFolder(os.sep.join([__url__,_program_name]))
	_utils._makeDirs(_data_path)
	if (__is_platform_not_linux):
	    _dbx_name = oodb.dbx_name('%s_settings.dbx' % (_program_name),_data_path)
	    print '(DEBUG) _dbx_name=%s' % (_dbx_name)
	
	if (not _isSkip):
	    if (__is_platform_not_linux):
		dbx = oodb.PickledFastCompressedHash2(_dbx_name,has_bsddb=oodb.__has_bsddb)
		try:
		    if (dbx.has_key('svnlook')):
			_svnlook = dbx['svnlook']
			svnlook = '' if (not os.path.exists(_svnlook)) else _svnlook
		finally:
		    dbx.close()
		
	    if (not os.path.exists(svnlook)):
		print 'Searching for svnlook.'
		svnlook = _utils.findUsingPath(r"@SVN_BINDIR@/svnlook")
	    
	    if (svnlook is not None) and (os.path.exists(svnlook)):
		print 'Found svnlook at "%s".' % (svnlook)
		root = os.path.dirname(svnlook)
		svnadmin_fname = os.sep.join([root,'svnadmin.exe'])
		if (os.path.exists(svnadmin_fname)):
		    svnadmin = svnadmin_fname
		else:
		    print 'Searching for svnadmin.'
		    svnadmin = _utils.findUsingPath(r"@SVN_BINDIR@/svnadmin") # Path to svnadmin utility
		    if (svnlook is not None) and (os.path.exists(svnlook)):
			print 'Found svnadmin at "%s".' % (svnadmin)
		    else:
			print 'Could not find svnadmin at "%s", cannot proceed. Install SVN Admin functions and try again.' % (svnadmin)
			sys.exit()
	    else:
		print 'Could not find svnlook at "%s", cannot proceed. Install SVN Admin functions and try again.' % (svnlook)
		sys.exit()
    
	    if (__is_platform_not_linux):
		dbx = oodb.PickledFastCompressedHash2(_dbx_name,has_bsddb=oodb.__has_bsddb)
		try:
		    if (dbx.has_key('svnlook')):
			del dbx['svnlook']
		    dbx['svnlook'] = svnlook
		finally:
		    dbx.close()
		
	if (os.path.exists(_restore_path)):
	    print 'Your --restore of "%s" exists.' % (_restore_path)
	    from vyperlogix.zip import secure
	    fext = os.path.splitext(_restore_path)
	    if (fext[-1] == '.bzip'):
		_utils.makeDirs(_repo_path)
		print 'BEGIN --restore of "%s" into "%s".' % (_restore_path,_repo_path)
		secure.unzipper(_restore_path,_repo_path,archive_type=secure.ZipType.bzip,passPhrase=_passPhrase)
		print 'END --restore of "%s" into "%s".' % (_restore_path,_repo_path)
	    else:
		print 'ERROR: Cannot restore the file named "%s" because it has an unrestorable file extension of "%s".' % (_restore_path,fext[-1])
	    sys.exit()
	    
	archive_type = _archive_type
	
	# Path to repository
	if (not os.path.exists(_repo_path)):
	    print 'Your --repo-path of "%s" does not exist.' % (_repo_path)
	    sys.exit()
	repo_dir = _repo_path
	repo = os.path.basename(os.path.abspath(repo_dir))
	
	# Added to the filename regexp, set when using --archive-type.
	ext_re = ""
	
	# Do we want to create an archive of the backup
	if archive_type:
	    # Additionally find files with the archive extension.
	    ext_re = "(" + re.escape(archive_type.value) + ")?"
	else:
	    print "Unknown archive type '%s'.\n\n" % archive_type
	    ppArgs()
	    sys.exit(2)
	
	_isUsingSFTP = False
	backup_dir = _backup_dir
	if (not _isSkip):
	    print "Beginning hot backup of '"+ repo_dir + "'."
	    
	    ### Step 1: get the youngest revision.
	    
	    try:
		youngest = get_youngest_revision()
	    except Exception, e:
		print str(e)
		sys.exit(1)
	    
	    print "Youngest revision is", youngest
	    
	    ### Step 2: Find next available backup path
	    
	    youngest_repo = repo + "-" + youngest
	    
	    # Where to store the repository backup.  The backup will be placed in
	    # a *subdirectory* of this location, named after the youngest
	    # revision.
	    print "DEBUG.1: _backup_dir is '%s' and it %s." % (_backup_dir,'exists' if (os.path.exists(_backup_dir)) else 'does NOT exist')
	    if (os.path.exists(_backup_dir)):
		backup_dir = _backup_dir
	    else:
		_utils._makeDirs(_backup_dir)
		print "DEBUG.2: _backup_dir is '%s' and it %s." % (_backup_dir,'exists' if (os.path.exists(_backup_dir)) else 'does NOT exist')
		if (os.path.exists(_backup_dir)):
		    backup_dir = _backup_dir
		else:
		    backup_dir = os.sep.join([_data_path,youngest_repo])
		    _utils._makeDirs(backup_dir)
	    _isUsingSFTP = (backup_dir != _backup_dir) and (_username) and (len(_username) > 0) and (_password) and (len(_password) > 0)
	    print "DEBUG.3: _isUsingSFTP is '%s'." % (_isUsingSFTP)
	    
	    backup_subdir = os.path.join(backup_dir, youngest_repo)
	    
	    # If there is already a backup of this revision, then append the
	    # next highest increment to the path. We still need to do a backup
	    # because the repository might have changed despite no new revision
	    # having been created. We find the highest increment and add one
	    # rather than start from 1 and increment because the starting
	    # increments may have already been removed due to num_backups.
	    
	    regexp = re.compile("^" + repo + "-" + youngest + "(-(?P<increment>[0-9]+))?" + ext_re + "$")
	    directory_list = [f for f in os.listdir(backup_dir) if (not f.endswith('.zip'))]
	    young_list = filter(lambda x: regexp.search(x), directory_list)
	    if young_list:
		young_list.sort(comparator)
		increment = regexp.search(young_list.pop()).groupdict()['increment']
		if increment:
		    backup_subdir = os.path.join(backup_dir, repo + "-" + youngest + "-" + str(int(increment) + 1))
		else:
		    backup_subdir = os.path.join(backup_dir, repo + "-" + youngest + "-1")
		for item in young_list:
		    f = os.path.join(backup_dir, item)
		    if (os.path.exists(f)):
			try:
			    os.remove(f)
			except:
			    pass
	    
	    #_backup_subdir = backup_subdir
	    #backup_subdir +=  '_' + _utils.timeStamp().replace(':','.').replace('.000Z','')
	    
	    ### Step 3: Ask subversion to make a hot copy of a repository.
	    ###         copied last.
	    
	    # +++
	    def perform_disk_space_check_and_cleanup(target_path):
		from vyperlogix.win import diskSpace

		_result = True
		_target_path_ = os.path.dirname(os.path.dirname(target_path))
		print 'DEBUG: BEGIN: perform_disk_space_check_and_cleanup() in "%s".' % (_target_path_)
		fpath = target_path
		_total_bytes = 0
		_num_files = 0
		_files_ = walk_and_collect_files_from(_target_path_, topdown=True, onerror=None, rejecting_re=None)
		for f,p in _files_.iteritems():
		    _fname = p
		    print 'DEBUG: perform_disk_space_check_and_cleanup() _fname --> "%s".' % (_fname)
		    if (os.path.isdir(_fname)):
			print 'DEBUG: perform_disk_space_check_and_cleanup() _utils.isUsingWindows --> "%s".' % (_utils.isUsingWindows)
			if (_utils.isUsingWindows):
			    _cmd_ = 'rmdir /S /Q "%s"' % (_fname)
			    print 'DEBUG: %s' % (_cmd_)
			    Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
			else:
			    _cmd_ = 'rm -R -f %s' % (_fname)
			    print 'DEBUG: %s' % (_cmd_)
			    Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
		    elif (os.path.isfile(_fname)):
			_total_bytes += _utils.fileSize(_fname)
			_num_files += 1
		_avg_size = _total_bytes / _num_files if (_num_files > 0) else list(_utils.folderSize(_repo_path))[-1]
		print "DEBUG: _avg_size=%s, _total_bytes=%s, _num_backups=%s." % (format_with_commas(_avg_size),format_with_commas(_total_bytes),format_with_commas(_num_files))
		_drv_letter = os.path.splitdrive(fpath)[0]
		_free_space = diskSpace.FreeSpace(_drv_letter) * (1024*1024*1024)
		_expected_free = (_avg_size * 2)
		print "DEBUG: _free_space=%s bytes for %s but needs %s bytes." % (format_with_commas(_free_space),_drv_letter,format_with_commas(_expected_free))
		if (_expected_free >= _free_space):
		    _result = False # Prepare to cancel the backup...
		    print "DEBUG: WARNING - MUST REMOVE SOME FILES - TOO MANY BACKUPS..."
		    files = _files_.values()
		    files.sort(date_comparator)
		    print "DEBUG: BEGIN: Files List Sorted..."
		    for f in files:
			print 'DEBUG: REMOVING "%s"' % (f)
			os.remove(f)
			_tgt_ = f.replace(target_path,'')
			print 'DEBUG: _tgt_="%s"' % (_tgt_)
			if (len(_tgt_) > 0):
			    _f_ = os.path.dirname(os.path.dirname(f))
			    while (1):
				try:
				    _tst_ = _f_.split(os.sep)[-1]
				    print 'DEBUG: _tst_=("%s"), _tgt_=("%s").' % (_tst_,_tgt_)
				    if (_tst_ == _tgt_):
					print 'DEBUG:j REMOVING "%s"' % (_f_)
					os.rmdir(_f_)
				    if (len(_f_) < len(target_path)):
					print 'DEBUG: Cannot consider anything shorter than the ("%s") "%s".' % (_f_,target_path)
					break
				except Exception, ex:
				    print 'DEBUG: Cannot continue upon error which is "%s".' % (ex)
				    break
			_free_space = diskSpace.FreeSpace(_drv_letter) * (1024*1024)
			print "DEBUG: _free_space=%s bytes for %s but needs %s bytes." % (format_with_commas(_free_space),_drv_letter,format_with_commas(_expected_free))
			if (_expected_free < _free_space):
			    print "DEBUG: Should be just enough Free Space by now."
			    _result = True # allow the backup to happen...
			    break
		    print "DEBUG: END!   Files List Sorted..."
		print 'DEBUG: END! perform_disk_space_check_and_cleanup() in "%s".' % (target_path)
		return _result
	    
	    archive_path = '' # initialize in case the backup doesn't run... otherwise exception happens.
	    
	    _process_the_backup = not _isDebug
	    print "1. _process_the_backup=%s" % (_process_the_backup)
	    print 'backup_subdir is "%s".' % (backup_subdir)
	    _process_the_backup = perform_disk_space_check_and_cleanup(backup_subdir)
	    print "2. _process_the_backup=%s" % (_process_the_backup)
	    if (_process_the_backup):
		print "Backing up repository to '" + backup_subdir + "'..."
		if have_subprocess:
		    p = subprocess.Popen([svnadmin, "hotcopy", repo_dir, backup_subdir, "--clean-logs"])
		    print 'subprocess is %s or "%s".' % (p.pid,str(p))
		    __pid__ = p.pid
		    try:
			p.wait()
			err_code = p.returncode
		    except KeyboardInterrupt, SystemExit:
			if (_isDebug):
			    from vyperlogix.process import killProcByPID
			    killProcByPID(p.pid)
			    raise
		    finally:
			__pid__ = None
		else:
		    err_code = -1
		    print 'ERROR: Which version of the runtime are you using anyway ?!?'
		if err_code != 0:
		    print "Unable to backup the repository."
		    sys.exit(err_code)
		else:
		    print "Done."
	    
		def perform_cleanup(target_path):
		    fpath = target_path
		    print 'DEBUG: BEGIN: perform_cleanup() in "%s" --> "%s".' % (target_path,fpath)
		    if (_utils.isUsingWindows):
			_cmd_ = 'rmdir /S /Q "%s"' % (fpath)
			print '%s' % (_cmd_)
			Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
		    else:
			_cmd_ = 'rm -f -R %s/*' % (fpath)
			print '%s' % (_cmd_)
			try:
			    Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
			except OSError:
			    print 'DEBUG: os.curdir=%s' % (os.curdir)
		    if (os.path.exists(fpath)) and (os.path.isdir(fpath)):
			try:
			    os.removedirs(fpath)
			except:
			    os.unlink(fpath)
		    print 'DEBUG: END! perform_cleanup() in "%s".' % (target_path)
		
		def perform_backup(archive_path):
		    print 'DEBUG: BEGIN: perform_backup() --> "%s".' % (archive_path)
		    if (_utils.isUsingLinux):
			_cmd_file_ = '%s/backup.sh' % (os.path.dirname(__file__))
			_bucket_ = os.path.dirname(archive_path).split(os.sep)[-1]
			_name_ = archive_path.split(os.sep)[-1]
			if (os.path.exists(os.path.abspath(_cmd_file_))):
			    _cmd_ = '%s %s %s %s' % (_cmd_file_,_bucket_,os.path.dirname(os.path.dirname(archive_path)),_name_)
			    print '%s' % (_cmd_)
			    try:
				Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
			    except OSError, ex:
				print 'ERROR: %s' % (_utils.formattedException(details=ex))
			else:
			    print 'INFO: Cannot locate the %s shell script.' % (_cmd_file_)
			_cmd_file_ = '%s/cleanup.sh' % (os.path.dirname(__file__))
			if (os.path.exists(os.path.abspath(_cmd_file_))):
			    _cmd_ = '%s' % (_cmd_file_)
			    print '%s' % (_cmd_)
			    try:
				Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=sys.stdout)
			    except OSError:
				print 'ERROR: %s' % (_utils.formattedException(details=ex))
			else:
			    print 'INFO: Cannot locate the %s shell script.' % (_cmd_file_)
		    print 'DEBUG: END! perform_backup() in "%s".' % (archive_path)
		
		_utils.makeDirs(backup_subdir)
		### Step 4: Make an archive of the backup if required.
		if archive_type and (len(archive_type.value) > 0):
		    archive_path = backup_subdir + archive_type.value
		    err_msg = ""
	    
		    print "Archiving backup to '%s' (%s)..." % (archive_path,archive_type)
		    if (archive_type == ArchiveTypes.gz) or (archive_type == ArchiveTypes.bz2):
			try:
			    import tarfile
			    print "tarfile.open('%s', 'w:%s')" % (archive_path,archive_type.value)
			    tar = tarfile.open(archive_path, 'w:' + archive_type.name)
			    try:
				print "tar.add('%s', '%s')" % (backup_subdir,os.path.basename(backup_subdir))
				tar.add(backup_subdir, os.path.basename(backup_subdir))
			    finally:
				print "tar.close()"
				tar.close()
			except ImportError, e:
			    err_msg = "Import failed: " + str(e)
			    err_code = -2
			except tarfile.TarError, e:
			    err_msg = "Tar failed: " + str(e)
			    err_code = -3
			finally:
			    print "DEBUG: About to perform_cleanup() in '%s'." % (backup_subdir)
			    perform_cleanup(backup_subdir)
			    perform_backup(archive_path)
	    
		    elif (archive_type):
			try:
			    from vyperlogix.zip import secure
			    if (archive_type == ArchiveTypes.zip):
				secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.zip,passPhrase=_passPhrase)
			    elif (archive_type == ArchiveTypes.ezip):
				secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.ezip,_iv=_iv,passPhrase=_passPhrase)
			    elif (archive_type == ArchiveTypes.xzip):
				secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.xzip,passPhrase=_passPhrase)
			    elif (archive_type == ArchiveTypes.bzip):
				secure.zipper(backup_subdir,archive_path,archive_type=secure.ZipType.bzip,passPhrase=_passPhrase)
			except ImportError, e:
			    err_msg = "Import failed: " + str(e)
			    err_code = -4
			except Exception, e:
			    err_msg = "General Failure: " + _utils.formattedException(details=e)
			    err_code = -5
			finally:
			    print "DEBUG: About to perform_cleanup()."
			    perform_cleanup(backup_subdir)
	    
		    if err_code != 0:
			print "Unable to create an archive for the backup.\n" + err_msg
			sys.exit(err_code)
		    #else:
			#print "Archive created, removing backup '" + backup_subdir + "'..."
			#_utils.safe_rmtree(backup_subdir, 1)
	
	### Step 5: finally, remove all repository backups other than the last
	###         NUM_BACKUPS.
	    
	_path = '/home'
	cx = None
	if (_isUsingSFTP):
	    from vyperlogix.ssh import sshUtils
	    rw_mode = _mask = 0777 if (sys.platform != 'win32') else _utils.windows_mask
	    _utils.chmod_tree(backup_subdir, rw_mode, rw_mode) # counteract previous safe_rmtree() actions.
	    # copy from backup_dir to _backup_dir where _backup_dir specifies a UNC path in the form of \\server\path
	    toks = ListWrapper(_backup_dir.split('\\'))
	    for i in xrange(len(toks)):
		if (toks[i] != ''):
		    i -= 1
		    break
	    _hostname = toks[i+1]
	    print '_hostname=%s, toks=%s, i=%s' % (_hostname,toks,i)
	    cx = None
	    if (len(_hostname) > 0) and (_username) and (len(_username) > 0) and (_password) and (len(_password) > 0):
		try:
		    cx = sshUtils.SSHConnection(hostname=_hostname,username=_username,password=_password)
		    if (cx.transport is None):
			print cx.lastErrorMessage
		    else:
			print 'cx.transport is %s' % (cx.transport)
			toks[i+1] = ''
			_path = cx.sep.join(toks[i+1:])
			if (not cx.exists(_path)):
			    print 'Cannot locate the target path via SSH at "%s", so cannot proceed.' % (_path)
			else:
			    _files = [f for f in os.listdir(backup_dir) if (os.path.splitext(f.lower())[-1] == '.zip')]
			    for f in _files:
				_f = os.sep.join([backup_dir,f])
				_r = cx.sep.join([_path,f])
				print 'stat of %s\n\t%s' % (_f,_utils.explain_stat(os.stat(_f),delim='\n\t'))
				cx.put(_f,_r,callback=sshUtils.giveXferStatus)
		except Exception, e:
		    print _utils.formattedException(details=e)
	_isNotUsingSFTP = (not _isUsingSFTP) or (cx is None) or (cx.transport is None)
	if num_backups > 0:
	    if (not _isSpecific):
		ext_re = ''
	    regexp = re.compile("^" + repo + "-[0-9]+(-[0-9]+)?" + ext_re + ("$" if (len(ext_re) > 0) else ''))
	    print 'DEBUG: _is_s3 is "%s"' % (_is_s3)
	    if (_is_s3):
		from vyperlogix.boto import s3
		print 'DEBUG: anS3Connection is "%s"' % (anS3Connection)
		files = s3.get_directory(__bucket_name__,aConnection=anS3Connection)
		_n_ = max(0,len(files)-num_backups)
	    else:
		directory_list = os.listdir(backup_dir) if (_isNotUsingSFTP) else cx.listdir(_path)
		old_list = filter(lambda x: regexp.search(x), directory_list)
		old_list.sort(comparator)
		_n_ = max(0,len(old_list)-num_backups)
	    print 'DEBUG: There are %d backups in "%s" with %d expected at-most.' % (_n_,backup_dir,num_backups)
	    if (_n_ > 0):
		print 'DEBUG: Ignoring these "%s".' % (old_list[_n_:])
		del old_list[_n_:]
		print 'DEBUG: There are now %d in the list to delete.' % (len(old_list))
		for item in old_list:
		    old_backup_item = os.path.join(backup_dir, item) if (_isNotUsingSFTP) else cx.sep.join([_path,item])
		    print "Removing old backup using %s: %s" % ('LOCAL-FILE-SYSTEM' if (_isNotUsingSFTP) else 'SSH',old_backup_item)
		    if (_isNotUsingSFTP):
			if os.path.isdir(old_backup_item):
			    _utils.safe_rmtree(old_backup_item, 1)
			else:
			    os.remove(old_backup_item)
		    elif (cx):
			if cx.isdir(old_backup_item):
			    cx.safe_rmtree(old_backup_item, 1)
			else:
			    cx.remove(old_backup_item)
			    
	def cleanUpCarbination(fpath):
	    _date_comparator = date_comparator
	    print 'DEBUG:  is "%s", _is_s3 is "%s"' % (_is_carbonite,_is_s3)
	    if (_is_carbonite):
		files = [os.sep.join([fpath,f]) for f in os.listdir(fpath)]
	    elif (_is_s3):
		from vyperlogix.boto import s3
		files = s3.get_directory(__bucket_name__,aConnection=anS3Connection)
		_date_comparator = s3_date_comparator
	    files.sort(_date_comparator)
	    dt = time.time()
	    _files = []
	    _fprefix = _repo_path.split(os.sep)[-1]
	    for f in files:
		_bool_ = f.find(_fprefix) > -1
		print 'DEBUG: %s :: "%s".startswith("%s")=%s' % (misc.funcName(),f,_fprefix,_bool_)
		if (_bool_):
		    print 'DEBUG:  is "%s", _is_s3 is "%s"' % (_is_carbonite,_is_s3)
		    if (_is_carbonite):
			statinfo = os.stat(f)
			t = statinfo.st_mtime
		    elif (_is_s3):
			t = f.metadata['ST_MTIME'].split('=')[0]
		    secs = dt - t
		    hours = secs / 3600
		    print >>sys.stderr, '%s.1 f=%s' % (misc.funcName(),f)
		    print >>sys.stderr, '%s.2 secs=%s, hours=%s' % (misc.funcName(),secs,hours)
		    _files.append(SmartObject.SmartFuzzyObject({'hours':hours,'secs':secs,'t':t,'fname':f}))
	    print >>sys.stderr, '%s.3 fpath=%s, len(_files)=%s' % (misc.funcName(),fpath,len(_files))
	    if (len(_files) > _carbonite_files):
		edge = 0 if (_files[-1].hours < _files[0].hours) else -1
		print >>sys.stderr, '%s.4 edge=%s because last is %s and first is %s.' % (misc.funcName(),edge,_files[-1].hours,_files[0].hours)
		#if (edge == -1):
		    #print >>sys.stderr, '%s.5 reversed !' % (misc.funcName())
		    #misc.reverse(_files)
		if (edge == -1):
		    _beginning_ = _carbonite_files
		    _ending_ = len(_files)
		else:
		    _beginning_ = 0
		    _ending_ = len(_files) - _carbonite_files
		for f in _files[_beginning_:_ending_]:
		    print >>sys.stderr, '%s.6 unlink(%s)' % (misc.funcName(),f.fname)
		    print 'DEBUG: _is_carbonite is "%s", _is_s3 is "%s"' % (_is_carbonite,_is_s3)
		    if (_is_carbonite):
			os.unlink(f.fname)
		    elif (_is_s3):
			from vyperlogix.boto import s3
			s3._delete_key_for_file(f)
	
	print >>sys.stderr, '1. _carbonite=%s, archive_path=%s' % (_carbonite,archive_path)
	print 'DEBUG:  is "%s", _is_s3 is "%s", os.path.exists("%s") is "%s"' % (_is_carbonite,_is_s3,archive_path,os.path.exists(archive_path))
	if ( (_is_carbonite) or (_is_s3) ) and (os.path.exists(archive_path)):
	    _date_comparator = date_comparator
	    if (_is_carbonite):
		directory_list = [os.sep.join([_carbonite,f]) for f in os.listdir(_carbonite) if (str(f).find(repo) > -1)]
	    elif (_is_s3):
		from vyperlogix.boto import s3
		directory_list = s3.get_directory(__bucket_name__,aConnection=anS3Connection)
		_date_comparator = s3_date_comparator
	    directory_list.sort(_date_comparator)
	    is_time_to_carbonite = True
	    print >>sys.stderr, '2. len(directory_list)=%s' % (len(directory_list))
	    _directory_list = []
	    dt = time.time()
	    for f in directory_list:
		print 'DEBUG:  _is_carbonite is "%s", _is_s3 is "%s"' % (_is_carbonite,_is_s3)
		if (_is_carbonite):
		    statinfo = os.stat(f)
		    t = statinfo.st_mtime
		elif (_is_s3):
		    t = f.metadata['ST_MTIME'].split('=')[0]
		secs = dt - t
		hours = secs / 3600
		print >>sys.stderr, '2.1 f=%s' % (f)
		print >>sys.stderr, '2.2 secs=%s, hours=%s' % (secs,hours)
		_directory_list.append(SmartObject.SmartFuzzyObject({'hours':hours,'secs':secs,'t':t}))
	    print >>sys.stderr, '%s' % (50*'=')
	    if (len(_directory_list) > 0):
		f = _directory_list[-1 if (_directory_list[-1].hours < _directory_list[0].hours) else 0]
		print >>sys.stderr, '2.3 secs=%s, hours=%s' % (f.secs,f.hours)
		is_time_to_carbonite = f.hours >= _carbonite_hours
	    print >>sys.stderr, '3. is_time_to_carbonite=%s' % (is_time_to_carbonite)
	    _carbonite_target = _carbonite
	    _carbonite_target_alt = _carbonite_alt
	    if (is_time_to_carbonite):
		print 'DEBUG:  _is_carbonite is "%s", _is_s3 is "%s"' % (_is_carbonite,_is_s3)
		if (_is_carbonite):
		    cs_day_ = None
		    if (_carbonite_schedule.has_key('_day_')):
			cs_day_ = _carbonite_schedule['_day_']
		    cs_hour_ = _utils.hour_of_day()
		    cs_days_ = None
		    if (_carbonite_schedule.has_key('days')):
			cs_days_ = _carbonite_schedule['days'] if (cs_day_.value in _carbonite_schedule['days']) else None
		    cs_hours_ = None
		    if (_carbonite_schedule.has_key('hours')):
			cs_hours_ = _carbonite_schedule['hours'] if (cs_hour_ in _carbonite_schedule['hours']) else None
		    cs_type_ = None
		    if (_carbonite_schedule.has_key('type')):
			cs_type_ = _carbonite_schedule['type']
			if (not cs_days_) or (not cs_hours_):
			    cs_type_ = None
			    if (is_type_alternate(cs_type_)):
				cs_type_ = BackupTypes.Primary
				_carbonite_target = _carbonite
				_carbonite_target_alt = _carbonite_alt
			    else:
				cs_type_ = BackupTypes.Alternate
				_carbonite_target = _carbonite_alt
				_carbonite_target_alt = _carbonite
			else:
			    if (is_type_alternate(cs_type_)):
				_carbonite_target = _carbonite_alt
				_carbonite_target_alt = _carbonite
			    else:
				_carbonite_target = _carbonite
				_carbonite_target_alt = _carbonite_alt
    
		    while (1):
			try:
			    _dest_fname = os.sep.join([_carbonite_target,os.path.basename(archive_path)])
			    p = list(os.path.splitext(_dest_fname))
			    p[0] = p[0].replace('.','_')
			    _dest_fname = ''.join(p)
			    _utils.copyFile(archive_path,_dest_fname)
			    if (_carbonite_optimize):
				os.unlink(archive_path)
			    break
			except:
			    if (_carbonite_target == _carbonite_target_alt):
				break # already done it so stop doing it !!!
			    _carbonite_target = _carbonite_target_alt
		elif (_is_s3):
		    from vyperlogix.boto import s3
		    s3.set_contents_from_file(__bucket_name__, archive_path, reduced_redundancy=True, callback=None, aConnection=anS3Connection)
	    cleanUpCarbination(_carbonite_target)
	    pass
	if (not _isNotUsingSFTP):
	    try:
		print 'Closing connection to %s' % (cx.transport)
		cx.close()
	    except:
		pass
	if (_isUsingSFTP):
	    print '_utils.removeAllFilesUnder(%s)' % (backup_dir)
	    _utils.removeAllFilesUnder(backup_dir)
	    
	ioTimeAnalysis.ioEndTime(__name__)
	ioTimeAnalysis.ioTimeAnalysisReport(fOut=sys.stdout)

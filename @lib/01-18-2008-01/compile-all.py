import re
import os,sys
import platform
import compileall

import zipfile

from vyperlogix.misc import _utils

_use_zipfile = True

_target_folder = "J:\@6"

_name = os.path.basename(os.path.basename(sys.argv[0]))
print _name

def collect_files_using(top,pattern,rejecting_re):
    _files = []
    for top,dirs,files in _utils.walk(os.path.abspath(top),rejecting_re=rejecting_re):
        for fn in [os.path.join(top,f) for f in files if (f.endswith(pattern))]:
            _files.append(fn)
    return _files

def main():
    global _is_target_folder_valid
    __vyperlogix__ = 'vyperlogix'
    fp = os.path.abspath(__vyperlogix__)
    
    _has_vyperlogix = False
    for f in sys.path:
        if (os.path.isdir(f)):
            files = os.listdir(f)
            if (__vyperlogix__ in files):
                _has_vyperlogix = True
                break
        if (str(f).find(__vyperlogix__) > -1):
            _has_vyperlogix = True
            break
        
    _bias = os.path.dirname(fp)
    print '_bias --> "%s" ...' % (_bias)
    _bias_name = fp.split(os.sep)[-1]
    print '_bias_name --> "%s" ...' % (_bias_name)

    if (not _has_vyperlogix):
        sys.path.insert(0,_bias)

    _normalized_name = lambda name:'%s_%s'%(name,'_'.join(platform.python_version().split('.')))
    normalized_name = lambda name:'%s_%s'%(name,platform.python_version())
    
    _target_folder = os.sep.join([_bias,normalized_name('dist')])
    _utils._makeDirs(_target_folder)
    _utils.removeAllFilesUnder(_target_folder)
    _utils._makeDirs(_target_folder)
    _is_target_folder_valid = (os.path.exists(_target_folder)) and (os.path.isdir(_target_folder))
    print '_is_target_folder_valid --> "%s" ...' % (_is_target_folder_valid)
    compileall.compile_dir(fp, rx=re.compile('/[.]svn'), force=True)
    
    if (_is_target_folder_valid):
        print 'Collecting .pyc files...',
        pyc_files = collect_files_using(fp,'.pyc',re.compile('/[.]svn'))
        
        if (len(pyc_files) > 0):
            print 'Removing .pyc files...\n(+++)','\n'.join(pyc_files),
            for f in pyc_files:
                os.remove(f)
            print 'Done !'
        else:
            print 'There are NO .pyc files.'
        
        print 'Collecting .pyo files...',
        pyo_files = collect_files_using(fp,'.pyo',re.compile('/[.]svn'))
        
        if (len(pyo_files) > 0):
            print 'Renaming .pyo --> .pyc ...\n(+++)','\n'.join(pyo_files),
            for f in pyo_files:
                f_new = '.'.join([os.path.splitext(f)[0],'pyc'])
                os.rename(f,f_new)
            print 'Done !'
        else:
            print 'There are NO .pyo files.'
    
    print 'Making dist folder...',
    
    _dist_folder = _target_folder
    print 'Done !'
    
    print 'Collecting .pyc files again...',
    pyc_files = collect_files_using(fp,'.pyc',re.compile('/[.]svn'))

    if (_use_zipfile == True):
        zf_name = '%s.zip' % (_bias_name)
        zf_name = '%s%s%s' % (_dist_folder,os.sep,zf_name)
        print 'Moving .pyc --> "%s" ...' % (zf_name)
        zf = zipfile.PyZipFile(zf_name, mode='w')
    else:
        print 'Moving .pyc --> "%s" ...' % (_dist_folder)
        
    for f in pyc_files:
        if (_use_zipfile == False):
            f_new = os.path.join(_dist_folder,os.path.basename(f))
            if (os.path.exists(f_new)):
                os.remove(f_new)
            if (f.find(_name) > -1):
                os.remove(f)
            else:
                try:
                    os.rename(f,f_new)
                except WindowsError, _details:
                    info_string = _utils.formattedException(details=_details)
                    print info_string
        else:
            try:
                f_new = f.replace(_bias,'')
                print '\tAdding %s --> "%s" ...' % (f,f_new)
                zf.write(f,f_new)
            except:
                zf.close()
                break
    if (_use_zipfile == True):
        zf.close()
        for name in zf.namelist():
            print name
        ftoks = list(os.path.splitext(zf_name))
        ftoks[0] = _normalized_name(ftoks[0])
        _zf_name = ''.join(ftoks)
        os.rename(zf_name,_zf_name)
    print 'Done !'
    
if (__name__ == '__main__'):
    try:
        from vyperlogix.misc import _psyco
        _psyco.importPsycoIfPossible(func=main)
    except Exception, ex:
        print >>sys.stderr, _utils.formattedException(details=ex)
    print 'BEGIN !'
    try:
        main()
    except Exception, ex:
        print >>sys.stderr, _utils.formattedException(details=ex)
    print 'END !'

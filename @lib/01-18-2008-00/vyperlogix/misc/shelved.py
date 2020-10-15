from win32api import GetComputerName
import shelve

class persistence(object):
    def __init__(self, fname):
        self.__fname = fname
        self.__isUsingSpecificFileName = False

    def set_isUsingSpecificFileName(self,bool):
        self.__isUsingSpecificFileName = bool
    
    def get_isUsingSpecificFileName(self):
        return self.__isUsingSpecificFileName
    
    def set_fname(self,fname):
        self.__fname = fname
        self.isUsingSpecificFileName = True
    
    def get_fname(self):
        return self.__fname
    
    def getShelvedFileName(self):
        if (self.isUsingSpecificFileName):
            return self.fname
        else:
            return '%s_%s_%s.dat' % (self.fname,__name__,GetComputerName())
    
    def shelveThis(self,key,value):
        handle = shelve.open(self.getShelvedFileName())
        handle[key] = value
        handle.close()
    
    def unShelveThis(self,key):
        value = ''
        fname = self.getShelvedFileName()
        try:
            handle = shelve.open(fname)
            if (handle.has_key(key)):
                try:
                    value = handle[key]
                except Exception, details:
                    print 'Unable to un-shelve from "%s" due to "%s".' % (fname,str(details))
                finally:
                    handle.close()
        except:
            print 'Unable to un-shelve from "%s", probably due to a faulty path name.' % fname
        return value

    fname = property(get_fname, set_fname)
    isUsingSpecificFileName = property(get_isUsingSpecificFileName, set_isUsingSpecificFileName)

from vyperlogix.misc import _utils

class LastErrorMixin():
    def __init__(self):
	self.__last_error = ''

    def last_error():
        doc = "last_error"
        def fget(self):
            return self.__last_error
        def fset(self, last_error):
            self.__last_error = last_error
        return locals()
    last_error = property(**last_error())

	

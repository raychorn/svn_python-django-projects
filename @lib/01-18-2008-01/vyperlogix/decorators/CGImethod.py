class CGImethod(object):
    def __init__(self,title):
        self.title = title
    def __call__(self,fn):
        def wrappedFn(*args):
            print "Content-Type: text/html\n\n"
            print "<HTML>"
            print "<HEAD><TITLE>%s</TITLE></HEAD>" % self.title
            print "<BODY>"
            try:
                fn(*args)
            except Exception,e:
                print
                print e
            print
            print "</BODY></HTML>"

        return wrappedFn

from django.core.management.base import BaseCommand
from django.core.handlers.wsgi import WSGIHandler

from optparse import OptionParser, make_option

try:
    from cherrypy.wsgiserver import CherryPyWSGIServer
except ImportError:
    try:
        from wsgiserver import CherryPyWSGIServer
    except ImportError:
        try:
            from vyperlogix.sockets import CherryPyWSGIServer
        except ImportError:
            import sys
            print sys.stderr, 'ERROR: Cannot use the %s command because cannot import CherryPyWSGIServer from the known sources.' % (__name__)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-h", "--host", dest="host", default="127.0.0.1"),
        make_option("-p", "--port", dest="port", default=9001),
        make_option("-d", "--daemon", dest="daemonize", action="store_true"),
    )

    def handle(self, *args, **options):
        import sys
        print >>sys.stderr, 'CherryPyWSGIServer(%s,%s)' % (options["host"],options["port"])
        server = CherryPyWSGIServer((options["host"], options["port"]), WSGIHandler())
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()
            
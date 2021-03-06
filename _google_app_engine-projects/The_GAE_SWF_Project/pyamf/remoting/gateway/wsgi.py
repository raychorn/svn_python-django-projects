# Copyright (c) 2007-2008 The PyAMF Project.
# See LICENSE for details.

"""
WSGI server implementation.

The Python Web Server Gateway Interface (WSGI) is a simple and universal
interface between web servers and web applications or frameworks.

The WSGI interface has two sides: the "server" or "gateway" side, and the
"application" or "framework" side. The server side invokes a callable
object (usually a function or a method) that is provided by the application
side. Additionally WSGI provides middlewares; a WSGI middleware implements
both sides of the API, so that it can be inserted "between" a WSGI server
and a WSGI application -- the middleware will act as an application from
the server's point of view, and as a server from the application's point
of view.

@see: U{WSGI homepage (external)<http://wsgi.org>}
@see: U{PEP-333 (external)<http://www.python.org/peps/pep-0333.html>}

@author: U{Nick Joyce<mailto:nick@boxdesign.co.uk>}
@since: 0.1.0
"""

import pyamf
from pyamf import remoting
from pyamf.remoting import gateway

__all__ = ['WSGIGateway']

class WSGIGateway(gateway.BaseGateway):
    """
    WSGI Remoting Gateway.
    """

    def getResponse(self, request, environ):
        """
        Processes the AMF request, returning an AMF response.

        @param request: The AMF Request.
        @type request: L{Envelope<pyamf.remoting.Envelope>}
        @rtype: L{Envelope<pyamf.remoting.Envelope>}
        @return: The AMF Response.
        """
        response = remoting.Envelope(request.amfVersion, request.clientType)

        for name, message in request:
            processor = self.getProcessor(message)
            response[name] = processor(message, http_request=environ)

        return response

    def badRequestMethod(self, environ, start_response):
        """
        Return HTTP 400 Bad Request.
        """
        response = "400 Bad Request\n\nTo access this PyAMF gateway you " \
            "must use POST requests (%s received)" % environ['REQUEST_METHOD']

        start_response('400 Bad Request', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response))),
        ])

        return [response]

    def __call__(self, environ, start_response):
        """
        @type environ:
        @param environ:
        @type start_response:
        @param start_response:

        @rtype: C{StringIO}
        @return: File-like object.
        """
        if environ['REQUEST_METHOD'] != 'POST':
            return self.badRequestMethod(environ, start_response)

        body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
        stream = None

        context = pyamf.get_context(pyamf.AMF0)

        # Decode the request
        try:
            request = remoting.decode(body, context)
        except pyamf.DecodeError:
            self.logger.debug(gateway.format_exception())

            response = "400 Bad Request\n\nThe request body was unable to " \
                "be successfully decoded."

            if self.debug:
                response += "\n\nTraceback:\n\n%s" % gateway.format_exception()

            start_response('400 Bad Request', [
                ('Content-Type', 'text/plain'),
                ('Content-Length', str(len(response))),
            ])

            return [response]

        # Process the request
        try:
            response = self.getResponse(request, environ)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.logger.debug(gateway.format_exception())

            response = "500 Internal Server Error\n\nThe request was " \
                "unable to be successfully processed."

            if self.debug:
                response += "\n\nTraceback:\n\n%s" % gateway.format_exception()

            start_response('500 Internal Server Error', [
                ('Content-Type', 'text/plain'),
                ('Content-Length', str(len(response))),
            ])

            return [response]

        # Encode the response
        try:
            stream = remoting.encode(response, context)
        except pyamf.EncodeError:
            self.logger.debug(gateway.format_exception())

            response = "500 Internal Server Error\n\nThe request was " \
                "unable to be encoded."

            if self.debug:
                response += "\n\nTraceback:\n\n%s" % gateway.format_exception()

            start_response('500 Internal Server Error', [
                ('Content-Type', 'text/plain'),
                ('Content-Length', str(len(response))),
            ])

            return [response]

        response = stream.getvalue()

        start_response('200 OK', [
            ('Content-Type', remoting.CONTENT_TYPE),
            ('Content-Length', str(len(response))),
        ])

        return [response]

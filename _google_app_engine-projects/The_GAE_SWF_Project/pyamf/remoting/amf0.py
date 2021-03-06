# Copyright (c) 2007-2008 The PyAMF Project.
# See LICENSE for details.

"""
AMF0 Remoting support.

@author: U{Nick Joyce<mailto:nick@boxdesign.co.uk>}

@since: 0.1.0
"""

import traceback, sys

from pyamf import remoting
from pyamf.remoting import gateway

class RequestProcessor(object):
    def __init__(self, gateway):
        self.gateway = gateway

    def authenticateRequest(self, request, service_request, *args, **kwargs):
        """
        Authenticates the request against the service.

        @param request: The AMF request
        @type request: L{Request<pyamf.remoting.Request>}
        """
        username = password = None

        if 'Credentials' in request.headers:
            cred = request.headers['Credentials']

            username = cred['userid']
            password = cred['password']

        return self.gateway.authenticateRequest(service_request, username, password, *args, **kwargs)

    def buildErrorResponse(self, request, error=None):
        """
        Builds an error response.

        @param request: The AMF request
        @type request: L{Request<pyamf.remoting.Request>}
        @return: The AMF response
        @rtype: L{Response<pyamf.remoting.Response>}
        """
        if error is not None:
            cls, e, tb = error
        else:
            cls, e, tb = sys.exc_info()

        return remoting.Response(build_fault(cls, e, tb), status=remoting.STATUS_ERROR)

    def _getBody(self, request, response, service_request, **kwargs):
        if 'DescribeService' in request.headers:
            return service_request.service.description

        return self.gateway.callServiceRequest(service_request, *request.body, **kwargs)

    def __call__(self, request, *args, **kwargs):
        """
        Processes an AMF0 request.

        @param request: The request to be processed.
        @type request: L{Request<pyamf.remoting.Request>}

        @return: The response to the request.
        @rtype: L{Response<pyamf.remoting.Response>}
        """
        response = remoting.Response(None)

        try:
            service_request = self.gateway.getServiceRequest(request, request.target)
        except gateway.UnknownServiceError, e:
            return self.buildErrorResponse(request)

        # we have a valid service, now attempt authentication
        try:
            authd = self.authenticateRequest(request, service_request, *args, **kwargs)
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            return self.buildErrorResponse(request)

        if not authd:
            # authentication failed
            response.status = remoting.STATUS_ERROR
            response.body = remoting.ErrorFault(code='AuthenticationError',
                description='Authentication failed')

            return response

        # authentication succeeded, now fire the preprocessor (if there is one)
        try:
            self.gateway.preprocessRequest(service_request, *args, **kwargs)
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            return self.buildErrorResponse(request)

        try:
            response.body = self._getBody(request, response, service_request, *args, **kwargs)

            return response
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            return self.buildErrorResponse(request)

def build_fault(cls, e, tb):
    """
    Builds a L{remoting.ErrorFault} object based on the last exception raised.
    """
    if hasattr(cls, '_amf_code'):
        code = cls._amf_code
    else:
        code = cls.__name__

    return remoting.ErrorFault(code=code, description=str(e),
        details=str(traceback.format_exception(cls, e, tb)).replace("\\n", ''))

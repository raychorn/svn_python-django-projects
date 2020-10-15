from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseNotModified

import os, sys

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.django import pages

from vyperlogix.django import django_utils

from vyperlogix.hash import lists

try:
    from settings import MEDIA_ROOT
except ImportError:
    MEDIA_ROOT = '/static/'
    
try:
    from settings import __title__
except ImportError:
    __title__ = 'Vyper Logix Corp.'

__cache__ = lists.HashedLists2()

def serve(fullpath):
    import mimetypes
    import rfc822
    import os
    import stat
    
    response = __cache__[fullpath]
    if (not response):
	mimetype = mimetypes.guess_type(fullpath)[0]
	fh = open(fullpath, 'rb')
	try:
	    contents = fh.read()
	except:
	    contents = ''
	finally:
	    fh.close()
	response = HttpResponse(contents, mimetype=mimetype)
	statobj = os.stat(fullpath)
	response["Last-Modified"] = rfc822.formatdate(statobj[stat.ST_MTIME])
	__cache__[fullpath] = response
    return response

def static(request):
    from django.conf import settings
    url_toks = django_utils.parse_url_parms(request)
    fpath = '/'.join([settings.MEDIA_ROOT,_utils.eat_leading_token_if_empty(request.path,delim='/')]).replace('/static/media/','/static/').replace('/',os.sep).replace(os.sep.join(['static','static']),os.sep.join(['static']))
    if (os.path.exists(fpath)):
	try:
	    return serve(fpath)
	except:
	    return HttpResponseNotAllowed(pages._render_the_page(request,__title__,'405.html',None,None,context={}))
    return HttpResponseNotFound(pages._render_the_page(request,__title__,'404.html',None,None,context={}))

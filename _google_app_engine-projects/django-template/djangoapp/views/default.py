##################################################################
## To-Do:
##
##  Bugs:
##  
##################################################################

from django.template.loader import get_template_from_string
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q

import mimetypes

import os, sys
import re

#from content import models as content_models

import urllib

import socket

#from vyperlogix import misc

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'Vyper-Menu&trade;'
__version__ = '1.0.0.0'

__content__ = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><title>{{ title }}</title></head><body>{{ body }}</body></html>'''

def default(request):
    global _title
    
    try:
	s_response = '';
	t = get_template_from_string(__content__)
	c = {'title':_title,'body':'<b>Hello World!</b>'}
	content = t.render(Context(c))
	return HttpResponse(content,mimetype='text/html')
    except Exception, e:
	info_string = '' #_utils.formattedException(details=e)
	mimetype = mimetypes.guess_type('.html')[0]
	return HttpResponse('<br/>'.join(info_string.split('\n')), mimetype=mimetype)


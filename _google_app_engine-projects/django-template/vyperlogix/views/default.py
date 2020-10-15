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

import model


_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'Vyper-Menu&trade;'
__version__ = '1.0.0.0'

__content__ = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><title>{{ title }}</title></head><body>{{ body }}</body></html>'''

__upload_form__ = '''<form enctype="multipart/form-data" action="/upload" method="post">
<input type="file" name="myfile" />
<input type="submit" />
</form>'''

def upload(request) :
    file_contents = request.get('myfile')
    file_name = request.get('filename')
    obj = model.BlobModel()
    obj.blob = db.Blob( file_contents )
    obj.name = file_name
    obj.put()
    
def download(request, id) :
    obj = model.BlobModel.all().filter("id", id).get()
    
def default(request):
    global _title

    try:
        s_response = '';
        t = get_template_from_string(__content__)
        c = {'title':_title,'body':__upload_form__}
        content = t.render(Context(c))
        return HttpResponse(content,mimetype='text/html')
    except Exception, e:
        info_string = '' #_utils.formattedException(details=e)
        mimetype = mimetypes.guess_type('.html')[0]
        return HttpResponse('<br/>'.join(info_string.split('\n')), mimetype=mimetype)


from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

import sys

from vyperlogix.misc import _utils

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

import urllib

from google.appengine.api import memcache

_navigation_tabs = memcache.get("_navigation_tabs")
_navigation_menu_type = memcache.get("_navigation_menu_type")

_title = memcache.get("_title")

def default(request):
    from models import Node
    return pages.render_the_page(request,'%s' % (_title),'_home.html',_navigation_menu_type,_navigation_tabs,context={})

def about(request):
    return pages.render_the_page(request,'About - %s' % (_title),'_about.html',_navigation_menu_type,_navigation_tabs,context={})


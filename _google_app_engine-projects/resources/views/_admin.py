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

conn_str = memcache.get("conn_str")

def _admin(request):
    from models import Node

    items = Node.objects.all()
    
    if (len(items) == 0):
        aNode = Node(id='-1', name='Top', parent=-1, creation_date=_utils.today_localtime(),modification_date=_utils.today_localtime(),is_active=True,is_file=False,is_url=False)
        aNode.save()
        i = aNode.id
    
    items = Node.objects.all()

    h = oohtml.Html()
    ul = h.tag(oohtml.oohtml.UL)
    for item in items:
        ul._tagLI(item.name)
    content = h.toHtml()
    
    c = {'ADMIN_CONTENT': content}
    return pages.render_the_page(request,'%s' % (_title),'_admin.html',_navigation_menu_type,_navigation_tabs,context=c)


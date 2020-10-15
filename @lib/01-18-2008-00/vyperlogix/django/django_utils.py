__copyright__ = """\
(c). Copyright 1990-2008, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

import socket

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.lists import ListWrapper
from vyperlogix.hash import lists

from vyperlogix.misc import ObjectTypeName

__staging__ = ['ubuntu.localdomain','ubuntu3.gateway.2wire.net']

__production__ = ['ubuntu2.gateway.2wire.net','ubuntu4.gateway.2wire.net','ubuntu5','ubuntu4.web20082']

__both__ = __staging__ + __production__

isStaging = lambda _cname:(_cname in __staging__)

isProduction = lambda _cname:(_cname in __production__)

isBeingDebugged = lambda host:(any([host.find(name) > -1 for name in ['rhorn.', '.dyn-o-saur.com', '127.0.0.1', 'localhost']]))

_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()

settings = None

is_Production = isProduction(_cname)

is_Staging = isStaging(_cname)

_int = lambda value:int(value) if (str(value).isdigit()) else value

render_template_with_context = lambda t,c:t.render(c) if (not misc.isString(t)) else render_from_string(t,context=c)

def site_id_for_requestor(request):
    from django.contrib.sites.models import Site
    
    try:
	sites = Site.objects.filter(domain=request.META['HTTP_HOST'])
	if (sites.count() == 0):
	    sites = Site.objects.all()[0]
	settings.SITE_ID = sites[0].id
    except:
	pass

def is_method_post(request):
    try:
	return request.method == 'POST'
    except:
	pass
    return False

def get_from_session(request,name,default=None):
    from vyperlogix.hash import lists
    from vyperlogix.classes.SmartObject import PyroSmartObject

    try:
	obj = request.session.get(name, default)
	return [o if (not lists.isDict(o)) else PyroSmartObject(o) for o in obj] if (misc.isList(obj)) else obj if (not lists.isDict(obj)) else PyroSmartObject(obj)
    except:
	pass
    return ''

def get(_dict,name,default=None):
    try:
	if (_dict.has_key(name)):
	    return _int(_dict[name])
    except:
	pass
    return default

def get_from_post(request,name,default=None):
    return get(request.POST,name,default=default)

def get_from_post_or_get(request,name,default=None):
    if (is_method_post(request)):
	return get(request.POST,name,default=default)
    else:
	return get(request.GET,name,default=default)
    return default

def get_from_get(request,name,default=None):
    return get(request.GET,name,default=default)

def get_from_environ(request,key,default=None):
    try:
	return _int(request.environ[key])
    except:
	try:
	    return _int(request.META[key])
	except:
	    return default
    return default

def parse_Query_String(request):
    return ListWrapper.ListWrapper([tuple(t.split('=')) for t in get(request.META,'QUERY_STRING','').split('&')])

def parse_Secure_Query_String(request):
    from vyperlogix.products import keys
    def decode(value):
	try:
	    return keys._decode(value)
	except:
	    pass
	return value
    return ListWrapper.ListWrapper([tuple(t.split('=')) for t in decode(get(request.META,'QUERY_STRING','')).split('&')])

def parse_url_parms(request):
    import urllib
    return [urllib.unquote_plus(t.strip()) for t in request.META['PATH_INFO'].split('/') if (len(t.strip()) > 0)]

def d_parms(url_toks):
    from vyperlogix.hash import lists
    
    url_toks = url_toks if (misc.isList(url_toks)) else []
    t = url_toks[1:]
    if (len(t) % 2 != 0):
	t.append('')
    return lists.HashedLists2(dict([tuple(t)]))

def patterns_insert(prefix, pattern_list, index, tuples):
    from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
    
    pattern_list = pattern_list if (misc.isList(pattern_list)) else [pattern_list]
    for t in tuples:
        regex, view_or_include = t[:2]
        default_kwargs = t[2:]
        if type(view_or_include) == list:
            pattern_list.append(RegexURLResolver(regex, view_or_include[0], *default_kwargs))
        else:
            pattern_list.append(RegexURLPattern(regex, prefix and (prefix + '.' + view_or_include) or view_or_include, *default_kwargs))
    return pattern_list

def load_content_from_template(template_name,context):
    from django.template import Context
    from django.template.loader import get_template
    
    t_body_tag = get_template(template_name)
    c = Context(context, autoescape=False)
    return t_body_tag.render(c)

def render_from_string(source,context={}):
    from django.template import Context
    from django.template import loader
    from django.template.loader import get_template
    
    _content = ''
    tplate = source
    if (misc.isString(source)):
	tplate = loader.get_template_from_string(source)
    if (ObjectTypeName.typeClassName(tplate) == 'django.template.Template'):
	_content = tplate.render(Context(context, autoescape=False))
    return _content
    
def paginate(items,items_name,selector,pageNo=1,numPerPage=10,maxPages=15,callback=None):
    from vyperlogix.html import myOOHTML as oohtml

    def navigate_pages():
        articles.append(['<hr align="left" color="silver" width="80%"/>'])
        articles.append(['<h3>More %s...</h3>' % (items_name)])
        _get_page_link_ = lambda pg,n,m:oohtml.renderAnchor('%s' % ('/%s/%s/%s/%d/' % (selector,m,pg,numPerPage)),n,target='_top')
        _get_page_link = lambda pg,n:_get_page_link_(pg,n,'page')
        get_page_link = lambda pg:_get_page_link(pg.replace('+',''),pg)
        pageLinks = [oohtml.renderAnchor('%s' % ('/%s/%s/%s/%d/' % (selector,'page',1,numPerPage)),'Start',target='_top') if (pageNo > 1) else 'Start',oohtml.renderAnchor('%s' % ('/%s/%s/%s/%d' % (selector,'page',pageNo-1,numPerPage)),'Prev',target='_top') if (pageNo > 1) else 'Prev']
        r = ['%d'%(i) for i in xrange(pageNo,totalPages+1 if (pageNo > totalPages-numPerPage) else pageNo+numPerPage)]
	if (len(r) < numPerPage):
	    pg = pageNo-(numPerPage-len(r))
	    if (pg < 1):
		pg = 1
	    r = ['%d'%(i) for i in xrange(pg,pageNo)] + r
	isAtEnd = False
	if (int(r[-1]) < totalPages):
	    r[-1] = '%s+'%(r[-1])
	else:
	    isAtEnd = True
        pageLinks += [get_page_link(i) if (int(i.replace('+','')) != pageNo) else '%s'%(i) for i in r]
        pageLinks += [_get_page_link_(pageNo+1,'Next','next')  if (pageNo < totalPages) else 'Next',_get_page_link(totalPages,'End') if (not isAtEnd) else 'End']
        delim = '&nbsp;'*5
        articles.append(['<small>%s</small>' % (delim.join(pageLinks))])
        articles.append(['<center><small>Page %d of %d</small></center>' % (pageNo,totalPages)])
        articles.append(['<hr align="left" color="silver" width="80%"/>'])
    
    h = oohtml.Html()
    articles = []
    totalNum = len(items)
    totalPages = (totalNum / numPerPage) + (1 if ((totalNum % numPerPage) > 0) else 0)

    if (totalNum > numPerPage):
        navigate_pages()
	
    iBegin = (pageNo-1)*numPerPage
    iEnd = iBegin+numPerPage
    for item in items[iBegin:iEnd]:
        try:
            if (callable(callback)):
                callback(item,articles,items_name,selector)
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            return info_string
    if (totalNum > numPerPage):
        navigate_pages()
    h.html_simple_table(articles)
    content = h.toHtml()
    return content

def __init__(_root_,isAdjustingPath=False):
    '''Initialize the sys.path for django under win32.'''
    import os, sys
    
    if (sys.platform == 'win32'):
	if (isAdjustingPath):
	    pass
	from vyperlogix import misc
	from vyperlogix.django import django_utils
	from vyperlogix.lists.ListWrapper import ListWrapper
	
	fp = os.path.dirname(os.path.abspath(_root_))
	while (fp.split(os.sep)[-1].find('django') > -1):
	    fp = os.path.dirname(fp)
	s = ListWrapper(sys.path)
	l = ListWrapper(list(set(s.findAllContaining(fp))))
	t = os.path.join(fp,'django')
	if (os.path.exists(t)):
	    l.append(t)
	    i = l.findFirstMatching(fp)
	    if (i > -1):
		del l[i]
	l = misc.sort(l)
	for item in l:
	    i = s.findFirstMatching(item)
	    while (i > -1):
		del s[i]
		i = s.findFirstMatching(item)
	sys.path = s.copy()
	for item in misc.reverse(l):
	    sys.path.insert(0, item)
	return 'settings'
    else:
	fpath = os.path.dirname(os.path.abspath(_root_))
	if (fpath not in sys.path):
	    sys.path.insert(0, fpath)
	return '%s.settings' % (fpath.split(os.sep)[-1])

def get_http_host(request):
    return request.META['HTTP_X_FORWARDED_SERVER'] if (request.META.has_key('HTTP_X_FORWARDED_SERVER')) else request.META['HTTP_HOST'] if (request.META.has_key('HTTP_HOST')) else ''

def get_fully_qualified_http_host(request):
    host = get_from_environ(request,'HTTP_X_FORWARDED_HOST',get_http_host(request))
    toks = host.split(':')
    port = toks[-1]
    host = toks[0]
    port = int(port) if (port.isdigit()) else 80
    isPort = port not in [80,443]
    return '%s%s%s' % (host,':' if (isPort) else '',port if (isPort) else '')

def is_request_HTTPS(request):
    _port = get_from_environ(request,'SERVER_PORT',80)
    return (_port == 443) if (is_Production or is_Staging) else True

def get_server_name(request,default='vyperlogix.com'):
    _servername = get_from_environ(request,'SERVER_NAME',default).replace('www.','')
    _servername = _servername if (_servername.find('127.0.0.1') == -1) and (_servername.find('localhost') == -1) else default
    return _servername

def seek_installed_apps(_root,INSTALLED_APPS=()):
    import os, re
    _reSVN = re.compile(r"[._]svn\Z")
    _re = re.compile(r"__init__\.py|models\.py|views\.py")
    td = list(INSTALLED_APPS)
    if (os.path.exists(_root)):
	_dirs = []
	for f in os.listdir(_root):
	    if (not _reSVN.search(f)):
		fp = os.path.join(_root,f)
		if (os.path.isdir(fp)):
		    d = lists.HashedLists2()
		    for ff in os.listdir(fp):
			if _re.search(ff) and (d[ff] is None):
			    d[ff] = 1
		    if (len(d) == 3):
			_dirs.append(f)
	for dName in _dirs:
	    td.append(dName)
    return tuple(td)

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

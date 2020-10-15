import os
import uuid
import logging

from django.conf import settings

from django.template import RequestContext

from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.shortcuts import render_to_response

from vyperlogix.django import django_utils

from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.classes.SmartObject import SmartObject, SmartFuzzyObject

from vyperlogix.enum.Enum import Enum

from vyperlogix.django.common.API.api import API

class LoggingMode(Enum):
    none = 2^0
    info = 2^1

def __default_superuser__():
    user = SmartFuzzyObject({'is_superuser':settings.DEBUG})
    return user

def __get_user__(request):
    uid = request.session.get('_auth_user_id')
    if (uid):
	user = User.objects.get(pk=uid)
    else:
	user = __default_superuser__()
    return user

def default(request,_get_user=None,domain='localhost',secure_endpoint='http://localhost',insecure_endpoint='http://localhost',air_id=None,air_version={},apiMap=None):
    try:
	__apiMap__ = apiMap if (apiMap.isAPI) else API({},secure_endpoint,insecure_endpoint)
    except:
	__apiMap__ = API({},secure_endpoint,insecure_endpoint)
    qryObj = django_utils.queryObject(request)
    parms = django_utils.parse_url_parms(request)
    context = RequestContext(request)
    
    __domainName = domain
    
    try:
	_user = __get_user__(request) if (_get_user is None) else _get_user(request)
    except:
	user = __default_superuser__()
    _is_method_post_ = django_utils.is_method_post(request)
       
    _logging_mode = LoggingMode.none
    is_logging_info = _logging_mode == LoggingMode.info
    
    is_html = lambda url:(url.endswith('.html')) or (url.endswith('.htm'))

    try:
        s_response = ''
        __error__ = ''

        url = '/%s%s' % (str('/'.join(parms)),'/' if ( (len(parms) > 0) and (not is_html(parms[-1])) ) else '')
        
	if (is_logging_info):
	    logging.info('(1) url=%s' % (url))
	    
        if (url.find('/activate/') > -1):
            toks = ListWrapper(url.split('/'))
            i = toks.findFirstMatching('activate')
            if (i > -1):
                del toks[i+1]
            url = '/'.join(toks)
        
        browserAnalysis = django_utils.get_browser_analysis(request,parms,any([]))

	_current_site = __domainName
	_current_site = _current_site.replace('.appspot','').replace('.com','').lower()

	aid = parms[-1] if (len(parms) > 0) else ''

	get_value_from = lambda value,key,default:value[key] if (v.has_key(key)) else default
	
	_data = {
            'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),
            'browserName':browserAnalysis.browserName,
            'browserVersion':browserAnalysis.browserVersion,
            'isRunningLocal':browserAnalysis.isRunningLocal(request),
            'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,
            'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,
            'isUsingMSIE':browserAnalysis.isUsingMSIE,
            'isBrowserWebKit':browserAnalysis.isBrowserWebKit,
            'isUsingAndroid':browserAnalysis.isUsingAndroid,
            'qryObj':qryObj,
            'serial':str(uuid.uuid4()),
            'isShowingFlash':True,
            'isShowingTitleBar':True,
            'is_superuser':_user.is_superuser,
            'secure_endpoint':secure_endpoint,
            'insecure_endpoint':insecure_endpoint,
            'request_endpoint':secure_endpoint if (django_utils.is_request_HTTPS(request)) else insecure_endpoint,
            'version':air_version[air_id] if (air_version[air_id]) else settings.VERSION,
            'air_id':air_id,
	    'apiMap':dict([(' '.join([str(s).capitalize() for s in k.split('@')[-1].split('_')]),[get_value_from(v,'url','').replace('/'+k.split('@')[0],''),get_value_from(v,'isPostRequired',False),get_value_from(v,'fields',[])]) for k,v in __apiMap__.asPythonDict().iteritems() if (len(k.split('@')) == 2)])
        }

	def render_main_html(request,browserAnalysis,qryObj,is_logging_info=False):
	    if (is_logging_info):
		logging.info('render_main_html.1 --> _current_site=%s'%(_current_site))

	    if (is_logging_info):
		logging.info('(1) _data=%s' % (str(_data)))
	    try:
		response = render_to_response('main-%s.html' % (air_id), _data)
	    except TemplateDoesNotExist, e:
		if (is_logging_info):
		    info_string = _utils.formattedException(details=e)
		    logging.info('(2) %s' % (info_string))
		try:
		    response = render_to_response('main-%s.html' % (aid), _data)
		except TemplateDoesNotExist, e:
		    if (is_logging_info):
			info_string = _utils.formattedException(details=e)
			logging.info('(3) %s' % (info_string))
		    try:
			response = render_to_response('main-%s.html' % (_current_site), _data)
		    except TemplateDoesNotExist, e:
			if (is_logging_info):
			    info_string = _utils.formattedException(details=e)
			    logging.info('(4) %s' % (info_string))
			try:
			    response = render_to_response('main.html', _data)
			except TemplateDoesNotExist, e:
			    if (is_logging_info):
				info_string = _utils.formattedException(details=e)
				logging.info('(5) %s' % (info_string))
			    response = render_to_response('404.html', _data)
            django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
            return response
	
	air_id = parms[-1].split('.')[0] if (len(parms) > 0) else '' # avoid the key error that would be caused without this line of code...

	if (is_logging_info):
	    logging.info('(5) air_id=%s' % (air_id))

	__apiMap__.__specific__ = is_html(url)
	m = __apiMap__[url]
        isUrlMapped = (m != None) and (m != []) and (callable(m.func))
	if (not isUrlMapped):
	    if (not is_html(url)):
		url = '/%s%s' % (str('/'.join(parms[0:-1])),'/' if (len(parms[0:-1]) > 0) else '')
	    m = __apiMap__[url]
	    isUrlMapped = (m != None) and (m != []) and (callable(m.func))
	    if (isUrlMapped):
		air_id = aid

		if (is_logging_info):
		    logging.info('(6) air_id=%s' % (air_id))

		if (settings.IS_PRODUCTION_SERVER):
		    settings.DOMAIN_NAME = settings.APPSPOT_NAME = air_domain[air_id]
	    else:
		_m_ = [k for k in air_version.keys() if ((len(aid) > 0) and ((aid.lower().find(k.lower()) > -1) or (k.lower().find(aid.lower()) > -1))) or (k.lower().find(_current_site) > -1) or (_current_site.lower().find(k.lower()) > -1)]
		air_id = _m_[0] if (len(_m_) > 0) else air_id

		if (is_logging_info):
		    logging.info('(7) air_id=%s, _m_=%s, aid=%s' % (air_id,_m_,aid))
		
        http_host = django_utils.get_from_META(request,'HTTP_HOST',default='')
        if (__apiMap__.__secure_endpoint__.find('127.0.0.1') > -1) and (http_host.find('localhost') > -1):
            http_host = http_host.replace('localhost','127.0.0.1')
	http_host = http_host.split(':')[0]
	if (is_logging_info):
	    logging.info('(7.0) http_host=%s' % (http_host))
	    logging.info('(7.1) isUrlMapped=%s' % (isUrlMapped))
	    try:
		logging.info('(7.2) m.isPostRequired=%s' % (m.isPostRequired))
	    except:
		pass
	    logging.info('(7.3) _is_method_post_=%s' % (_is_method_post_))
	    logging.info('(7.4) __apiMap__.__secure_endpoint__=%s' % (__apiMap__.__secure_endpoint__))
	    logging.info('(7.5) settings.IS_PRODUCTION_SERVER=%s' % (settings.IS_PRODUCTION_SERVER))
	    logging.info('(7.6) django_utils.is_request_HTTPS(request)=%s' % (django_utils.is_request_HTTPS(request)))
	    logging.info('(7.7) django_utils.get_from_environ(request,\'SERVER_PORT\',80)=%s' % (django_utils.get_from_environ(request,'SERVER_PORT',80)))
	    logging.info('(7.8) django_utils.is_Production()=%s, django_utils.is_Staging()=%s' % (django_utils.is_Production(request),django_utils.is_Staging(request)))
        if (isUrlMapped) and ( ((m.isPostRequired) and _is_method_post_) or ((not m.isPostRequired) and not _is_method_post_) ) and (__apiMap__.__secure_endpoint__.find(http_host) > -1) and ( (not settings.IS_PRODUCTION_SERVER) or ((settings.IS_PRODUCTION_SERVER) and (django_utils.is_request_HTTPS(request)))): # (must be mapped), (must use POST), (must use secure endpoint) and (if production must use SSL).
            try:
                response = m.func(request,parms,browserAnalysis,air_id,__apiMap__)
		if (is_logging_info):
		    logging.info('(8) response=%s' % (response))
		    logging.info('(9) settings.APP_SESSION_KEY=%s' % (settings.APP_SESSION_KEY))
                django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
                return response
            except Exception, e:
		info_string = _utils.formattedException(details=e)
		logging.info('%s' % (info_string))
	    return render_main_html(request,browserAnalysis,qryObj,is_logging_info)
	if (air_version[air_id] is None):
	    try:
		_message = django_utils.get_from_post_or_get(request,'message','')
		if (len(_message) > 0):
		    _data['message'] = _message
		_url_ = os.sep+os.sep.join([c for c in url.split('/') if (len(c) > 0)])
		_s_ = os.sep.join([settings.MEDIA_ROOT,_url_])
		if (os.path.isfile(_s_)) and (os.path.exists(_s_)):
		    _url_ = '/static/'+'/'.join([c for c in url.split('/') if (len(c) > 0)])
		    try:
			return HttpResponseRedirect(_url_) # allow the web server to handle this rather than the application server...
		    except:
			pass
		    return django_static.serve(_s_) # if all else fails the application server should handle the request...
		_url_ = '/'.join(url.split('/')[1 if (url.startswith('/')) else 0:])
		return render_to_response(_url_, _data)
	    except TemplateDoesNotExist, e:
		try:
		    _url_ += 'index.htm'
		    return render_to_response(_url_, _data)
		except TemplateDoesNotExist, e:
		    try:
			_url_ += 'l'
			return render_to_response(_url_, _data)
		    except TemplateDoesNotExist, e:
			info_string = _utils.formattedException(details=e)
			logging.info('%s' % (info_string))
        return render_main_html(request,browserAnalysis,qryObj,is_logging_info)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        logging.warning(info_string)
        _content = '<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))) if (not browserAnalysis.isRunningLocal(request)) else ''
        response = render_to_response('main.html', {'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'content':_content,'isShowingFlash':False,'isShowingTitleBar':True})
        django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
        return response


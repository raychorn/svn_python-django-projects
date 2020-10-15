# Google App Engine for Flash projects with PyAMF. 
# Copyright (c) 2008 Aral Balkan (http://aralbalkan.com)
# Released under the Open Source MIT License
#
# Blog post: http://aralbalkan.com/1307 
# Google App Engine: http://code.google.com/appengine/
# PyAMF: http://pyamf.org

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import logging
from urlparse import urlparse
import os

from gaeswf import BaseSWFHandler

class InitialFlashExample(BaseSWFHandler):

	def get(self, path):		
		# This is the root app URL that maps to this application in app.yaml.
		# If this application is accessed from root, set appUrl = '/'. 
		# In all other cases, set appUrl to the URL defined in your app.yaml 
		# file with a trailing forward slash but _without_ a forward slashe
		# at the end (e.g. /examples/swfaddress is correct).
		appUrl = "/examples/initial/flash"

		# Path to the example SWF
		swf = 'http://' + urlparse(self.request.url).netloc + '/swfs/initial.swf';

		# Handle deep links
		self.handleDeepLinks(appUrl);

		template_values = {
			'type': 'Flash',
			'title': 'Initial Google App Engine Flash client proof-of-concept',
			'description': '',
			'appUrl': appUrl,
			'swf': swf,
			'width': '550',
			'height': '500'			
		}

		# Write out the HTML file to embed the SWF.
		# Thanks to Javier for pointing out the static_dir does _not_ work for templates.  
		# (see http://aralbalkan.com/1307#comment-135454)
		path = os.path.join(os.path.dirname(__file__), '../templates/example_initial.html')
		self.response.out.write(template.render(path, template_values, debug=True))
		
class InitialFlexExample(BaseSWFHandler):

	def get(self, path):
		
		# See comments, above, for explanations.
				
		appUrl = "/examples/initial/flex"
		swf = 'http://' + urlparse(self.request.url).netloc + '/swfs/InitialFlex.swf';

		self.handleDeepLinks(appUrl);

		template_values = {
			'type': 'Flex',
			'title': 'Initial Google App Engine Flex 3 client proof-of-concept',
			'description': '',
			'appUrl': appUrl,
			'swf': swf,
			'width': '550',
			'height': '550'			
		}

		path = os.path.join(os.path.dirname(__file__), '../templates/example_initial.html')
		self.response.out.write(template.render(path, template_values, debug=True))
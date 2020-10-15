######################################################################
#
# The GAE SWF Project (http://gaeswf.appspot.com)
#
# Main handlers for the project. All calls go through here and
# are routed accordingly to other handlers and to the 
# Flash Remoting gateway.
# 
# Copyright (c) 2008 Aral Balkan. Released under the MIT license.
#
# Learn more about Google App Engine and other cool stuff at
# the Singularity Web Conference: Online on October 24-26, 2008
# http://singularity08.com
#
# Blog: http://aralbalkan.com
#
######################################################################

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from urlparse import urlparse

import logging
import os

from examples import InitialFlashExample
from examples import InitialFlexExample
from examples import photo

from google.appengine.api import users

from google.appengine.ext import db
from examples.model import Photo

class IndexHandler(webapp.RequestHandler):

	def get(self):
		# Write out index file.
		# Thanks to Javier for pointing out the static_dir does _not_ work for templates.  
		# (see http://aralbalkan.com/1307#comment-135454)
		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path, None, debug=True))


class TestUploadHandler(webapp.RequestHandler):
	def get(self):
		
		if self.request.get('show', False):
			user = users.get_current_user()
			p = Photo.all().filter("user = ", user).get()
			if p:
				self.response.headers['Content-Type'] = "image/jpeg"
				self.response.out.write(p.fileBlob)
		else:
			self.response.out.write("""
			<form action="test" method="post" enctype="multipart/form-data">
			    <div><input type="file" id="fileUpload" name="upload" /></div>
			    <div><input type="submit" value="Upload" /></div>
			</form>""")		
		
	def post(self):

		user = users.get_current_user()
		p = Photo.all().filter("user = ", user).get()

		if p == None:
			p = Photo()
			p.user = user;
		
		fileBlob = db.Blob(self.request.get('upload'))
		
		#logging.info('====> ' + fileBlob)
		
		logging.info("[[[ " + self.request.body + "]]]")
		
		p.fileBlob = fileBlob
		p.put();
		
		self.redirect('/test?show=true')

class NotFoundHandler(webapp.RequestHandler):
	
	def get(self):
		# Not found
		template_vars = {
		'title': 'Error 404 Kitten: I\'m sorry, I tried really hard to find it.',
		'content': '<img src="/images/404kitten.jpg" width="375" height="500" alt="404 Kitten."/><p><a href="http://flickr.com/photos/mydnight296/2343975616/">Photo</a> by <a href="http://flickr.com/people/mydnight296/">Vannessa</a>.</p>'
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/simple.html')
		self.response.out.write(template.render(path, template_vars, debug=True))

def main():
	application = webapp.WSGIApplication([
		('/', IndexHandler),
		('/test', TestUploadHandler),
		('/photo/upload', photo.PhotoUploadHandler),
		('/photo/download', photo.PhotoDownloadHandler),
		('/examples/initial/flash(/.*)?', InitialFlashExample),
		('/examples/initial/flex(/.*)?', InitialFlexExample),
		('/.*', NotFoundHandler)
	], debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()

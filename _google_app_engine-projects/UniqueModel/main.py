#! /usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import controller


def main():
    app = webapp.WSGIApplication([
                                  (r'/$' , controller.UniquenessTestRequestHandler),
                                  (r'/.*' , controller.Error404RequestHandler)
                                  ], debug=True)
    run_wsgi_app(app)
    
if __name__ == '__main__':
    main()
    

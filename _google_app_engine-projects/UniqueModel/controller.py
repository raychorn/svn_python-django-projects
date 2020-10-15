from google.appengine.ext import webapp
from google.appengine.ext import db

import domain
import datetime
import burns
        
class Error404RequestHandler(webapp.RequestHandler):
    def get(self):
        self.error(400)
        self.response.out.write('<html><head><title>Error: 404</title></head><body><h3>Error: 404</h3><p>The requested page %s cannot be found.</p></body></html>'%self.request.url)
            
    
class UniquenessTestRequestHandler(webapp.RequestHandler):
    def get(self):
        tests = []
        stuff = []
        
        start = datetime.datetime.now()
        u = domain.UniqueMe(
                     unique_property = 'unique!',
                     some_other_property = 'unique 1'
                     )
        try:
            u.put()
            stuff.append(u)
            tests.append(('insert 1st UniqueMe', True))
        except burns.UniqueConstraintViolatedError:
            tests.append(('insert 1st UniqueMe', False))
        
        u1 = domain.UniqueMe(
                     unique_property = 'unique!',
                     some_other_property = 'unique 2'
                     )
        try:
            u1.put()
            tests.append(('insert 2nd UniqueMe', False))
        except burns.UniqueConstraintViolatedError:
            tests.append(('insert 2nd UniqueMe',True))
        
        u2 = domain.UniqueMe1(
                     unique_property = 'unique1!',
                     some_other_property = 'unique 1!'
                     )
        try:
            u2.put()
            stuff.append(u2)
            tests.append(('insert 1st UniqueMe1',True))
        except burns.UniqueConstraintViolatedError:
            tests.append(('insert 1st UniqueMe1',False))
        
        
        u3 = domain.UniqueMe1(
                     unique_property = 'unique1!',
                     some_other_property = 'unique 2!'
                     )
        try:
            u3.put()
            tests.append(('insert 2nd UniqueMe1',False))
        except burns.UniqueConstraintViolatedError:
            tests.append(('insert 2nd UniqueMe1',True))
            
        try:
            bu = domain.BigUnique(
                                 prop1 = 'prop1',
                                 prop2 = 'prop2',
                                 prop3 = 'prop3',
                                 prop4 = 'prop4',
                                 prop5 = 'prop5'
                             )
            bu.put()
            stuff.append(bu)
            tests.append(('insert 1st BigUnique',True))
        except burns.UniqueConstraintViolatedError:
            tests.append(('insert 1st BigUnique', False))
            
        try:
            domain.BigUnique(
                                 prop1 = 'prop1',
                                 prop2 = 'prop22',
                                 prop3 = 'prop33',
                                 prop4 = 'prop4',
                                 prop5 = 'prop5'
                             ).put()
            tests.append(('insert 2nd BigUnique',False))
        except burns.UniqueConstraintViolatedError:
            tests.append(('insert 2nd BigUnique', True))
            
        try:
            domain.BigUnique(
                                 prop1 = 'prop11',
                                 prop2 = 'prop2',
                                 prop3 = 'prop3',
                                 prop4 = 'prop4',
                                 prop5 = 'prop5'
                             ).put()
            tests.append(('insert 3rd BigUnique',False))
        except burns.UniqueConstraintViolatedError:
            tests.append(('insert 3rd BigUnique', True))
            
        i = 0
        for thing in stuff:
            try:
                thing.delete()
                tests.append(('Deleting item %d'%i, True))
            except:
                tests.append(('Deleting item %d'%i, False))
            i+=1    
            
        
        self.response.out.write('<html><head><title>Tests</title></head><body><table border="1"><tr><td>Test</td><td>Passed</td></tr>')
        for t in tests:
            self.response.out.write('<tr><td>%s</td><td>%s</td></tr>' % t)
        self.response.out.write('</table><br>Total time: %s' % str(datetime.datetime.now()-start))
        self.response.out.write('</body></html>')
        
        
from google.appengine.ext import db
import burns

class UniqueMe(burns.UniqueModel):
    unique_property = db.StringProperty(required=True)
    some_other_property = db.StringProperty(required=True)
    
    _uniques = set([
                    (unique_property,)
                    ])
    
class UniqueMe1(burns.UniqueModel):
    unique_property = db.StringProperty(required=True)
    some_other_property = db.StringProperty(required=True)
    
    _uniques = set([
                    (unique_property,)
                    ])
    
class BigUnique(burns.UniqueModel):
    prop1 = db.StringProperty(required=True)
    prop2 = db.StringProperty(required=True)
    prop3 = db.StringProperty(required=True)
    prop4 = db.StringProperty(required=True)
    prop5 = db.StringProperty(required=True)
    
    _uniques = set([
                    (prop1,),
                    (prop2,prop3)
                    ])
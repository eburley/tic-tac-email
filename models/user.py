from google.appengine.ext import ndb

class User(ndb.Model):
    games = ndb.KeyProperty(repeated = True)
    user_id = ndb.StringProperty()


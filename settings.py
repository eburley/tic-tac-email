import os

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'])

JINJA_ENVIRONMENT.globals['url_for'] = webapp2.uri_for

class SendgridAccount:
    username = 'foo'
    password = 'password'
    from_domain = 'example.com'
    sender_email = 'tictactoe@example.com'

# load settings_local if it exists...
try:
    import settings_local
except Exception, e:
    pass

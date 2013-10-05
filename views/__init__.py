from google.appengine.api import users
import webapp2

from settings import JINJA_ENVIRONMENT

class MainHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        user = users.get_current_user()
        context = {'user': user}
        self.response.write(template.render(context))

class LoginHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            destination = self.request.get('dest')
            self.redirect(destination or self.uri_for('main'))

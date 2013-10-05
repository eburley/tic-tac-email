from google.appengine.api import users
import webapp2

from settings import JINJA_ENVIRONMENT

class NewGameHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(self.uri_for('login', dest=self.uri_for('newGame')))
        else:
            template = JINJA_ENVIRONMENT.get_template('newGame.html')
            context = {'user': user}
            self.response.write(template.render(context))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(self.uri_for('login', dest=self.uri_for('newGame')))
        else:
            invitee_email = self.request.get('invitee')
            invitee_user = users.User(invitee_email)

            # todo: construct the game, 
            # send the invite
            # unit test

            template = JINJA_ENVIRONMENT.get_template('inviteSent.html')
            context = {'user':user,
                       'invitee': invitee_email }
            self.response.write(template.render(context))

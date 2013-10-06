from google.appengine.api import users
import webapp2

from settings import JINJA_ENVIRONMENT
from models import game
from commands.mail import send_game_invite

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
        current_user = users.get_current_user()
        if not current_user:
            self.redirect(self.uri_for('login', dest=self.uri_for('newGame')))
        else:
            invitee_email = self.request.get('invitee')
            invitee_user = users.User(invitee_email)

            # construct the game
            new_game = game.Game(player_X=invitee_user, player_O=current_user)
            new_game.put()
            # send the invite
            send_game_invite(new_game)

            template = JINJA_ENVIRONMENT.get_template('inviteSent.html')
            context = {'user':current_user,
                       'invitee': invitee_email }
            self.response.write(template.render(context))


import unittest
from mock import patch

import webapp2
import webtest

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import testbed

from views.games import NewGameHandler
from views.games import users
from models import game

class TestNewGame(unittest.TestCase):
    """
    Test that NewGame responds correctly
    """
    def setUp(self):
        # todo: should we use the routing from main instead?
        app = webapp2.WSGIApplication([
            webapp2.Route('/login', handler='views.LoginHandler', name='login'),
            webapp2.Route('/games/newGame', handler=NewGameHandler, name='newGame'),])        
        self.testapp = webtest.TestApp(app)

        # use the stubs
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_all_stubs()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_requires_signin(self):
        """
        NewGame should require you to be a user
        """
        with patch.object(users,'get_current_user') as patched_users:            
            patched_users.return_value = None
            response = self.testapp.get('/games/newGame')
            self.assertEqual(response.status_int, 302, 
                msg='we should require signin')

    def test_get_renders_a_form(self):
        """
        NewGame should return a form for creating a game
        with a user if you're signed in
        """
        with patch.object(users,'get_current_user') as patched_users:            
            patched_users.return_value = {'Name':'bob'}
            response = self.testapp.get('/games/newGame')
            self.assertIsNotNone(response.form)

    @patch('views.games.send_game_invite')
    @patch.object(users, 'get_current_user')
    def test_post_creates_a_game(self, patched_users, send_game_invite):
        """
        Posting to the new game endpoint should
        create a game and send an invite
        """
        patched_users.return_value = users.User(email='test@example.com')
        invitee_email = 'john@example.com'
        self.testapp.post('/games/newGame',
            { 'invitee': invitee_email})
        # there should be a game
        self.assertEqual(1, len(game.Game.query().fetch(2)))
        # the invited user should be player X
        new_game = game.Game.query().fetch(1)[0]
        self.assertEqual(new_game.player_X.email(), invitee_email)
        # the inviting user should be player O
        self.assertEqual(new_game.player_O, patched_users.return_value)
        self.assertTrue(send_game_invite.called)




        








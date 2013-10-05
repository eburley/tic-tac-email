import unittest
from mock import patch

import webapp2
import webtest

from views.games import NewGameHandler
from views.games import users

class TestNewGame(unittest.TestCase):
    """
    Test that NewGame responds correctly
    """
    def setUp(self):
        app = webapp2.WSGIApplication([
            webapp2.Route('/login', handler='views.LoginHandler', name='login'),
            webapp2.Route('/games/newGame', handler=NewGameHandler, name='newGame'),])        
        self.testapp = webtest.TestApp(app)

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
        








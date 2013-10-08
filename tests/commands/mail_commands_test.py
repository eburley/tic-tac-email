import unittest
from mock import patch

from google.appengine.api import users

from settings import SendgridAccount
from models import game
from commands.mail import send_game_invite
from commands.mail import GAME_KEY_HEADER
from commands.mail import _send_to

class TestMailCommands(unittest.TestCase):
    
    @patch('sendgrid.Message')
    @patch('sendgrid.Sendgrid')
    def test_send_to(self, Sendgrid, Message):
        """
        _send_to should use settings and
        call Sendgrid appropriately.  _send_to
        is the workhorse of the mail commands.
        """
        sendgrid_instance = Sendgrid.return_value
        message_instance = Message.return_value

        recipient = 'dest@eburley.com'
        recipient_name = 'lucky_stiff'
        subject = 'hellow from tictacemail'
        plaintext = 'the quick brown'
        html = '<h1>the quick brown fox</h1>'

        _send_to(recipient, recipient_name, subject, plaintext, html)

        # make sure we're using settings.
        Sendgrid.assert_called_once_with(SendgridAccount.username,
            SendgridAccount.password, secure=True)
        
        # make sure message is constructed and configured as expected.
        Message.assert_called_once_with(SendgridAccount.sender_email,
                                        subject, 
                                        plaintext, 
                                        html)

        message_instance.add_to.assert_called_once_with(recipient, recipient_name)

        # make sure it sends.
        sendgrid_instance.web.send.assert_called_once_with(message_instance)
    
    @patch('sendgrid.Message')
    @patch('sendgrid.Sendgrid')    
    def test_send_to_supports_headers(self, Sendgrid, Message):
        """
        _send_to should allow callers to supply additional headers via kwarg
        so that they can set email context
        """
        k,v = ('x-game-key',123)
        headers = {k:v}
        _send_to('foo@example.com', 'foo', 'test', 'plain', 'html', headers=headers)
        Message.return_value.add_header.assert_called_once_with(k,v)


    @patch('commands.mail._send_to')    
    @patch('commands.mail.JINJA_ENVIRONMENT')
    def test_send_game_invite(self, JINJA_ENVIRONMENT, mockSendTo):
        """
        send_game_invite should send an invite to player_X
        on behalf of player_O.  send_game_invite should
        use the templating system.
        """
        invitee = users.User('recip@example.com')
        invitor = users.User('sender@example.com')
        new_game = game.Game(player_X = invitee, player_O = invitor, id='3')
        send_game_invite(new_game)
        
        self.assertTrue(mockSendTo.called)
        mock_args = mockSendTo.call_args[0]
        self.assertEqual(mock_args[0], invitee.email())
        self.assertEqual(mock_args[1], invitee.nickname())
        # should have supplied a game header
        mock_kwargs = mockSendTo.call_args[1]

        self.assertTrue('headers' in mock_kwargs.keys())
        self.assertTrue(GAME_KEY_HEADER in mock_kwargs.get('headers').keys())
        # subject should contain invitors email.
        self.assertTrue(invitor.email() in mock_args[2])
        # should have called JINJA 
        self.assertTrue(JINJA_ENVIRONMENT.get_template.called)
        # should have given the template some game context
        renderer = JINJA_ENVIRONMENT.get_template.return_value.render
        self.assertTrue('game' in renderer.call_args[0][0], 'game should be passed')









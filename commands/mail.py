import sendgrid
from settings import JINJA_ENVIRONMENT

from settings import SendgridAccount


GAME_KEY_HEADER = 'x-game-key'

def _send_to(recipient, recipient_name, subject, plaintext, html, **kwargs):

    # make a secure connection to SendGrid
    send = sendgrid.Sendgrid(SendgridAccount.username,
        SendgridAccount.password,
        secure=True)

    # make a message object
    message = sendgrid.Message(SendgridAccount.sender_email, 
                               subject, 
                               plaintext, 
                               html)

    # add a recipient
    message.add_to(recipient, recipient_name)

    headers = kwargs.get('headers', None)
    if headers:
        for k,v in headers.iteritems():
            message.add_header(k,v)

    # send it!
    send.web.send(message)


def send_game_invite(game, context=None):
    html_template = JINJA_ENVIRONMENT.get_template('mail/gameInvite.html')
    plain_template = JINJA_ENVIRONMENT.get_template('mail/gameInvite.txt')

    invitee = game.player_X    
    invitor = game.player_O
    context = context or {}
    context.update({'name': invitee.nickname(),
               'opponent_name': invitor.nickname(),})
    html = html_template.render(context)
    plaintext = plain_template.render(context)

    subject = 'Play Tic-Tac-Toe by email with ' + invitor.email() 
    headers = {GAME_KEY_HEADER: game.key.urlsafe()}

    _send_to(invitee.email(),
             invitee.nickname(), 
             subject, 
             plaintext, 
             html, 
             headers=headers)

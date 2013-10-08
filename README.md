tic-tac-email
=============
A sample play tic-tac-toe by email for app engine.

You'll need a SendGrid (www.sendgrid.com) account.  You can set your settings
in settings.py, but it would be better to use a settings_local.py like so:

    from settings import SendgridAccount

    SendgridAccount.username = '<your actual username>'
    SendgridAccount.password = '<your actual password>'
    SendgridAccount.from_domain = '<your from domain>'
    SendgridAccount.sender_email = '<the email sender>'

settings_local.py is already in the .gitignore

#!/usr/bin/env python
import webapp2

app = webapp2.WSGIApplication([
    webapp2.Route('/login', handler='views.LoginHandler', name='login'),
    webapp2.Route('/games/newGame', handler='views.games.NewGameHandler', name='newGame'),
    webapp2.Route('/', handler='views.MainHandler', name='main'),
], 
debug=True)


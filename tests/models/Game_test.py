import unittest
import mock

from google.appengine.ext import ndb

import models.game as game
import models.user as user


class TestGame(unittest.TestCase):
    

    def setUp(self):
        self.player_X = ndb.Key(user.User, 'playerX')
        self.player_O = ndb.Key(user.User, 'playerO')
        self.the_game = game.Game(player_X=self.player_X, player_O=self.player_O)

    def test_model(self):        
        self.assertEqual(self.the_game.player_X, self.player_X)
        self.assertEqual(self.the_game.player_O, self.player_O)
        self.assertEqual(self.the_game.board, game.BLANK_BOARD)

    def test_normal_moves(self):
        result = self.the_game.move(0, 0, game.X_SYMBOL)        
        self.assertEqual(self.the_game.board, 'X________')
        self.assertEqual(result, game.MoveResults.MOVE_VALID)

        result = self.the_game.move(1, 0, game.O_SYMBOL)
        self.assertEqual(self.the_game.board, 'X__O_____')
        self.assertEqual(result, game.MoveResults.MOVE_VALID)

    def test_invalid_starting_moves(self):
        """
        validate that an invalid starting move is rejected
        """
        result = self.the_game.move(0, 0, game.O_SYMBOL)
        # shouldn't have taken effect
        self.assertEqual(self.the_game.board, game.BLANK_BOARD)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

    def test_invalid_row_col_ranges(self):
        """
        validate that rows and colmns are as expected
        """
        result = self.the_game.move(-1, 0, game.X_SYMBOL)
        self.assertEqual(self.the_game.board, game.BLANK_BOARD)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

        result = self.the_game.move(0,-1,game.X_SYMBOL)
        self.assertEqual(self.the_game.board, game.BLANK_BOARD)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

        result = self.the_game.move(3, 0, game.X_SYMBOL)
        self.assertEqual(self.the_game.board, game.BLANK_BOARD)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

        result = self.the_game.move(0, 3, game.X_SYMBOL)
        self.assertEqual(self.the_game.board, game.BLANK_BOARD)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

    def test_invalid_symbol(self):
        """
        validate that game symbols are the only ones being used
        """
        result = self.the_game.move(1,1, game.EMPTY_SYMBOL)
        self.assertEqual(self.the_game.board, game.BLANK_BOARD)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

    def test_already_taken_spot(self):
        """
        verify that the game doesn't let you put a piece on top
        of another one.
        """
        initial_board = '____X____'
        self.the_game.board = initial_board
        result = self.the_game.move(1, 1, game.O_SYMBOL)
        self.assertEqual(self.the_game.board, initial_board)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

    def test_out_of_turn(self):
        """
        verify that a game doesn't allow a player to move
        out of turn.
        """
        initial_board = '____X____'
        self.the_game.board = initial_board
        result = self.the_game.move(1,0, game.X_SYMBOL)
        self.assertEqual(self.the_game.board, initial_board)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

        initial_board = '____XO___'
        self.the_game.board = initial_board
        result = self.the_game.move(1, 0, game.O_SYMBOL)
        self.assertEqual(self.the_game.board, initial_board)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

    def test_already_won_or_drawn(self):
        """
        verify that a game doesn't allow a play when the game is 
        already won or drawn
        """
        won_board = '_X_OXO_X_'
        self.the_game.board = won_board
        result = self.the_game.move(0, 0, game.O_SYMBOL)
        self.assertEqual(self.the_game.board, won_board)
        self.assertEqual(result, game.MoveResults.MOVE_INVALID)

    def test_game_state(self):
        self.the_game.board = game.BLANK_BOARD
        self.assertEqual(self.the_game.determine_game_state(), 
            game.GameState.GAME_NOT_STARTED)

        self.the_game.board = '____X____'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_IN_PROGRESS)

        self.the_game.board = 'OXOOXOXOX'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_DRAW)

        # check the diagonals
        self.the_game.board = 'OXOXOXOXO'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_O_WINS)
        self.the_game.board = 'OOXOXXXOO'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_X_WINS)

        # check rows
        self.the_game.board = 'XXXOXOOOX'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_X_WINS)
        self.the_game.board = 'OXOOOXXXX'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_X_WINS)
        self.the_game.board = 'OOXXXXOXO'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_X_WINS)

        # check columns
        self.the_game.board = 'OXOOXOOOX'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_O_WINS)
        self.the_game.board = 'XOOXOOOOX'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_O_WINS)
        self.the_game.board = 'OXOXXOXOO'
        self.assertEqual(self.the_game.determine_game_state(),
            game.GameState.GAME_OVER_O_WINS)






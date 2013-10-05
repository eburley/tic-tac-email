from google.appengine.ext import ndb

import user


X_SYMBOL = 'X'
O_SYMBOL = 'O'
EMPTY_SYMBOL = '_'
BLANK_BOARD = '_________'

class MoveResults:
    MOVE_INVALID='INVALID'
    MOVE_VALID='VALID'

class GameState:
    GAME_NOT_STARTED='New'
    GAME_IN_PROGRESS='In Progress'
    GAME_OVER_X_WINS='X Wins'
    GAME_OVER_O_WINS='O Wins'
    GAME_OVER_DRAW='Draw'

class Game(ndb.Model):
    player_X = ndb.KeyProperty()
    player_O = ndb.KeyProperty()
    board = ndb.StringProperty(default=BLANK_BOARD)

    def move(self, row, column, symbol):
        """
        Apply the indicated move.  
        Moves must follow normal tic-tac-toe rules.
        returns MoveResult and updates the board
        """
        game_state = self.determine_game_state()
        if game_state not in (GameState.GAME_NOT_STARTED, GameState.GAME_IN_PROGRESS):
            return MoveResults.MOVE_INVALID

        # check for initial move
        if self.board == BLANK_BOARD and symbol == O_SYMBOL:
            return MoveResults.MOVE_INVALID

        # check for invalid row and column
        if row < 0 or row > 2 or column < 0 or column > 2:
            return MoveResults.MOVE_INVALID

        # make sure the game piece is valid
        if symbol != X_SYMBOL and symbol != O_SYMBOL:
            return MoveResults.MOVE_INVALID

        # make sure the game piece isn't moving out of turn
        x_moves = self.board.count(X_SYMBOL)
        o_moves = self.board.count(O_SYMBOL)
        if symbol == X_SYMBOL and x_moves > o_moves:
            return MoveResults.MOVE_INVALID
        elif symbol == O_SYMBOL and o_moves >= x_moves:
            # note that x always goes first.
            return MoveResults.MOVE_INVALID            

        # figure out position.
        position = (3 * row) + column

        # make sure there's not already a piece there.
        if self.board[position] != EMPTY_SYMBOL:
            return MoveResults.MOVE_INVALID

        self.board = self.board[:position] + symbol + self.board[position+1:]        
        return MoveResults.MOVE_VALID

    def determine_game_state(self):
        """
        determine whether the game is under way or not.
        """
        if self.board == BLANK_BOARD:
            return GameState.GAME_NOT_STARTED

        # check for three of the same symbol across or down.
        for r in range(3):
            offset = r*3
            if self.board[offset] == self.board[offset+1] == self.board[offset+2]:
                if self.board[offset] == X_SYMBOL:
                    return GameState.GAME_OVER_X_WINS
                elif self.board[offset] == O_SYMBOL:
                    return GameState.GAME_OVER_O_WINS
            if self.board[r] == self.board[3 + r] == self.board[6 + r]:
                if self.board[r] == X_SYMBOL:
                    return GameState.GAME_OVER_X_WINS
                elif self.board[r] == O_SYMBOL:
                    return GameState.GAME_OVER_O_WINS

        # check for diagonal wins
        if ((self.board[0] == self.board[4] == self.board[8]) or
            (self.board[2] == self.board[4] == self.board[6])):
            if self.board[4] == X_SYMBOL:
                return GameState.GAME_OVER_X_WINS
            elif self.board[4] == O_SYMBOL:
                return GameState.GAME_OVER_O_WINS
        
        # check for tie.
        if not self.board.count(EMPTY_SYMBOL):
            return GameState.GAME_OVER_DRAW

        return GameState.GAME_IN_PROGRESS






        



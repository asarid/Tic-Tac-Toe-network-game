from enum import Enum
import datetime
import uuid

class StateOfGame(Enum):
    INITIALIZED = 1
    STARTED = 2
    WON = 3
    TIE = 4


class symbolsOfBoard(Enum):
    nothing = 0     # a spectator (does not have any symbol)
    O = 1           # 'O'
    X = 2           # 'X'
    DOLLAR = 3      # '$'
    HASHTAG = 4     # '#'
    SHTRUDEL = 5    # '@'
    PLUS = 6        # '+'
    PERCENT = 7     # '%'
    EQUALS = 8      # '='


class Game(dict):

    def __init__(self, num_of_players, gameState = "INITIALIZED"):
        """Constructor for Game class

        Args:
            num_of_players (int): number of players in the game
        """
        self.game_ID = str(uuid.uuid4())
        self.num_of_players = num_of_players
        self.game_state = gameState
        self.board = [ [' ' for i in range(self.num_of_players+1)] for j in range(self.num_of_players+1) ] # initiaze the (x+1)^2 board with zeros, where 'x' is the number of players
        self.winner_ID = ""
        self.duration = 0 # datetime.timedelta()
        self.creation_date = datetime.datetime.now()
        
        dict.__init__(self, game_ID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())
    
    def set_game_ID(self, game_ID: str):
        self.game_ID = game_ID
        dict.__init__(self, game_ID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())

    def set_game_state(self, game_state: str):
        self.game_state = game_state
        dict.__init__(self, game_ID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())

    def set_square_on_board(self, square: tuple):
        """set a certain square on board

        Args:
            square (tuple): consists of (row, column, symbol to put on board)
        """
        self.board[square[0]][square[1]] = square[2]
        dict.__init__(self, game_ID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())

    def set_num_of_players(self, num_of_players: int):
        self.num_of_players = num_of_players
        dict.__init__(self, game_ID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())

    def set_winner_ID(self, winner_ID: str):
            self.winner_ID = winner_ID
            dict.__init__(self, game_ID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())

    def set_duration(self):
        self.duration = (datetime.datetime.now() - self.creation_date).total_seconds()
        dict.__init__(self, game_ID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())

    def set_creation_date(self, creation_date: datetime):
        self.creation_date = creation_date
        dict.__init__(self, game_ID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())


# class Board:
#     def __init__(self, num_of_players : int) -> None:
#         # initiaze the (x+1)^2 board with zeros, where 'x' is the number of players
#         self._board = [ [0 for i in (self.num_of_players+1)] for j in (self.num_of_players+1) ] # initiaze the (x+1)^2 board with zeros, where 'x' is the number of players


class User:
    
    def __init__(self, token : int, nikName : str):
        self.token = token
        self.nikName = nikName
        self.creation_date = datetime.datetime.now()
        
        # self.gamesParticipated = 0
        # self.gamesWon = 0
        # self.avgTimeForMove = 0
        self.userStat = UserStat()


class UserStat:
    def __init__(self):
        self.numOfGamesParticipated = 0
        self.gamesWon = 0
        self.gamesInTie = 0
        self.avgTimeForMove = 0
    
    def updateStat(self, wonOrDrawOrLose: int = 0, avg_time_for_move: int = 0):
        """update the statistics of a user, before updating the DB

        Args:
            wonOrDrawOrLose (int, optional): 0 - the user losed the game, 1 - the user won the last game, 2 - the user had a draw in the last game. Defauls to 0.
            avg_time_for_move (int, optional): average time for moves in the last game. Defaults to 0.
        """
        if (wonOrDrawOrLose == 1):
            self.gamesWon = self.gamesWon + 1
        elif (wonOrDrawOrLose == 2):
            self.gamesInTie = self.gamesInTie + 1
        self.avgTimeForMove = (self.numOfGamesParticipated * self.avgTimeForMove + avg_time_for_move)/(self.numOfGamesParticipated + 1)
        self.numOfGamesParticipated = self.numOfGamesParticipated + 1
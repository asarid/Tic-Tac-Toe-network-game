from enum import Enum
import datetime
import uuid

class StateOfGame(Enum):
    INITIALIZED = 1
    OCCURRING = 2
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

    def __init__(self, num_of_players, gameState = StateOfGame.INITIALIZED.name):
        """Constructor for Game class

        Args:
            num_of_players (int): number of players in the game
        """
        self.game_ID = str(uuid.uuid4())
        self.num_of_players = num_of_players
        self.game_state = gameState
        self.board = [ [0 for i in range(self.num_of_players+1)] for j in range(self.num_of_players+1) ] # initiaze the (x+1)^2 board with zeros, where 'x' is the number of players
        self.winner_ID = ""
        self.duration = 0 # datetime.timedelta()
        self.creation_date = datetime.datetime.now()
        
        dict.__init__(self, gameID = self.game_ID, num_of_players = self.num_of_players, game_state = self.game_state, board = self.board, winner_ID = self.winner_ID, duration = self.duration, creation_date = self.creation_date.isoformat())
    


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
        

    
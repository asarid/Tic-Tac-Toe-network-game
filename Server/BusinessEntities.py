from enum import Enum
import datetime
import uuid

class StateOfGame(Enum):
    INITIALIZED = 1
    OCCURRING = 2
    WON = 3
    TIE = 4


class SignsOfBoard(Enum):
    O = 1
    X = 2
    DOLLAR = 3
    HASHTAG = 4
    SHTRUDEL = 5
    PLUS = 6
    EQUALS = 7
    PERCENT = 8


class Game:

    def __init__(self, num_of_players):
        """Constructor for Game class

        Args:
            num_of_players (int): number of players in the game
        """
        self.game_ID = str(uuid.uuid4())
        self.num_of_players = num_of_players
        self.game_state = StateOfGame.INITIALIZED.name
        self.board = [ [0 for i in range(self.num_of_players+1)] for j in range(self.num_of_players+1) ] # initiaze the (x+1)^2 board with zeros, where 'x' is the number of players
        self.winner_ID = ""
        self.duration = 0 # datetime.timedelta()
        self.creation_date = datetime.datetime.now()
    


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
        

    
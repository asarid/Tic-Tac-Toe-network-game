import DataAccess.DataAccess as DA
import BusinessEntities as BE
import socket


factory = DA.AccessFactory()
factory.register_DB_access('JSON', DA.JSON_db_access)
# factory.register_format('SQL', SQL_db_access)



db_access = DA.JSON_db_access()

registeredUsers = {}            # each entry is a {user_socket_address : user_token}
activeGames = {}                # each entry is a {gameID : (BE.Game, [active Participants : Participants], [passive participants, only addrs of spectators : tuple (of addr)])}

class Participant:
    """represents a participant in a game as an active player or a spectator
    """
    def __init__(self, addr: tuple, symbol: int, turn: int = -1):
        """initialize the details of a participant in a game

        Args:
            addr (tuple): an address of the participant (IP address, Port number)
            symbol (BE.symbolsOfBoard): which symbol should represent the player in the game (1-8 as a player, 0 as a spectator)
            turn (int): which turn the participant has (1-8, 0 for a spectator, -1 before the beginning)
        """
        self.addr = addr
        self.symbol = symbol
        self.turn = turn


# entry page functions

def signUpUser(nikName: str, addr: tuple):
    """sign up a new user by registering him

    Args:
        nikName (str): the nikName he chose
        addr (tuple): the socket pair (IP address, Port number)

    Returns:
        var: his new and unique token if succedds, else -1
    """
    user = db_access.create_new_user(nikName)
    
    if (isinstance(user, BE.User)):
        #registeredUsers[addr] = (user)
        registeredUsers[addr] = user
        return user.token
    else:
        return -1


def signInUser(token: str, addr: tuple):    
    """sign in user using its unique token

    Args:
        token (str): unique ID of the user
        addr (tuple): tuple of (IP address, port number)

    Returns:
        var : nik name in case the login was successful, else: -1
    """
    user = db_access.fetch_user_by_ID(token)
    if (isinstance(user, BE.User)):
        registeredUsers[addr] = (user)
        return user.nikName
    else:
        return -1

def unregisterUser(addr: tuple):
    """pop the user who exit the game from the dynamoc memory of users

    Args:
        addr (tuple): tuple of (IP address, port number)
    """
    if addr in registeredUsers:
        registeredUsers.pop(addr)



# main page functions

def registerNewGame(num_of_participants: int, addr: tuple):
    game = db_access.create_new_game(num_of_participants)
    if (isinstance(game, BE.Game)):
        newParticipant = Participant(addr, 1, BE.symbolsOfBoard.O.value)
        activeGames[game.game_ID] = (game, [newParticipant],[]) # the key is the address of the first player, we save the game record and a list of sockets of players
        return game
    else:
        return -1

def fetchAllActiveGames():
    return activeGames


def joinExistingGame(game_ID: str, token: str):
    pass

def viewStatistics():
    pass


# game management functions

def moveOnBoard(game_ID: str, token: str, whichSquare: int):
    pass

def checkStateOfGame(game_ID: str):
    pass

def timeout(token: str):
    pass

def someoneExitedAbruptly(sock : socket):
    pass

def gameHasFinished(game_ID: str):
    pass
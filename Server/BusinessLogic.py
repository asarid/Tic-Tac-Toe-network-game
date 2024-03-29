import DataAccess.DataAccess as DA
import BusinessEntities as BE
import socket


factory = DA.AccessFactory()
factory.register_DB_access('JSON', DA.JSON_db_access)
# factory.register_format('SQL', SQL_db_access)



db_access = DA.JSON_db_access()
registeredUsers = {}
activeGames = {}


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

def registerNewGame(addr: tuple, num_of_participants: int):
    game = db_access.create_new_game(num_of_participants)
    if (isinstance(game, BE.Game)):
        activeGames[game.game_ID] = (game, [addr]) # the key is the address of the first player, we save the game record and a list of sockets of players
        return game
    else:
        return -1

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






# class BusinessLogic:
#     def __init__(self):
#         self.db_access = DA.JSON_db_access()
#         self.registeredUsers = {}
#         self.activeGames = {}


#     # entry page functions
        
#     def signUpUser(self, nikName: str) -> str:
#         pass

#     def signInUser(self, token: str) -> BE.User:
#         pass

#     def signOutUser(self, token: str):
#         pass


#     # main page functions

#     def startNewGame(self, token: str):
#         pass

#     def joinExistingGame(self, game_ID: str, token: str):
#         pass

#     def viewStatistics(self):
#         pass

    
#     # game management functions
    
#     def moveOnBoard(self, game_ID: str, token: str, whichSquare: int):
#         pass

#     def checkStateOfGame(self, game_ID: str):
#         pass

#     def timeout(self, token: str):
#         pass

#     def someoneExitedAbruptly(self, sock : socket):
#         pass

#     def gameHasFinished(self, game_ID: str):
#         pass
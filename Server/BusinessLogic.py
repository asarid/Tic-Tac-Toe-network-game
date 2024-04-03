import DataAccess.DataAccess as DA
import BusinessEntities as BE
import socket
import random
import threading

factory = DA.AccessFactory()
factory.register_DB_access('JSON', DA.JSON_db_access)
# factory.register_format('SQL', SQL_db_access)



db_access = DA.JSON_db_access()

registeredUsers = {}            # each entry is a { user_address 'addr' : [BE.User, socket, game_ID - if any] }
activeGames = {}                # each entry is a {gameID : (BE.Game, [active Participants : Participants], [passive participants, only addrs of spectators : tuple (of addr)])}

selector = None

class Participant:
    """represents a participant in a game as an active player or a spectator
    """
    def __init__(self, addr: tuple, nikName: str, symbol: int, turn: int = -1):
        """initialize the details of a participant in a game

        Args:
            addr (tuple): an address of the participant (IP address, Port number)
            symbol (BE.symbolsOfBoard): which symbol should represent the player in the game (1-8 as a player, 0 as a spectator)
            turn (int): which turn the participant has (1-8, 0 for a spectator, -1 before the beginning)
        """
        self.addr = addr
        self.nik_name = nikName
        self.symbol = symbol
        self.turn = turn


# entry page functions

def signUpUser(nikName: str, addr: tuple, sock: socket):
    """sign up a new user by registering him

    Args:
        nikName (str): the nikName he chose
        addr (tuple): the socket pair (IP address, Port number)
        sock (socket): socket he is connected with, written in order to identify the 
                        right registered object in the selector.
    Returns:
        var: his new and unique token if succedds, else -1
    """
    user = db_access.create_new_user(nikName)
    
    if (isinstance(user, BE.User)):
        registeredUsers[addr] = [user, sock]
        return user.token
    else:
        return -1


def signInUser(token: str, addr: tuple, sock: socket):    
    """sign in user using its unique token

    Args:
        token (str): unique ID of the user
        addr (tuple): tuple of (IP address, port number)
        sock (socket): socket he is connected with, written in order to identify the 
                        right registered object in the selector.
        
    Returns:
        var : nik name in case the login was successful, else: -1
    """
    user = db_access.fetch_user_by_ID(token)
    if (isinstance(user, BE.User)):
        registeredUsers[addr] = [user, sock]
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
    """add a new game to the dict of active games and update the registered user with the game ID he started

    Args:
        num_of_participants (int): number of supposed participants in the game
        addr (tuple): address (IP, PORT) of the player who sought to start a game

    Returns:
        var: BE.Game new game if the operation succeeded, else -1. 
    """
    game = db_access.create_new_game(num_of_participants)
    if (isinstance(game, BE.Game)):
        newParticipant = Participant(addr, registeredUsers[addr][0].nikName, BE.symbolsOfBoard.O.value)
        activeGames[game.game_ID] = (game, [newParticipant],[]) # the key is the address of the first player, we save the game record and a list of sockets of players
        registeredUsers[addr].append(game.game_ID)              # add the game_ID to the new game the user just now started.
        return game
    else:
        return -1

def fetchAllActiveGames():
    """return all the active games using the dict 'activeGames'

    Returns:
        Dict: dict of active games
    """
    return activeGames


def joinToExistingGame(game_ID: str, type_of_joined_user: str, addr: tuple):
    if type_of_joined_user == "spectator":
        activeGames[game_ID][2].append(addr) # add the spectator user address to the list of spectators
    else:
        newParticipant = Participant(addr, registeredUsers[addr][0].nikName, activeGames[game_ID][1][-1].symbol + 1)
        activeGames[game_ID][1].append(newParticipant) # add the active player user address to the list of players
        
        # compare the number of connected players to the amount that the game should has
        num_of_players = activeGames[game_ID][0].num_of_players
        num_of_active_players = len(activeGames[game_ID][1])

        # the game should not be started yet
        if (num_of_players > num_of_active_players): 
            notifyParticipants(game_ID, "5_newPlayer", num_of_players-num_of_active_players)
        # the game should start, so determine order of playing and call the function in charge of starting the game
        elif (num_of_players == num_of_active_players):
            active_players = activeGames[game_ID][1]
            random.shuffle(active_players)
            for index, player in enumerate(active_players):
                player.turn = index + 1
            startTheGame(game_ID)


def viewStatistics():
    pass

def notifyOneParticipant(addr: tuple, response: str, value):
    """notify one participant of a certain game with a message sent as an argument.
        We do so by making a response messaege, the thread of the socket will take it from there.
    Args:
        addr (str): address of the participant to be notified
        response (str): a headline to the message to the user
        value (var): the content of the message (could be a number, a text, etc.)
    """
    message = {
        "response": response,
        "value": value
    }
    
    player_sock = registeredUsers[addr][1]
    player_Message = selector.get_key(player_sock).data
    player_Message.response = message
    player_Message.false_request = True
    player_Message.response_created = False

def notifyParticipants(game_ID: str, response: str, value, *rest):
    """notify all the participants of a certain game with a message sent as an argument, 
        except some users that the 'rest' argument comprises. We do so by making a response message,
        the thread of the socket will take it from there.
    Args:
        game_ID (str): ID of the game that its participants should be notified
        response (str): a headline to the message to the user
        value (var): the content of the message (could be a number, a text, etc.)
        rest (tuple): a tuple of addresses of users that should not get that message
    """
    message = {
        "response": response,
        "value": value
    }

    # iterate the list of active players, whose list contains Participants instances
    for player_Participant in activeGames[game_ID][1]:
        if player_Participant.addr not in rest:
            player_sock = registeredUsers[player_Participant.addr][1]
            player_Message = selector.get_key(player_sock).data
            player_Message.response = message
            player_Message.false_request = True
            player_Message.response_created = False
           
    
    # iterate the list of spectators, whose list contains only addresses, not Participants instances
    for player_Participant in activeGames[game_ID][2]:
        if player_Participant not in rest:
            player_sock = registeredUsers[player_Participant][1]
            player_Message = selector.get_key(player_sock).data
            player_Message.response = message
            player_Message.false_request = True
            player_Message.response_created = False
            
        
            # falseRequest = prepareFalseRequest(message["action"], message["value"], "text/json", "utf-8")
            # player_Message._recv_buffer += falseRequest
            # threading.Thread(target=notify_helper, args=(player_Message,)).start()

# def notify_helper(player_Message):
#     while (player_Message.between_read_to_write == True):
#         pass
#     player_Message.process_events(3)

# def prepareFalseRequest(action, value, content_type, encoding) -> bytes:

#     content_bytes = json.dumps((action, value), ensure_ascii=False).encode(encoding)
    
#     json_header = {
#             "byteorder": sys.byteorder,
#             "content-type": content_type,
#             "content-encoding": encoding,
#             "content-length": len(content_bytes)
#             }
#     jsonheader_bytes = json.dumps(json_header, ensure_ascii=False).encode(encoding)
#     message_hdr = struct.pack(">H", len(jsonheader_bytes))
    
#     return message_hdr + jsonheader_bytes + content_bytes



# game management functions

def startTheGame(game_ID: str): 
    activeGames[game_ID][0].game_state = "STARTED"
    active_players = activeGames[game_ID][1]

    for player in active_players:
        notifyOneParticipant(player.addr, "6_beforeStart", (player.turn, player.symbol))

    notifyParticipants(game_ID, "7_start", active_players[0].nik_name)

    notifyOneParticipant(active_players[0].addr, "8_yourMove", "")


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
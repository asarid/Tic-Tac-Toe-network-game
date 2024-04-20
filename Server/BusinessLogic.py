import DataAccess as DA
import BusinessEntities as BE
import socket
import random
import datetime

factory = DA.AccessFactory()
factory.register_DB_access('JSON', DA.JSON_db_access) # create an instance of a DB accessor based on JSON files
# factory.register_format('SQL', SQL_db_access)



db_access = DA.JSON_db_access() # the gateway to the DB accessor

registeredUsers = {}            # each entry is a { user_address 'addr' : [BE.User, socket, game_ID - if any] }
activeGames = {}                # each entry is a { gameID : [BE.Game, [active Participants : Participants], [passive participants, only addrs of spectators : tuple (ip, port)], numOfMovesDone: int = 0, turn = 0]}

addr_Message = None              

# dict with pairs: {symbolOfCurrentPlayer : symbolOfNextPlayer}
symbols = {
    'O': 'X',
    'X': '$',
    '$': '#',
    '#': '@',
    '@': '+',
    '+': '%',
    '%': '=',
    '=': 'O'
    }


class Participant:
    """represents a participant in a game as an active player or a spectator
    """
    def __init__(self, addr: tuple, nikName: str, symbol: str, turn: int = -1):
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
        var: his new and unique token if succeeds, else -1
    """
    user = db_access.create_new_user(nikName)
    
    if (isinstance(user, BE.User)):
        registeredUsers[addr] = [user, sock] # store the new user in a dict
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
        for key, _user in registeredUsers.items(): # check if this user is already connected to the server
            if _user[0].token == token:
                return -2
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
    game = BE.Game(num_of_participants)
    
    newParticipant = Participant(addr, registeredUsers[addr][0].nikName, 'O')
    activeGames[game.game_ID] = [game, [newParticipant],[], 0, 0] # the key is the address of the first player, we save the game record, a list
                                                                    # of sockets of players and spectators and how many moves were done so far.
    registeredUsers[addr].append(game.game_ID)      # add the game_ID of the new game the user just now started.
    return game

def fetchAllActiveGames():
    """return all the active games using the dict 'activeGames'

    Returns:
        Dict: dict of active games
    """
    return activeGames


def joinToExistingGame(game_ID: str, type_of_joined_user: str, addr: tuple):
    """handle a case in which a user wants to join to a game (either as a player or a spectator)

    Args:
        game_ID (str): ID of the game the user wnats to join to
        type_of_joined_user (str): "player" or "spectator"
        addr (tuple): (ip, port)
    """
    if type_of_joined_user == "spectator":
        activeGames[game_ID][2].append(addr) # add the spectator user address to the list of spectators
        registeredUsers[addr].append(game_ID) # add game_ID for purposes of remiving this user from the list of spectators to be notified about moves in the game
        
        # send a response with value of the remaining number of players to start the game (0 or more)
        notifyOneParticipant(addr, "14_newSpectator", activeGames[game_ID][0].num_of_players-len(activeGames[game_ID][1]))

    else:
        newParticipant = Participant(addr, registeredUsers[addr][0].nikName, symbols[activeGames[game_ID][1][-1].symbol])
        print("symbol of second:", newParticipant.symbol)
        activeGames[game_ID][1].append(newParticipant) # add the active player user address to the list of players
        registeredUsers[addr].append(game_ID) # add game_ID for purposes of remiving this user from the list of spectators to be notified about moves in the game

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


def fetchGamesHistory():
    """fetch history of games from the DB

    Returns:
        list: a list of Games
    """
    # fetch history of games from the database (the fetched games are sorted by creation date)
    games = db_access.fetch_all_games()

    return games

def fetchUsersStats():
    """fetch statistics of users

    Returns:
        list: list of user statistics
    """
    usersStats = db_access.fetch_users_stats()
    return usersStats


def notifyOneParticipant(addr: tuple, response: str, value):
    """notify one participant of a certain game with a message sent as an argument.
        We do so by making a response messaege, the thread of the socket will take it from there.
    Args:
        addr (str): address of the participant to be notified
        response (str): a headline to the message to the user
        value (var): the content of the message (could be a number, a text, etc.)
    """
    message = ({
        "response": response,
        "value": value
    }, False)
    
    player_Message = addr_Message[addr]
    player_Message.responses.append(message)
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
    message = ({
        "response": response,
        "value": value
    }, False)

    # iterate the list of active players, whose list contains Participants instances
    for player_Participant in activeGames[game_ID][1]:
        if player_Participant.addr not in rest:
            player_Message = addr_Message[player_Participant.addr]
            player_Message.responses.append(message)
            player_Message.response_created = False
           
    
    # iterate the list of spectators, whose list contains only addresses, not Participants instances
    for player_Participant in activeGames[game_ID][2]:
        if player_Participant not in rest:
            player_Message = addr_Message[player_Participant]
            player_Message.responses.append(message)
            player_Message.response_created = False
            



# game management functions

def startTheGame(game_ID: str):
    activeGames[game_ID][0].set_game_state("STARTED")
    activeGames[game_ID][0].set_creation_date(datetime.datetime.now())
    print("game that started: ", activeGames[game_ID][0])
    
    active_players = activeGames[game_ID][1]

    for player in active_players:
        notifyOneParticipant(player.addr, "6_beforeStart", (player.turn, player.symbol))

    notifyParticipants(game_ID, "7_start", active_players[0].nik_name)

    notifyOneParticipant(active_players[0].addr, "8_yourMove", "")


def moveOnBoard(game_ID: str, squareChanged: tuple, addr: tuple):
    gameInQuestion = activeGames[game_ID][0]
    gameInQuestion.set_square_on_board(squareChanged)
    activeGames[game_ID][3] = activeGames[game_ID][3] + 1  # increase number of moves

    lastPlayer = activeGames[game_ID][1][activeGames[game_ID][4]]
    activeGames[game_ID][4] = (activeGames[game_ID][4] + 1) % len(activeGames[game_ID][1])  # increase 'turn' counter
    nextPlayer = activeGames[game_ID][1][activeGames[game_ID][4]]

    result = checkStateOfGame(gameInQuestion.board, squareChanged, activeGames[game_ID][3])

    if (result == 0): # the game is not finished
        notifyParticipants(game_ID, "9_afterOneMove", (squareChanged, nextPlayer.nik_name), nextPlayer.addr)
        notifyOneParticipant(nextPlayer.addr, "10_YourMoveArrived", squareChanged)
    
    else: # game has finished, either by victory or by draw
        gameHasFinished(game_ID, result, squareChanged, lastPlayer)


def checkStateOfGame(board: list, squareChanged: tuple, numOfMoves: int) -> int:
    """check if after the move that was done the state of the game has changed

    Args:
        board (list): the board of game
        squareChanged (tuple): (row changed, column changed, which symbol)
        numOfMoves (int): number of moves done so far
        
    Returns:
        int: 0 - continue, the game didn't finished
             1 - the game was won
             2 - it's a draw 
    """
    print(f"check: ({squareChanged[0]} {squareChanged[1]})")
    # if there were not enough moves so far, continue with the game
    if numOfMoves <= 2*(len(board)-1):
        return 0
    
    # then, check for a victory
    symbol = squareChanged[2]
    row = squareChanged[0]
    col = squareChanged[1]
    size = len(board)

    # check victory in the column 
    if (row > 0  and  board[row-1][col] == symbol):
        if (row > 1 and board[row-2][col] == symbol):
            return 1
        elif (row < size - 1  and  board[row+1][col] == symbol):
            return 1
    elif (row < size - 2  and  board[row+1][col] == symbol  and  board[row+2][col] == symbol):
        return 1
    
    # check victory in the row
    if (col > 0  and  board[row][col-1] == symbol):
        if (col > 1 and board[row][col-2] == symbol):
            return 1
        elif (col < size - 1  and  board[row][col+1] == symbol):
            return 1
    elif (col < size - 2  and  board[row][col+1] == symbol  and  board[row][col+2] == symbol):
        return 1
    
    # check victory in the backward slash diagonal
    if (row > 0  and  col > 0  and  board[row-1][col-1] == symbol):
        if (row > 1  and  col > 1  and  board[row-2][col-2] == symbol):
            return 1
        elif (row < size - 1  and  col < size - 1  and  board[row+1][col+1] == symbol):
            return 1
    elif (row < size - 2  and  col < size - 2  and  board[row+1][col+1] == symbol  and  board[row+2][col+2] == symbol):
        return 1
    
    # check victory in the forward slash diagonal
    if (row > 0  and  col < size - 1  and  board[row-1][col+1] == symbol):
        if (row > 1  and  col < size - 2  and  board[row-2][col+2] == symbol):
            return 1
        elif (row < size - 1  and  col > 0  and  board[row+1][col-1] == symbol):
            return 1
    elif (row < size - 2  and  col > 1  and  board[row+1][col-1] == symbol  and  board[row+2][col-2] == symbol):
        return 1
    
    # finally, check for a draw
    if (numOfMoves == size*size):
        return 2
    
    # if al other options were not true, continue the game
    return 0
    

def timeout(game_ID: str):
    lastPlayer = activeGames[game_ID][1][activeGames[game_ID][4]]
    activeGames[game_ID][4] = (activeGames[game_ID][4] + 1) % len(activeGames[game_ID][1])  # increase 'turn' counter
    nextPlayer = activeGames[game_ID][1][activeGames[game_ID][4]]

    notifyParticipants(game_ID, "15_timeout", (lastPlayer.nik_name, nextPlayer.nik_name), nextPlayer.addr)
    notifyOneParticipant(nextPlayer.addr, "10_YourMoveArrived", (-1,-1, ''))


def someoneExitedAbruptly(addr : tuple):
    # if the user is still registered 
    if addr in registeredUsers:
        # the user is associated with an occurring game
        if len(registeredUsers[addr]) == 3:
            isPlayer = True
            for participant_addr in activeGames[registeredUsers[addr][2]][2]:
                if participant_addr == addr: # the user is a spectator
                    exitTheGame(registeredUsers[addr][2], "no", addr)
                    isPlayer = False
                    break
            if isPlayer == True: # the user is a player, should notify the other players
                exitTheGame(registeredUsers[addr][2], "O", addr)
        else:
            unregisterUser(addr)
                  
                            



def gameHasFinished(game_ID: str, result: int, squareChanged: tuple, lastPlayer: Participant):
    
    game = activeGames[game_ID][0]
    game.set_duration()

    users_list = []

    if (result == 1): # the game has won
        notifyParticipants(game_ID, "11_victory", (squareChanged, lastPlayer.nik_name), lastPlayer.addr)
        notifyOneParticipant(lastPlayer.addr, "12_youWon", "")

        game.set_game_state("WON")
        game.set_winner_name(registeredUsers[lastPlayer.addr][0].nikName)

        for player in activeGames[game_ID][1]:
            user = registeredUsers[player.addr][0]
            users_list.append(user)
            if player.addr != lastPlayer.addr:
                user.userStat.updateStat()
            else:
                user.userStat.updateStat(1)

    elif (result == 2): # it's a draw
        notifyParticipants(game_ID, "13_draw", squareChanged)
        game.set_game_state("TIE")

        for player in activeGames[game_ID][1]:
            user = registeredUsers[player.addr][0]
            users_list.append(user)
            user.userStat.updateStat(2)

    db_access.update_users(users_list)
    db_access.update_game(game)

    for player in activeGames[game_ID][1]:
        registeredUsers[player.addr].pop()  # remove game_ID, this user is not associated anymore to a game
    for spectator_addr in activeGames[game_ID][2]:
        registeredUsers[spectator_addr].pop()  # remove game_ID, this user is not associated anymore to a game
    
    activeGames.pop(game_ID, None)

def quitInMiddle(game_ID: str, is_spectator: bool, addr: tuple):
    # the user is a spectator, there no need to act except removing him from the list of sepctators
    if is_spectator == True:
        activeGames[game_ID][2].remove(addr)

    # the user is a player, we need to send a message to the other players and remove certain entries from the lists
    elif game_ID in activeGames:
        notifyParticipants(game_ID, "18_someoneQuitted", "", addr)
        for player in activeGames[game_ID][1]:
            registeredUsers[player.addr].pop()  # remove game_ID, this user is not associated anymore to a game
        for spectator_addr in activeGames[game_ID][2]:
            registeredUsers[spectator_addr].pop()  # remove game_ID, this user is not associated anymore to a game
        activeGames.pop(game_ID, None)

def exitTheGame(game_ID: str, is_spectator: bool, addr: tuple):
    
    # the user is a spectator, there no need to act except removing him from the list of sepctators
    if is_spectator == True:
        activeGames[game_ID][2].remove(addr)
        unregisterUser(addr)

    # the user is a player, we need to notify the other players and remove certain entries from the lists
    elif game_ID in activeGames:
        notifyParticipants(game_ID, "18_someoneQuitted", "", addr)
        for player in activeGames[game_ID][1]:
            registeredUsers[player.addr].pop()  # remove game_ID, this user is not associated anymore to a game
        for spectator_addr in activeGames[game_ID][2]:
            registeredUsers[spectator_addr].pop()  # remove game_ID, this user is not associated anymore to a game
        activeGames.pop(game_ID, None)
        unregisterUser(addr)
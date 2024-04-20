import abc
import json
import random
import os
import datetime

# conf_path = os.getcwd()
# sys.path.append(conf_path[:conf_path.rfind("\\")])
# databases_path = sys.path.append(conf_path[:conf_path.rfind("\\")+1]+"Databases")


import BusinessEntities as BE



class DataAccessInterface(metaclass=abc.ABCMeta):
    """an interfance whom any DB manager should implement

    Raises:
        NotImplementedError: an exception raised if one of the methods of this interface is not implemented
    """

    # =======================================
    # =========  CRUD operations  ===========
    # =======================================


    # ==============================
    # =========  CREATE  ===========

    @abc.abstractmethod
    def create_new_game(self, numOfPlayers : int) -> BE.Game:
        raise NotImplementedError

    @abc.abstractmethod
    def create_new_user(self) -> str:
        raise NotImplementedError
    

    # ============================
    # =========  READ  ===========

    @abc.abstractmethod
    def fetch_game_by_ID(self, id: str) -> BE.Game:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_all_games(self, id: str) -> dict:
        raise NotImplementedError
    
    @abc.abstractmethod
    def fetch_user_by_ID(self, id: int) -> BE.User:
        raise NotImplementedError


    # ==============================
    # =========  UPDATE  ===========

    @abc.abstractmethod
    def update_game(self, game : BE.Game):
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_user(self, user : BE.User):
        raise NotImplementedError
    

    # ==============================
    # =========  DELETE  ===========

    @abc.abstractmethod
    def delete_game_by_ID(self, id: str):
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_user_by_ID(self, id: str):
        raise NotImplementedError




class AccessFactory:
    """using this factory a new type of access to the database can be created without
        any change except adding the new class of access
    """
    def __init__(self):
        self._creators = {} # a dict of types of access to the database

    def register_DB_access(self, format, creator):
        self._creators[format] = creator

    def get_access_by_DB_type(self, format):
        """get access to the database according to the type of database

        Args:
            format: format of database

        Raises:
            ValueError: if the type of database is not found

        Returns:
            var: an instance of the access to the DB
        """
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()





class JSON_db_access(DataAccessInterface):
    """access to a JSON database
    """
    def __init__(self):
        """initialize paths of files

        Raises:
            Exception: if some file supposed to be in the database is not found
        """
        self.users_full = "./Databases/JSON/users_full.json"
        self.users_tokens = "./Databases/JSON/users_tokens.json"
        self.games = "./Databases/JSON/games.json"

        files = [self.users_full,self.users_tokens,self.games]
        
        # Check if file exists
        for filePath in files:
            if os.path.exists(filePath) is False:
                raise Exception("File not found")    
        
        # self.lastDateGamesFetched = datetime.datetime.now() 


    # ==============================
    # =========  CREATE  ===========

    def create_new_game(self, numOfPlayers: int):
        """create an entry of new game in the DB

        Args:
            numOfPlayers (int): number of players (not including spectators)

        Returns:
            Game: the new game
        """
        newGame = BE.Game(num_of_players = numOfPlayers)
        dictGames = {}

        if (os.path.getsize(self.games) != 0):
            with open(self.games) as gamesFile:
                dictGames = json.load(gamesFile)
        dictGames[newGame.game_ID] = newGame    # load this new game into the dict of games

        with open(self.games, 'w') as gamesFile: # write the new dict of games (now includes the new game) into the DB
            json.dump(dictGames, gamesFile, indent=4, separators=(',',': '), cls=GameEncoderJSON)

        return newGame


    def create_new_user(self, nik_name : str) -> BE.User:
        """create an entry of new user in the DB

        Args:
            nik_name (str): a nik name the user chose for himself

        Returns:
            BE.User: the instance of the new user
        """
        dictUserTokens = {}
        newToken = random.randint(1,9999) # chooose a random token for the user

        if (os.path.getsize(self.users_tokens) != 0):
            with open(self.users_tokens) as usersTokensFile:
                dictUserTokens = json.load(fp = usersTokensFile)
            while (newToken in dictUserTokens): # verify the token is unique
                newToken = random.randint(1,9999)

        dictUserTokens[newToken] = nik_name
        with open(self.users_tokens, 'w') as usersTokensFile:
            json.dump(dictUserTokens, usersTokensFile, indent=4, separators=(',',': '))

        newUser = BE.User(token = newToken, nikName = nik_name)
        dictUsers = {}
        if (os.path.getsize(self.users_full) != 0):
            with open(self.users_full) as usersFile:
                dictUsers = json.load(usersFile)
        dictUsers[newUser.token] = newUser
        with open(self.users_full, 'w') as usersFile: # store the dict of users (with the new user) in the DB
            json.dump(dictUsers, usersFile, indent=4, separators=(',',': '), cls=UserEncoderJSON)

        return newUser
    

    # ============================
    # =========  READ  ===========

    def fetch_game_by_ID(self, id: str) -> BE.Game:
        """fetch a game from the DB based on its ID

        Args:
            id (str): the ID of the requested game

        Returns:
            BE.Game: the game whose ID was passed as parameter
        """
        try:
            with open(self.games) as gamesFile:
                dictGames = json.load(gamesFile)
            dictGame = dictGames[id]
            game                = BE.Game(dictGame["num_of_players"])
            game.game_ID        = dictGame["game_ID"]
            game.game_state     = dictGame["game_state"]
            game.board          = dictGame["board"]
            game.winner_ID      = dictGame["winner_ID"]
            game.creation_date  = datetime.datetime.fromisoformat(dictGame["creation_date"])
            game.duration       = dictGame["duration"]

            return game
        
        except json.JSONDecodeError:
            print("fetch_game_by_ID(): Seems like the 'games' file is empty or corrupted")
        except KeyError:
            print("fetch_game_by_ID(): The key in the dictionary is not found")
    

    def fetch_all_games(self) -> list:
        """fetch all the games in the DB

        Returns:
            list: a list of all the games in the DB
        """
        try:
            with open(self.games) as gamesFile:
                dictGames = json.load(gamesFile) # fetch all the games from the DB
            
            how_many_to_save = 30  # how many games we want to store in the database
            sorted_games_by_creationDate = sorted(dictGames.items(), key=lambda x:datetime.datetime.fromisoformat(x[1]["creation_date"]))
            # lastDateGamesFetched = datetime.datetime.now()

            # remove old games records (save only 'how_many_to_save' records or less), do it no more than once a day
            if (len(sorted_games_by_creationDate) > how_many_to_save):
                sorted_games_by_creationDate = sorted_games_by_creationDate[-30:]
                for index, game in enumerate(sorted_games_by_creationDate):
                    if (index < len(dictGames.items()) - how_many_to_save):
                        dictGames.pop(game[0]) # pop the game with game_ID 'game[0]'
                    else:
                        break
            
                with open(self.games, 'w') as gamesFile:
                    json.dump(dictGames, gamesFile, indent=4, separators=(',',': '), cls=GameEncoderJSON)

            return sorted_games_by_creationDate
        
        except json.JSONDecodeError:
            print("fetch_all_games(): Seems like the 'games' file is empty or corrupted")
            return []
        except KeyError:
            print("fetch_all_games(): The key in the dictionary is not found")
            return []
                    
    def fetch_users_stats(self) -> list:
        """fetch user statistics (not including sensitive data)

        Returns:
            list: a list of UserStats
        """
        try:
            with open(self.users_full) as usersFile:
                dictUsers = json.load(usersFile)
            
            users_list = []
            for key, user in dictUsers.items():
                users_list.append((user["nik_name"],user["user_stat"])) # list of statistics of all users
            
            return users_list
        
        except json.JSONDecodeError:
            print("fetch_users_stats(): Seems like the 'users' file is empty or corrupted")
            return []
        except KeyError:
            print("fetch_users_stats(): The key in the dictionary is not found")
            return []

    def fetch_user_by_ID(self, token: int) -> BE.User:
        """fetch a specific user based on its ID

        Args:
            token (int): a token of one user

        Returns:
            BE.User: the user whiose token was passed as parameter
        """
        try:
            with open(self.users_full) as usersFile:
                dictUsers = json.load(usersFile)
            
            if (token not in dictUsers):
                return "notFound"
            
            dictUser = dictUsers[token]
            user = BE.User(dictUser["token"],dictUser["nik_name"])
            user.creation_date = datetime.datetime.fromisoformat(dictUser["creation_date"])
            
            user.userStat.numOfGamesParticipated = dictUser["user_stat"]["games_participated"]
            user.userStat.gamesWon               = dictUser["user_stat"]["games_won"]
            user.userStat.gamesInTie             = dictUser["user_stat"]["games_tie"]
            user.userStat.avgTimeForMove         = dictUser["user_stat"]["avg_time_for_move"]
        
            return user
        
        except json.JSONDecodeError:
            print("fetch_user_by_ID(): Seems like the 'users_full' file is empty or corrupted")
        except KeyError:
            print("fetch_user_by_ID(): The key in the dictionary is not found")


    # ==============================
    # =========  UPDATE  ===========

    def update_game(self, game : BE.Game):
        """update a gmae in the DB (replace the old Game by a new Game)

        Args:
            game (BE.Game): the new and updated game
        """
        try:
            with open(self.games) as gamesFile:
                dictGames = json.load(gamesFile)
            id = game.game_ID
            dictGames.pop(id, None)
            dictGames[game.game_ID] = game

            with open(self.games, 'w') as gamesFile:
                json.dump(dictGames, gamesFile, indent=4, separators=(',',': '), cls=GameEncoderJSON)    
        
        except json.JSONDecodeError:
            print("update_game(): Seems like the file is empty or corrupted")


    def update_user(self, user : BE.User):
        """update a user in the DB

        Args:
            user (BE.User): the new user to replace wit the old User entry
        """
        try:
            with open(self.users_full) as usersFile:
                dictUsers = json.load(usersFile)
            
            if (dictUsers[user.token]["nik_name"] != user.nikName):
                with open(self.users_tokens) as usersTokensFile:
                    dictUsersTokens = json.load(usersTokensFile)
    
                dictUsersTokens.pop(user.token, None)
                dictUsersTokens[user.token] = user.nikName
    
                with open(self.users_tokens, 'w') as usersTokensFile:
                    json.dump(dictUsersTokens, usersTokensFile, indent=4, separators=(',',': '))

            dictUsers.pop(user.token, None)
            dictUsers[user.token] = user
            
            with open(self.users_full, 'w') as usersFile:
                json.dump(dictUsers, usersFile, indent=4, separators=(',',': '), cls=UserEncoderJSON)    
        
        except json.JSONDecodeError:
            print("update_user(): Seems like the file is empty")
        

    def update_users(self, users_list: list):
        """update a list of users at once. the update is made only for the statistics, if anyone
            wants to update its nik_name, it can be done through the function 'update_user'

        Args:
            users_list (list): a list of users to be updated in the DB
        """
        try:
            with open(self.users_full) as usersFile:
                dictUsersFull = json.load(usersFile)
            
            for user in users_list:
                dictUsersFull.pop(user.token, None)     
                dictUsersFull[user.token] = user
            
            with open(self.users_full, 'w') as usersFile:
                json.dump(dictUsersFull, usersFile, indent=4, separators=(',',': '), cls=UserEncoderJSON)    
        
        except json.JSONDecodeError:
            print("update_users(): Seems like the file is empty")

    # ==============================
    # =========  DELETE  ===========

    def delete_game_by_ID(self, id: str):
        """dalete some game baes on its ID

        Args:
            id (str): the ID of the game to be deleted
        """
        try:
            with open(self.games) as gamesFile:
                dictGames = json.load(gamesFile)
            dictGames.pop(id, None)

            with open(self.games, 'w') as gamesFile:
                json.dump(dictGames, gamesFile, indent=4, separators=(',',': '), cls=GameEncoderJSON)
        
        except json.JSONDecodeError:
            print("delete_game_by_ID(): Seems like the file is empty anyway, or the file is corrupted")


    def delete_user_by_ID(self, id: str):
        """delete user based on its token

        Args:
            id (str): the token of the user to be deleted
        """
        try:
            with open(self.users_tokens) as usersTokensFile:
                dictUserTokens = json.load(usersTokensFile)
            dictUserTokens.pop(id, None) # delete from the file includes only tokens and nik names
            
            with open(self.users_tokens, 'w') as usersTokensFile:
                json.dump(dictUserTokens, usersTokensFile, indent=4, separators=(',',': '))

            with open(self.users_full) as usersFullFile:
                dictUsers = json.load(usersFullFile)
            dictUsers.pop(id, None) # delete from the file includes full data on the users
            
            with open(self.users_full, 'w') as usersFullFile:
                json.dump(dictUsers, usersFullFile, indent=4, separators=(',',': '), cls=UserEncoderJSON)
            
        
        except json.JSONDecodeError:
            print("delete_user_by_ID(): Seems like the file is empty anyway, or the file is corrupted")


class GameEncoderJSON(json.JSONEncoder):
    """encoder of a Game (a custom class can't be converted to a json object directly)
    """
    def default(self, obj):
        if isinstance(obj, BE.Game):
            return {"game_ID"       : obj.game_ID,
                    "num_of_players": obj.num_of_players,
                    "game_state"    : obj.game_state,
                    "board"         : obj.board,
                    "winner_ID"     : obj.winner_ID,
                    "creation_date" : obj.creation_date.isoformat(),
                    "duration"      : obj.duration,
                    }
        return super().default(obj)
    
class UserEncoderJSON(json.JSONEncoder):
    """encoder of a Game (a custom class can't be converted to a json object directly)
    """
    def default(self, obj):
        if isinstance(obj, BE.User):
            return {"token"         : obj.token,
                    "nik_name"      : obj.nikName,
                    "creation_date" : obj.creation_date.isoformat(),
                    "user_stat"     : serialize_userStat_JSON(obj.userStat)
                    }
        return super().default(obj)
    
def serialize_userStat_JSON(userStat : BE.UserStat):
    """helps the user encoder encode the UserStat object

    Args:
        userStat (BE.UserStat): the object to be encoded

    Returns:
        dict: a dict represented an encoded UserStat
    """
    return {"games_participated": userStat.numOfGamesParticipated,
            "games_won"         : userStat.gamesWon,
            "games_tie"         : userStat.gamesInTie,
            "avg_time_for_move" : userStat.avgTimeForMove
            }
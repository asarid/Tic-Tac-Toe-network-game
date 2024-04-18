import abc
import json
import random
import sys
import os
import datetime

conf_path = os.getcwd()
sys.path.append(conf_path[:conf_path.rfind("\\")])
databases_path = sys.path.append(conf_path[:conf_path.rfind("\\")+1]+"Databases")


import BusinessEntities as BE



class DataAccessInterface(metaclass=abc.ABCMeta):


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
    def __init__(self):
        self._creators = {}

    def register_DB_access(self, format, creator):
        self._creators[format] = creator

    def get_access_by_DB_type(self, format):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()





class JSON_db_access(DataAccessInterface):
    
    def __init__(self):
        self.users_full = "../Databases/JSON/users_full.json"
        self.users_tokens = "../Databases/JSON/users_tokens.json"
        self.games = "../Databases/JSON/games.json"

        files = [self.users_full,self.users_tokens,self.games]
        
        # Check if file exists
        for filePath in files:
            if os.path.exists(filePath) is False:
                raise Exception("File not found")    
        
        self.lastDateGamesFetched = datetime.datetime.now()


    # ==============================
    # =========  CREATE  ===========

    def create_new_game(self, numOfPlayers):
        newGame = BE.Game(num_of_players = numOfPlayers)
        dictGames = {}

        if (os.path.getsize(self.games) != 0):
            with open(self.games) as gamesFile:
                dictGames = json.load(gamesFile)
        dictGames[newGame.game_ID] = newGame

        with open(self.games, 'w') as gamesFile:
            json.dump(dictGames, gamesFile, indent=4, separators=(',',': '), cls=GameEncoderJSON)

        return newGame


    def create_new_user(self, nik_name : str) -> BE.User:

        dictUserTokens = {}
        newToken = random.randint(1,9999)

        if (os.path.getsize(self.users_tokens) != 0):
            with open(self.users_tokens) as usersTokensFile:
                dictUserTokens = json.load(fp = usersTokensFile)
            while (newToken in dictUserTokens):
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
        with open(self.users_full, 'w') as usersFile:
            json.dump(dictUsers, usersFile, indent=4, separators=(',',': '), cls=UserEncoderJSON)

        return newUser
    

    # ============================
    # =========  READ  ===========

    def fetch_game_by_ID(self, id: str) -> BE.Game:
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
        try:
            with open(self.games) as gamesFile:
                dictGames = json.load(gamesFile)
            
            how_many_to_save = 30  # how many games we want to store in the database
            sorted_games_by_creationDate = sorted(dictGames.items(), key=lambda x:datetime.datetime.fromisoformat(x[1]["creation_date"]))
            lastDateGamesFetched = datetime.datetime.now()

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
        try:
            with open(self.users_full) as usersFile:
                dictUsers = json.load(usersFile)
            
            users_list = []
            for key, user in dictUsers.items():
                users_list.append((user["nik_name"],user["user_stat"]))
            
            return users_list
        
        except json.JSONDecodeError:
            print("fetch_users_stats(): Seems like the 'users' file is empty or corrupted")
            return []
        except KeyError:
            print("fetch_users_stats(): The key in the dictionary is not found")
            return []

    def fetch_user_by_ID(self, token: int) -> BE.User:
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
        try:
            with open(self.games) as gamesFile:
                dictGames = json.load(gamesFile)
            dictGames.pop(id, None)

            with open(self.games, 'w') as gamesFile:
                json.dump(dictGames, gamesFile, indent=4, separators=(',',': '), cls=GameEncoderJSON)
        
        except json.JSONDecodeError:
            print("delete_game_by_ID(): Seems like the file is empty anyway, or the file is corrupted")


    def delete_user_by_ID(self, id: str):
        try:
            with open(self.users_tokens) as usersTokensFile:
                dictUserTokens = json.load(usersTokensFile)
            dictUserTokens.pop(id, None)
            
            with open(self.users_tokens, 'w') as usersTokensFile:
                json.dump(dictUserTokens, usersTokensFile, indent=4, separators=(',',': '))

            with open(self.users_full) as usersFullFile:
                dictUsers = json.load(usersFullFile)
            dictUsers.pop(id, None)
            
            with open(self.users_full, 'w') as usersFullFile:
                json.dump(dictUsers, usersFullFile, indent=4, separators=(',',': '), cls=UserEncoderJSON)
            
        
        except json.JSONDecodeError:
            print("delete_user_by_ID(): Seems like the file is empty anyway, or the file is corrupted")


class GameEncoderJSON(json.JSONEncoder):
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
    def default(self, obj):
        if isinstance(obj, BE.User):
            return {"token"         : obj.token,
                    "nik_name"      : obj.nikName,
                    "creation_date" : obj.creation_date.isoformat(),
                    "user_stat"     : serialize_userStat_JSON(obj.userStat)
                    }
        return super().default(obj)
    
def serialize_userStat_JSON(userStat : BE.UserStat):
    return {"games_participated": userStat.numOfGamesParticipated,
            "games_won"         : userStat.gamesWon,
            "games_tie"         : userStat.gamesInTie,
            "avg_time_for_move" : userStat.avgTimeForMove
            }
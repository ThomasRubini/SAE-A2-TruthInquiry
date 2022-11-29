import string
import random


# Map of all actively running games
# game_lists["game.id"]-> game info linked to that id
game_lists = {}

def random_string(length: int) ->str:
    """
    This function create a random string as long as the lint passed as 
    parameter
    
    : param length: the lenght of the random string
    : type length : int
    : return      : a random string
    : return type : string
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))

class GameInfo:
    """
    The game info class stores all information linked to a active game

    Game.start_token : str, 
    Game.id : str, the game identifier of the game
    """
    def __init__(self):
        self.start_token = None

def create_game():
    """
    This function creates a new game by creating a GameInfo object and stores 
    it into the game_lists dictionnary

    : return      : a new GameInfo
    : return type : GameInfo
    """
    game = GameInfo()
    game.id = random_string(6)
    game.start_token = random_string(64)
    game_lists[game.id] = game
    #TODO ADD A WEBSOCKET IF THE GAME IS KNOWN TO BE MULTIPLAYER
    return game

def get_game_info(game_id):
    """
    This function retrieve a the GameInfo object linked to the game_id
    passed as parametter

    : param game_id : the lenght of the random string
    : type game_id  : str
    : return        : The GameInfo Object linked to the gameId
    : return type   : GameInfo
    """
    if game_id in game_lists:
        return game_lists[game_id]
    else:
        return None
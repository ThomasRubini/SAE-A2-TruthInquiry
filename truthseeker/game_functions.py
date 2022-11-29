import string
import random
import jwt
from datetime import datetime, timedelta
import truthseeker

# Map of all actively running games
# games_list["game.id"]-> game info linked to that id
games_list = {}

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

class Member:
    """
    stores information related to the member of a given game

    Member.username : The username of this member
    Member.socker : The reference to the socket to talk to this member

    """
    def __init__(self, username):
        self.username = username
        self.socket = None

class GameInfo:
    """
    The game info class stores all information linked to a active game
 
    GameInfo.id : str, the game identifier of the game
    GameInfo.owner : Member, the game identifier of the game
    GameInfo.members : Member[], the members of the game
    """
    def __init__(self):
        self.game_id = None
        self.owner = None
        self.members = []

    def _gen_jwt(self, username, owner):
        return jwt.encode(
            payload={
                "game_id": self.game_id,
                "username": username,
                "owner": owner,
                "exp": datetime.utcnow() + timedelta(hours = 1) # handled automatically on jwt.decode
            },
            key=truthseeker.app.config["SECRET_KEY"],
            algorithm="HS256"
        )

    def set_owner(self, username):
        self.owner = Member(username)
        self.members.append(self.owner)
        return self.owner, self._gen_jwt(username, owner=True)

    def add_member(self, username):
        member = Member(username)
        self.members.append(member)
        return member, self._gen_jwt(username, owner=False)

def create_game():
    """
    This function creates a new game by creating a GameInfo object and stores 
    it into the games_list dictionnary

    : return      : a new GameInfo
    : return type : GameInfo
    """
    game = GameInfo()
    game.id = random_string(6)
    game.start_token = random_string(64)
    games_list[game.id] = game
    #TODO ADD A WEBSOCKET IF THE GAME IS KNOWN TO BE MULTIPLAYER
    return game

def get_game(game_id):
    if game_id in games_list:
        return games_list[game_id]
    else:
        return None

def get_game_info(game_id):
    """
    This function retrieve a the GameInfo object linked to the game_id
    passed as parametter

    : param game_id : the lenght of the random string
    : type game_id  : str
    : return        : The GameInfo Object linked to the game_id
    : return type   : GameInfo
    """
    if game_id in games_list:
        return games_list[game_id]
    else:
        return None
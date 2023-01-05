import string
import random
from datetime import datetime, timedelta
import truthseeker


# Map of all actively running games
# games_list["game.game_id"]-> game info linked to that id
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

    def __str__(self) -> str:
        return "Member[username={}]".format(self.username)

    def __repr__(self) -> str:
        return self.__str__()

class Game:
    """
    The game info class stores all information linked to a active game
 
    Game.game_id : str, the game identifier of the game
    Game.owner : Member, the game identifier of the game
    Game.members : Member[], the members of the game
    """
    def __init__(self):
        self.game_id = None
        self.owner = None
        self.members = []
        self.has_started = True

    def set_owner(self, username):
        self.owner = Member(username)
        self.members.append(self.owner)
        return self.owner

    def get_member(self, username):
        for member in self.members:
            if member.username == username:
                return member

    def add_member(self, username):
        if self.get_member(username):
            return None
        member = Member(username)
        self.members.append(member)
        return member

    def __str__(self) -> str:
        return "Game[game_id={}, owner={}, members={}]".format(self.game_id, self.owner, self.members)

    def __repr__(self) -> str:
        return self.__str__()

def create_game(owner):
    """
    This function creates a new game by creating a Game object and stores 
    it into the games_list dictionnary

    : return      : a new Game
    : return type : Game
    """
    game = Game()
    game.owner = owner
    game.members.append(Member(owner))
    game.game_id = random_string(6)
    games_list[game.game_id] = game
    #TODO ADD A WEBSOCKET IF THE GAME IS KNOWN TO BE MULTIPLAYER
    return game

def get_game(game_id):
    if game_id in games_list:
        return games_list[game_id]
    else:
        return None

def get_game_info(game_id):
    """
    This function retrieve a the Game object linked to the game_id
    passed as parametter

    : param game_id : the lenght of the random string
    : type game_id  : str
    : return        : The Game Object linked to the game_id
    : return type   : Game
    """
    if game_id in games_list:
        return games_list[game_id]
    else:
        return None
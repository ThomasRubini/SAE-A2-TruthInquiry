import string
import random
from truthseeker.logic.data_persistance.data_access import *
from datetime import datetime, timedelta
from truthseeker import APP


# Map of all actively running games
# games_list["game.game_id"]-> game info linked to that id

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
        self.has_started = False
        self.gamedata = {}
        self.reaction_table = {}

    def set_owner(self, username):
        self.owner = Member(username)
        self.members.append(self.owner)
        return self.owner

    def generate_data(self):
        #TODO Get language from player
        self.gamedata, self.reaction_table = generateGameData("FR")

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

    def get_npc_reaction(self,npc_id,reaction):
        if npc_id not in self.reaction_table.keys():
            return 0
        reaction_id = self.reaction_table[npc_id][int(reaction)]
        return read_image(f"./truthseeker/static/images/npc/{npc_id}/{reaction_id}.png")

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
    APP.games_list[game.game_id] = game
    return game

def get_game(game_id):
    if game_id in APP.games_list:
        return APP.games_list[game_id]
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
    if game_id in APP.games_list:
        return APP.games_list[game_id]
    else:
        return None

def generateNpcText(npc: tables.Npc, lang: str) -> dict:
    data = {}
    data["name"] = getTextFromLid(lang, npc.NAME_LID)
    data["QA_0"] = getTextFromLid(lang, getNpcRandomAnswer(npc,0).TEXT_LID)
    data["QA_1"] = getTextFromLid(lang, getNpcRandomAnswer(npc,1).TEXT_LID)
    return data

def generateNpcReactions(npc : tables.Npc) ->list:
    data = []
    data.append(getNpcRandomTraitId(npc))
    data.append(getNpcRandomTraitId(npc))
    return data

def generatePlaceData(npcs :list, places: list, lang : str) -> dict:
    data = {}
    random.shuffle(npcs)
    for place in places:
        placedata = data[str(place.PLACE_ID)] = {}
        placedata["name"] = getTextFromLid(lang,place.NAME_LID)
        placedata["npcs"] = []
        for _ in npcs:
            placedata["npcs"].append(npcs.pop().NPC_ID)
            if len(placedata["npcs"]) == 2: break
    return data


def generateGameData(LANG):
    data = {}
    data["npcs"] = {}
    reactions_table = {}
    npcs = []
    while len(npcs) != 5:
        npc = getRandomNpc()
        if npc not in npcs :
            npcs.append(npc)
    for npc in npcs:
        data["npcs"][str(npc.NPC_ID)] = generateNpcText(npc,LANG)
        reactions_table[str(npc.NPC_ID)] = generateNpcReactions(npc)

    places = []
    while len(places) != 3:
        place = getRandomPlace()
        if place not in places:
            places.append(place)

    data["rooms"] = generatePlaceData(npcs,places,LANG)
    data["questions"] = {}
    data["questions"]["QA_0"] = getTextFromLid("FR",getRandomQuestion(0).TEXT_LID)
    data["questions"]["QA_1"] = getTextFromLid("FR",getRandomQuestion(1).TEXT_LID)
    return data, reactions_table


def read_image(path:str):
    try:
        return open(path, "rb").read()
    except:
        return 1

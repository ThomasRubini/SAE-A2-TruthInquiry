import string
import random
from typing import Union

from truthseeker.logic.data_persistance.data_access import *
from truthseeker import APP

def random_string(length: int) ->str:
    """
    This function create a random string as long as the lint passed as 
    parameter
    
    :param length: the length of the random string to create
    :return: a random string
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))

class Member:
    """
    stores information related to the member of a given game

    :attr str username: The username of this member
    :attr TODO progress: TODO
    :attr TODO results: TODO
    """
    
    def __init__(self, username):
        self.username = username
        self.progress = 0
        self.results = None

    def __str__(self) -> str:
        return "Member[username={}]".format(self.username)

    def __repr__(self) -> str:
        return self.__str__()

class Game:
    """
    The game info class stores all information linked to a active game

    :attr str game_id: str, the game identifier of the game
    :attr owner  Member: the player start created the game. It is also stored in self.members
    :attr Member[] members: the members of the game
    :attr bool has_started: TODO
    :attr TODO gamedata: TODO
    :attr TODO reaction_table: TODO
    """

    def __init__(self):
        self.game_id = None
        self.owner = None
        self.members = []
        self.has_started = False
        self.gamedata = {}
        self.reaction_table = {}

    def set_owner(self, username: str) -> Member:
        """
        Set the owner of the game

        :param username: the username of the owner.
        :return: the Member object created by this method
        """
        self.owner = Member(username)
        self.members.append(self.owner)
        return self.owner
    
    def generate_game_results(self) -> None:
        """
        TODO + TODO RET TYPE
        """
        data = {}
        npcs = data["npcs"] = {}
        for npc_id in self.gamedata["npcs"]:
            npcs[npc_id] = {}
            npcs[npc_id]["name"] = self.gamedata["npcs"][npc_id]["name"]
            traitId = self.reaction_table[npc_id]
            trait = get_trait_from_trait_id(traitId)
            npcs[npc_id]["reaction"] = get_text_from_lid("FR",trait.NAME_LID)
        player_results = data["player"] = {}
        for member in self.members:
            player_results[member.username] = member.results
        return data

    def generate_data(self) -> None:
        """
        TODO
        """
        #TODO Get language from player
        self.gamedata, self.reaction_table = generate_game_data("FR")

    def get_member(self, username: str) -> Union[Member, None]:
        """
        Get a Member object from a username

        :param username: the username of the member to search for
        :return the member corresponding to the username, or None if none if found:
        """
        for member in self.members:
            if member.username == username:
                return member
        
    def add_member(self, username: str) -> Union[Member, None]:
        """
        Add a Member to the game

        :param username: the username of the member to add
        :return: the Member created, or None if a Member with this username already exists in the game
        """
        if self.get_member(username):
            return None
        member = Member(username)
        self.members.append(member)
        return member

    def get_npc_reaction(self, npc_id, reaction) -> None:
        """
        TODO + TODO TYPES
        """
        if npc_id not in self.reaction_table.keys():
            return 0
        reaction_id = self.reaction_table[npc_id][int(reaction)]
        return read_image(f"./truthseeker/static/images/npc/{npc_id}/{reaction_id}.png")
    
    def get_player_results(self, responses: dict) -> None:
        """
        TODO + TODO RETTYPE
        """
        results = {}
        try:
            for npc_id in responses:
                trait_id = get_trait_id_from_string(responses[npc_id])
                results[npc_id] = trait_id == str(self.reaction_table[npc_id])
            return results
        except:
            return False


    def has_finished(self) -> bool:
        """
        Checks if the game has finished by checking if every Member has submitted answers
        
        :return: True if the game has finished, else False
        """
        for member in self.members:
            if member.results == None : return False
        return True

    def __str__(self) -> str:
        return "Game[game_id={}, owner={}, members={}]".format(self.game_id, self.owner, self.members)

    def __repr__(self) -> str:
        return self.__str__()

def create_game(owner: str) -> Game:
    """
    This function creates a new game by creating a Game object and stores 
    it into the games_list dictionnary

    :return: a new Game
    """
    game = Game()
    game.owner = owner
    game.members.append(Member(owner))
    game.game_id = random_string(6)
    APP.games_list[game.game_id] = game
    return game

def get_game(game_id: str) -> Union[Game, None]:
    """
    Get a game from its ID

    :param game_id: the id of the game to search
    :return: the Game object or None if not found
    """
    if game_id in APP.games_list:
        return APP.games_list[game_id]
    else:
        return None

def check_username(username: str) -> bool:
    """
    Check if a username is valid using a set of rules

    :param username: the username to check
    :return: True or False depending on if the rules are respected
    """
    
    if not username:
        return False
    if not username.isalnum():
        return False
    if not username == username.strip():
        return False
    if not len(username) < 16:
        return False
    
    return True

def generate_npc_text(npc: tables.Npc, lang: str) -> dict:
    data = {}
    data["name"] = get_text_from_lid(lang, npc.NAME_LID)
    data["QA_0"] = get_text_from_lid(lang, get_npc_random_answer(npc,0).TEXT_LID)
    data["QA_1"] = get_text_from_lid(lang, get_npc_random_answer(npc,1).TEXT_LID)
    return data

def generate_npc_reactions(npc: tables.Npc) ->list:
    return get_npc_random_trait_id(npc)

def generate_place_data(npcs: list, places: list, lang: str) -> dict:
    data = {}
    random.shuffle(npcs)
    for place in places:
        placedata = data[str(place.PLACE_ID)] = {}
        placedata["name"] = get_text_from_lid(lang,place.NAME_LID)
        placedata["npcs"] = []
        for _ in npcs:
            placedata["npcs"].append(npcs.pop().NPC_ID)
            if len(placedata["npcs"]) == 2: break
    return data


def generate_game_data(LANG):
    data = {}
    data["npcs"] = {}
    reactions_table = {}
    npcs = []
    while len(npcs) != 5:
        npc = get_random_npc()
        if npc not in npcs :
            npcs.append(npc)
    for npc in npcs:
        data["npcs"][str(npc.NPC_ID)] = generate_npc_text(npc,LANG)
        reactions_table[str(npc.NPC_ID)] = generate_npc_reactions(npc)

    places = []
    while len(places) != 3:
        place = get_random_place()
        if place not in places:
            places.append(place)

    data["rooms"] = generate_place_data(npcs,places,LANG)
    data["questions"] = {}
    data["questions"]["QA_0"] = get_text_from_lid("FR",get_random_question(0).TEXT_LID)
    data["questions"]["QA_1"] = get_text_from_lid("FR",get_random_question(1).TEXT_LID)
    data["traits"] = get_traits(LANG)
    return data, reactions_table

def read_image(path:str):
    try:
        return open(path, "rb").read()
    except:
        return 1

def get_trait_id_from_string(trait):
    return get_trait_from_text(trait)

def get_npc_image(npc_id):
    return read_image(f"./truthseeker/static/images/npc/{npc_id}/0.png")

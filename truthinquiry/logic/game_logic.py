import string
import random
from typing import Union

from truthinquiry.ext.database.models import *
from truthinquiry.ext.database import dbutils

games_list = {}

def random_string(length: int) -> str:
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
        return f"Member[username={self.username}]"

    def __repr__(self) -> str:
        return self.__str__()


class Game:
    """
    The game info class stores all information linked to a active game

    :attr str game_id: the game identifier of the game
    :attr owner  Member: the player start created the game. It is also stored in self.members
    :attr Member[] members: the members of the game
    :attr bool has_started: status of the current game
    :attr dict gamedata: data of the game (npcs, their text, their reactions and rooms placement)
    :attr dict reaction_table: mapping of the npc_ids in the game to their reactions id
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

    def generate_game_results(self) -> dict:
        """
        Create the final leaderboard of the game, containing all members score.

        :return: a dictionnary representation of the leaderboard
        """
        data = {}
        npcs = data["npcs"] = {}
        for npc_id in self.gamedata["npcs"]:
            npcs[npc_id] = {}
            npcs[npc_id]["name"] = self.gamedata["npcs"][npc_id]["name"]
            trait_id = self.reaction_table[npc_id]
            trait = dbutils.get_trait_from_trait_id(trait_id)
            npcs[npc_id]["reaction"] = dbutils.get_text_from_lid("FR", trait.NAME_LID)
            npcs[npc_id]["description"] = dbutils.get_reaction_description("FR", trait.TRAIT_ID)
        player_results = data["player"] = {}
        for member in self.members:
            player_results[member.username] = member.results
        return data

    def generate_data(self) -> None:
        """
        Creates and sets the game's data (npcs, their text, their reactions and rooms placement)
        """
#       TODO Get language from player
        self.gamedata, self.reaction_table = generate_game_data("FR")
        self.gamedata["game_id"] = self.game_id

    def get_member(self, username: str) -> Union[Member, None]:
        """
        Get a Member object from a username

        :param username: the username of the member to search for
        :return: the member corresponding to the username, or None if none if found:
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

    def get_npc_reaction(self, npc_id) -> bytes:
        """
        Returns the reaction image of a npc, if found in the reaction table

        :param npc_id: the id of the npc, to get the reactions from, must be in the current game
        :return: the reaction image as bytes
        """
        if npc_id not in self.reaction_table:
            return 0
        reaction_id = self.reaction_table[npc_id]
        return read_image(f"./truthinquiry/static/images/npc/{npc_id}/{reaction_id}.png")

    def get_player_results(self, responses: dict) -> Union[dict, None]:
        """
        Checks the player's answers againts the reaction map.
        Return None when a npc is not found in the reaction table, meaning an invalid npc was sent

        :param responses: the player anwsers, a dictionnary of npc_id to the string representation of the npc's reaction
        :return: a dictionnary of npc_id to a boolean, true if they got the correct answer, false if not.
        """
        results = {}
        try:
            for npc_id in responses:
                trait_id = get_trait_id_from_string(responses[npc_id])
                results[npc_id] = trait_id == self.reaction_table[npc_id]
            return results
        except:
            return False

    def has_finished(self) -> bool:
        """
        Checks if the game has finished by checking if every Member has submitted answers

        :return: True if the game has finished, else False
        """
        for member in self.members:
            if member.results is None:
                return False
        return True

    def __str__(self) -> str:
        return f"Game[game_id={self.game_id}, owner={self.owner}, members={self.members}]"

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
    games_list[game.game_id] = game
    return game


def get_game(game_id: str) -> Union[Game, None]:
    """
    Get a game from its ID

    :param game_id: the id of the game to search
    :return: the Game object or None if not found
    """
    if game_id in games_list:
        return games_list[game_id]
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


def generate_npc_text(npc: Npc, lang: str) -> dict:
    """
    Creates the dictionnary of a npc names and dialogs, it searches the npc's pool of answser for both question
    types

    :param npc: a Npc object
    :param lang: the lang to get the text in
    :return: a dictionnary object containing the npc's name and both answers
    """
    data = {}
    data["name"] = dbutils.get_text_from_lid(lang, npc.NAME_LID)
    data["QA_0"] = dbutils.get_text_from_lid(lang, dbutils.get_npc_random_answer(npc, 0).TEXT_LID)
    data["QA_1"] = dbutils.get_text_from_lid(lang, dbutils.get_npc_random_answer(npc, 1).TEXT_LID)
    return data


def generate_place_data(npc_list: list, places: list, lang: str) -> dict:
    """
    Create the place dictionnary for a game, assigns two npc for each room given in the place_list
    except the last one who will be alone :(

    :param npcs_list: the list of all npcs in the game
    :param place_list: the list of the given rooms
    :param lang: the language to seach the name of the room in
    :return: a dictionnary of place_id to an array of npc_id and a string of the room name
    """
    data = {}
    random.shuffle(npc_list)
    for place in places:
        placedata = data[str(place.PLACE_ID)] = {}
        placedata["name"] = dbutils.get_text_from_lid(lang, place.NAME_LID)
        placedata["npcs"] = []
        for _ in npc_list:
            placedata["npcs"].append(npc_list.pop().NPC_ID)
            if len(placedata["npcs"]) == 2:
                break
    return data


def generate_game_data(lang: str) -> tuple[dict, dict]:
    """
    Create the gamedata of a game for a given language, chooses 5 random npcs, generate their texts and reactions,
    chooses 3 random rooms and places the npcs in them and chooses an inspector question for each type of question
    availible in the Question Table.

    :param lang: the lang to generate all the texts in
    :return: two dictionnaries, one containing the game data, the second containing the reaction table
    """
    data = {}
    data["npcs"] = {}
    reactions_table = {}
    npcs = []
    while len(npcs) != 5:
        npc = dbutils.get_random_npc()
        if npc not in npcs:
            npcs.append(npc)
    for npc in npcs:
        data["npcs"][str(npc.NPC_ID)] = generate_npc_text(npc, lang)
        reactions_table[str(npc.NPC_ID)] = dbutils.get_npc_random_trait_id(npc)

    places = []
    while len(places) != 3:
        place = dbutils.get_random_place()
        if place not in places:
            places.append(place)

    data["rooms"] = generate_place_data(npcs, places, lang)
    data["questions"] = {}
    data["questions"]["QA_0"] = dbutils.get_text_from_lid("FR", dbutils.get_random_question(0).TEXT_LID)
    data["questions"]["QA_1"] = dbutils.get_text_from_lid("FR", dbutils.get_random_question(1).TEXT_LID)
    data["traits"] = dbutils.get_traits(lang)
    return data, reactions_table


def read_image(path: str) -> bytes:
    """
    Returns the byte representation of an image given its path

    :param path: the path to the image
    :return: the byte representation of the image, none if its not found or not readable
    """
    try:
        with open(path, "rb") as file:
            return file.read()
    except IOError:
        return None


def get_trait_id_from_string(trait: str) -> int:
    """
    Returns the trait_id from its text value

    :param text: the text representation of the trait in any lang
    :return: the trait_id linked to this text
    """
    return dbutils.get_trait_from_text(trait)


def get_npc_image(npc_id: int):
    """
    Returns the byte representation of the neutral image for an npc

    :param npc_id: npc to get the neutral image from
    :return: the byte representation of the image, none if its not found or not readable
    """
    return read_image(f"./truthinquiry/static/images/npc/{npc_id}/0.png")
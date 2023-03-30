from truthinquiry import create_app
import json

import pytest
from dotenv import load_dotenv

# Load dotenv file
load_dotenv()

app = create_app()

###############################################################################
#                                                                             #
#                                                                             #
#                               Test Classes                                  #
#                                                                             #
#                                                                             #
###############################################################################


class TestException(Exception):
    __test__ = False

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class User:
    def __init__(self, username):
        self.username = username
        self.client = app.test_client()


def create_game(user: User) -> str:
    """_summary_

    Args:
        user (User): _description_

    Raises:
        TestException: _description_
        TestException: _description_
        TestException: _description_

    Returns:
        str: _description_
    """
    data = {"username": user.username}
    responseObject = user.client.post("/api/v1/createGame", data=data)
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return content["game_id"]


def join_game(user: User, game_id: str) -> bool:
    """_summary_

    Args:
        user (User): _description_
        game_id (str): _description_

    Raises:
        TestException: _description_
        TestException: _description_
        TestException: _description_

    Returns:
        bool: _description_
    """
    data = {"username": user.username, "game_id": game_id}
    responseObject = user.client.post("/api/v1/joinGame", data=data)
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return True


def start_game(user: User) -> bool:
    """_summary_

    Args:
        user (User): _description_

    Raises:
        TestException: _description_
        TestException: _description_
        TestException: _description_

    Returns:
        bool: _description_
    """
    responseObject = user.client.post("/api/v1/startGame")
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return True


def get_game_data(user: User) -> tuple:
    """_summary_

    Args:
        user (User): _description_

    Raises:
        TestException: _description_
        TestException: _description_
        TestException: _description_

    Returns:
        tuple: _description_
    """
    responseObject = user.client.post("/api/v1/getGameData")
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return (content["gamedata"], content["username"])


def get_game_members(game_id: str) -> list:
    """_summary_

    Args:
        game_id (str): _description_

    Raises:
        TestException: _description_
        TestException: _description_
        TestException: _description_

    Returns:
        list: _description_
    """
    app_client = app.test_client()
    data = {"game_id":game_id}
    responseObject = app_client.post("/api/v1/getGameMembers",data=data)
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return content["members"]


def is_owner(user: User) -> bool:
    """_summary_

    Args:
        user (User): _description_

    Raises:
        TestException: _description_
        TestException: _description_
        TestException: _description_

    Returns:
        bool: _description_
    """
    responseObject = user.client.post("/api/v1/isOwner")
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return content["owner"]


def has_joined(user: User) -> bool:
    """_summary_

    Args:
        user (User): _description_

    Raises:
        TestException: _description_
        TestException: _description_
        TestException: _description_

    Returns:
        bool: _description_
    """
    responseObject = user.client.post("/api/v1/hasJoined")
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return content["joined"]


def check_anwser(user: User, responses: list) -> bool:
    """_summary_

    Args:
        user (User): _description_
        responses (list): _description_

    Raises:
        TestException: _description_
        TestException: _description_
        TestException: _description_

    Returns:
        bool: _description_
    """
    data = {"responses": responses}
    responseObject = user.client.post("/api/v1/submitAnswers", data=data)
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return True

###############################################################################
#                                                                             #
#                                                                             #
#                           /api/v1/createGame                                #
#                                                                             #
#                                                                             #
###############################################################################
#
# This endpoint create a game in the server, the username passed as parametter 
# is set as the game owner


def test_that_people_can_create_a_game():
    user = User("neotaku")
    assert create_game(user) != False


def test_that_two_person_creating_two_games_results_in_two_distincts_game():
    userOne = User("neorage")
    userTwo = User("neobergine")
    gameOne = create_game(userOne)
    gameTwo = create_game(userTwo)
    assert gameOne != gameTwo


def test_that_two_person_having_the_same_pseudo_creating_two_games_results_in_two_distincts_games():
    userOne = User("neo")
    userTwo = User("neo")
    gameOne = create_game(userOne)
    gameTwo = create_game(userTwo)
    assert gameOne != gameTwo


def test_that_not_sending_a_username_results_in_an_error():
    app_client = app.test_client()
    responseObject = app_client.post("/api/v1/createGame")
    assert responseObject.status_code == 200
    assert responseObject.json["error"] != 0


def test_that_sending_a_empty_username_results_in_an_error():
    user = User("")
    with pytest.raises(TestException) as e:
        create_game(user)


def test_that_a_too_long_username_results_in_an_error():
    user = User("Le test unitaire est un moyen de vérifier qu’un extrait de code fonctionne correctement. C’est l’une des procédures mises en oeuvre dans le cadre d’une méthodologie de travail agile. ")
    with pytest.raises(TestException) as e:
        create_game(user)


def test_that_username_that_contains_non_alphanumerics_results_in_an_error():
    user = User("я русский пират")
    with pytest.raises(TestException) as e:
        create_game(user)

###############################################################################
#                                                                             #
#                                                                             #
#                              /api/v1/joinGame                               #
#                                                                             #
#                                                                             #
###############################################################################
#
# This endpoint adds the username passed as parameter to the game identified by
# its game_id also passed as the parametter


def test_that_people_can_join_a_game():
    game_id = create_game(User("neoracle"))
    assert join_game(User("neobjectif"), game_id) == True


def test_that_two_person_can_join_a_game():
    game_id = create_game(User("neomblic"))
    joueur1_a_join = join_game(User("neobjectif"), game_id)
    joueur2_a_join = join_game(User("neorgane"), game_id)
    assert joueur1_a_join == True and joueur2_a_join == True


def test_that_people_cant_join_if_the_username_is_already_used():
    game_id = create_game(User("neoreille"))
    join_game(User("neosomse"), game_id)
    with pytest.raises(TestException) as e:
        join_game(User("neosomse"), game_id)


def test_that_people_joining_without_sending_any_data_results_in_an_error():
    app_client = app.test_client()
    responseObject = app_client.post("/api/v1/joinGame")
    assert responseObject.status_code == 200
    assert responseObject.json["error"] != 0


def test_that_people_joining_without_sending_a_game_id_results_in_an_error():
    data = {"username": "neomblic"}
    app_client = app.test_client()
    responseObject = app_client.post("/api/v1/joinGame", data=data)
    assert responseObject.status_code == 200
    assert responseObject.json["error"] != 0


def test_that_people_joining_without_sending_an_username_still_results_in_an_error():
    game_id = create_game(User("neonyx"))
    data = {"game_id": game_id}
    app_client = app.test_client()
    responseObject = app_client.post("/api/v1/joinGame", data=data)
    assert responseObject.status_code == 200
    assert responseObject.json["error"] != 0


def test_that_people_joining_with_an_empty_username_still_results_in_an_error():
    game_id = create_game(User("neodeur"))
    user = User("")

    with pytest.raises(TestException) as e:
        join_game(user, game_id)


def test_that_people_joining_aving_an_username_that_contains_non_alphanumerics_still_results_in_an_error():
    game_id = create_game(User("neobservateur"))
    user = User("Я брат русского пирата")

    with pytest.raises(TestException) as e:
        join_game(user, game_id)


def test_that_people_joining_aving_a_too_long_username_still_results_in_an_error():
    game_id = create_game(User("neordre"))
    user = User("Les tests unitaires sont généralement effectués pendant la phase de développement des applications mobiles ou logicielles. Ces tests sont normalement effectués par les développeurs, bien qu’à toutes fins pratiques, ils puissent également être effectués par les responsables en assurance QA.")

    with pytest.raises(TestException) as e:
        join_game(user, game_id)

###############################################################################
#                                                                             #
#                                                                             #
#                             /api/v1/startGame                               #
#                                                                             #
#                                                                             #
###############################################################################
#
# Cette requete crée les données necessaire au bon fonctionnement du jeu,
# c'est a dire qu'elle choisit les personnages, leurs reactions ainsi que leurs
# reponses et les stoquent dans sa memoire en attendant que les clients les
# recuperent


def test_that_people_can_start_a_game():
    owner = User("neAUBERGINE")
    game_id = create_game(owner)
    start_game(owner)


def test_that_a_started_game_cannot_be_started_again():
    owner = User("neosteopathie")
    game_id = create_game(owner)
    start_game(owner)
    with pytest.raises(TestException) as e:
        start_game(owner)


def test_that_non_owners_cant_start_a_game():
    owner = User("neosteopathie")
    notOwner = User("neorphelin")
    game_id = create_game(owner)
    join_game(notOwner, game_id)
    with pytest.raises(TestException) as e:
        start_game(notOwner)


def test_that_someone_with_no_game_cant_start_one():
    owner = User("neosteopathie")
    with pytest.raises(TestException) as e:
        start_game(owner)

###############################################################################
#                                                                             #
#                                                                             #
#                              /api/v1/getGameData                            #
#                                                                             #
#                                                                             #
###############################################################################
#
# Guess the game from the cookie and returns general game data necessary to the
# client to work properly


def test_that_we_can_get_the_data_of_a_started_game():
    owner = User('neo')
    create_game(owner)
    start_game(owner)
    get_game_data(owner)[0]


def test_that_the_game_data_has_all_5_npcs():
    owner = User("one")
    create_game(owner)
    start_game(owner)
    game_data = get_game_data(owner)[0]
    assert len(game_data["npcs"]) == 5


def test_that_each_npc_has_a_name_in_the_game_data():
    owner = User("one")
    create_game(owner)
    start_game(owner)
    game_data = get_game_data(owner)[0]
    for npc_id, npc in game_data["npcs"].items():
        assert npc["name"] is not None
        assert npc["name"] != ""


def test_that_each_npc_has_a_type_0_answer_in_the_game_data():
    owner = User("one")
    create_game(owner)
    start_game(owner)
    game_data = get_game_data(owner)[0]
    for npc_id, npc in game_data["npcs"].items():
        assert npc["QA_0"] is not None
        assert npc["QA_0"] != ""
        assert "{SALLE}" in npc["QA_0"]


def test_that_each_npc_has_a_type_1_answer_in_the_game_data():
    owner = User("one")
    create_game(owner)
    start_game(owner)
    game_data = get_game_data(owner)[0]
    for npc_id, npc in game_data["npcs"].items():
        assert npc["QA_1"] is not None
        assert npc["QA_1"] != ""
        assert "{NPC}" in npc["QA_1"]


def test_that_the_game_data_has_all_rooms():
    owner = User("one")
    create_game(owner)
    start_game(owner)
    game_data = get_game_data(owner)[0]
    assert len(game_data["rooms"]) == 3


def test_that_the_game_data_has_all_questions():
    owner = User("one")
    create_game(owner)
    start_game(owner)
    game_data = get_game_data(owner)[0]
    assert len(game_data["questions"]) == 2
    assert game_data["questions"]["QA_0"] is not None
    assert game_data["questions"]["QA_0"] != ""

    assert game_data["questions"]["QA_1"] is not None
    assert game_data["questions"]["QA_1"] != ""


def test_that_the_game_data_contains_all_traits():
    owner = User("one")
    create_game(owner)
    start_game(owner)
    game_data = get_game_data(owner)[0]
    assert len(game_data["traits"]) == 5
    for trait in game_data["traits"]:
        assert trait is not None
        assert trait != ""


def test_that_a_player_can_get_the_data_of_a_started_game():
    owner = User('neo')
    notOwner = User('oen')
    game_id = create_game(owner)
    join_game(notOwner, game_id)
    start_game(owner)
    get_game_data(notOwner)[0]


def test_that_a_player_as_the_same_data_that_the_creator():
    owner = User('neo')
    notOwner = User('oen')
    game_id = create_game(owner)
    join_game(notOwner, game_id)
    start_game(owner)
    OwnerData,ownerUsername = get_game_data(owner)
    notOwnerData,NotOwnerUsername = get_game_data(notOwner)
    assert OwnerData["game_id"] == notOwnerData["game_id"]
    assert ownerUsername != NotOwnerUsername


###############################################################################
#                                                                             #
#                                                                             #
#                           /api/v1/getGameMembers                            #
#                                                                             #
#                                                                             #
###############################################################################
#
# Guess the game from the cookie and returns the members of that game


def test_that_we_can_get_the_players_of_a_game():
    owner = User('neo')
    game_id = create_game(owner)
    player = User('pasneo')
    join_game(player, game_id)
    get_game_members(game_id)


def test_that_the_creator_of_the_game_is_in_the_game():
    player_name = 'neo'
    owner = User(player_name)
    game_id = create_game(owner)
    members = get_game_members(game_id)
    assert player_name in members


def test_that_players_that_join_are_in_the_game():
    princess_name = 'BlanceNeige'
    princess = User(princess_name)
    dwarfs_names = ["Sneezy", "Sleepy", "Grumpy", "Happy", "Doc", "Dopey", "Bashful"]
    dwarfs = {name: User(name) for name in dwarfs_names}
    game_id = create_game(princess)
    for dwarf in dwarfs.values():
        join_game(dwarf, game_id)
    members = get_game_members(game_id)
    assert princess_name in members
    for name in dwarfs_names:
        assert name in members

###############################################################################
#                                                                             #
#                                                                             #
#                                 /api/v1/isOwner                             #
#                                                                             #
#                                                                             #
###############################################################################
#
# This endpoint it used to know if the username stored in the cookie is the 
# owner of the game


def test_that_the_creator_is_the_owner(): 
    owner = User("neo")
    create_game(owner)
    assert is_owner(owner)
 

def test_that_a_player_is_not_the_owner():
    owner = User("neo")
    notOwner = User("az")
    game_id = create_game(owner)
    join_game(notOwner, game_id)
    assert is_owner(notOwner) is False


def test_that_a_player_calling_is_owner_with_no_game_cant_be_a_owner():
    assert is_owner(User("neoumie")) is False


###############################################################################
#                                                                             #
#                                                                             #
#                               /api/v1/hasJoined                             #
#                                                                             #
#                                                                             #
###############################################################################
#
# Checks the cookie to see if the client is currently in a given game


def test_that_a_client_that_has_not_joined_a_game_has_not_joined_a_game():
    player = User('neo')
    assert has_joined(player) is False


def test_that_a_client_that_has_joined_a_game_has_joined_a_game():
    player = User('neo')
    create_game(player)
    assert has_joined(player) is True
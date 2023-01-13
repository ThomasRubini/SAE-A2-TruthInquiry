import json

import pytest

from truthseeker import APP
test_app = APP.test_client()

class TestException(Exception):
    __test__ = False
   
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

###############################################################################
#                                                                             #
#                                                                             #
#                               Test Classes                                  #
#                                                                             #
#                                                                             #
###############################################################################

class User:
    def __init__(self,username):
        self.username = username
        self.isAdmin = False

def create_game(user:User):
    data = {"username":user.username}
    responseObject = test_app.post("/api/v1/createGame",data=data)
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    user.isAdmin = True
    return content["game_id"]


def join_game(user:User,game_id:str):
    data = {"username":user.username,"game_id":game_id}
    responseObject = test_app.post("/api/v1/joinGame",data=data)
    if responseObject.status_code != 200:
        raise TestException("status code is not 200")
    content = responseObject.json
    if content is None:
        raise TestException("Response is null")
    if content["error"] != 0:
        raise TestException("backend returned an error: "+content["msg"])
    return True

def start_game(user:User):
    responseObject = test_app.post("/api/v1/startGame")
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
# Cette requete api crée une salle de jeu multijoueur dans le serveur, elle 
# octroie ensuite les droit de creation de la salle a l'utilisateur dont le 
# pseudo est donné en parametre post

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
    responseObject = test_app.post("/api/v1/createGame")
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
# Cette requete ajoute dans la partie identifié par l'identifiant de jeu 
# (game_id) l'utilisateur indentifié par son pseudo (username) 

def test_that_people_can_join_a_game():
    game_id = create_game(User("neoracle"))
    assert join_game(User("neobjectif"),game_id) == True

def test_that_two_person_can_join_a_game():
    game_id = create_game(User("neomblic"))
    joueur1_a_join = join_game(User("neobjectif"),game_id)
    joueur2_a_join = join_game(User("neorgane"),game_id)
    assert joueur1_a_join == True and joueur2_a_join == True

def test_that_people_cant_join_if_the_username_is_already_used():
    game_id = create_game(User("neoreille"))
    join_game(User("neosomse"),game_id)
    with pytest.raises(TestException) as e:
        join_game(User("neosomse"),game_id)

def test_that_people_joining_without_sending_any_data_results_in_an_error():
    game_id = create_game(User("neoxyde"))
    responseObject = test_app.post("/api/v1/joinGame")
    assert responseObject.status_code == 200
    assert responseObject.json["error"] != 0

def test_that_people_joining_without_sending_a_game_id_results_in_an_error():
    data={"username":"neomblic"}
    responseObject = test_app.post("/api/v1/joinGame",data=data)
    assert responseObject.status_code == 200
    assert responseObject.json["error"] != 0

def test_that_people_joining_without_sending_an_username_still_results_in_an_error():
    game_id = create_game(User("neonyx"))
    data={"game_id":game_id}
    responseObject = test_app.post("/api/v1/joinGame",data=data)
    assert responseObject.status_code == 200
    assert responseObject.json["error"] != 0

def test_that_people_joining_with_an_empty_username_still_results_in_an_error():
    game_id = create_game(User("neodeur"))
    user = User("")
    
    with pytest.raises(TestException) as e:
        join_game(user,game_id)

def test_that_people_joining_aving_an_username_that_contains_non_alphanumerics_still_results_in_an_error():
    game_id = create_game(User("neobservateur"))
    user = User("Я брат русского пирата")
    
    with pytest.raises(TestException) as e:
        join_game(user,game_id)

def test_that_people_joining_aving_a_too_long_username_still_results_in_an_error():
    game_id = create_game(User("neordre"))
    user = User("Les tests unitaires sont généralement effectués pendant la phase de développement des applications mobiles ou logicielles. Ces tests sont normalement effectués par les développeurs, bien qu’à toutes fins pratiques, ils puissent également être effectués par les responsables en assurance QA.")
    
    with pytest.raises(TestException) as e:
        join_game(user,game_id)


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
    join_game(notOwner,game_id)
    with pytest.raises(TestException) as e:
        start_game(notOwner)

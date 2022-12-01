import requests
import json

###############################################################################
#                                                                             #
#                                                                             #
#                                Constantes                                   #
#                                                                             #
#                                                                             #
###############################################################################

# "scheme" : le protocol a utiliser pour les requette
scheme = "http://"

port = "80"
# "baseUrl" : url racine du serveur web
baseUrl = "truthseeker.simailadjalim.fr"

# 
url= scheme+baseUrl+":"+port


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
        self.JWT =""
        self.isAdmin = False

def createGame(user:User):
    data = {"username":user.username}
    response = requests.post(url+"/api/v1/createGame",data=data)
    if response.status_code != 200:
        return False
    content = json.loads(response.content.decode("utf-8"))
    if content is None:
        return False
    if content["status"] != "ok":
        print(content["status"])
        return False
    user.JWT = content["JWT"]
    user.isAdmin = True
    return content["game_id"]


def joinGame(user:User,game_id:str):
    data = {"username":user.username,"game_id":game_id}
    response = requests.post(url+"/api/v1/joinGame",data=data)
    if response.status_code != 200:
        return False
    content = json.loads(response.content.decode("utf-8"))
    if content is None:
        return False
    if content["status"] != "ok":
        print(content["status"])
        return False
    user.JWT = content["JWT"]
    return True

def startGame(user:User):
    data = {"JWT":user.JWT}
    response = requests.post(url+"/api/v1/startGame",data=data)
    if response.status_code != 200:
        return False
    content = json.loads(response.content.decode("utf-8"))
    if content is None:
        return False
    if content["status"] != "ok":
        print(content["status"])
        return False
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
# pseudo est donné en parametre post et lui retourne son token JWT"

def test_that_people_can_create_a_game():
    user = User("neotaku")
    assert createGame(user) == True

def test_that_two_person_creating_two_games_results_in_two_distincts_game():
    userOne = User("neorage")
    userTwo = User("neobergine")
    gameOne = createGame(userOne)
    gameTwo = createGame(userTwo)
    assert gameOne != gameTwo

def test_that_two_person_having_the_same_pseudo_creating_two_games_results_in_two_distincts_games():
    userOne = User("neo")
    userTwo = User("neo")
    gameOne = createGame(userOne)
    gameTwo = createGame(userTwo)
    assert gameOne != gameTwo
    

def test_that_not_sending_a_username_results_in_an_error():
    response = requests.post(url+"/api/v1/createGame")
    assert response.status_code == 200
    assert json.loads(response.content.decode("utf-8"))["status"] != "ok"
    

def test_that_sending_a_empty_username_results_in_an_error():
    user = User("")
    assert createGame(user) == False

def test_that_a_too_long_username_results_in_an_error():
    user = User("Le test unitaire est un moyen de vérifier qu’un extrait de code fonctionne correctement. C’est l’une des procédures mises en oeuvre dans le cadre d’une méthodologie de travail agile. ")
    assert createGame(user) == False

def test_that_username_that_contains_non_alphanumerics_results_in_an_error():
    user = User("я русский пират")
    assert createGame(user) == False

###############################################################################
#                                                                             #
#                                                                             #
#                              /api/v1/joinGame                               #
#                                                                             #
#                                                                             #
###############################################################################
#
# Cette requete ajoute dans la partie identifié par l'identifiant de jeu 
# (game_id) l'utilisateur indentifié par son pseudo (username) et lui retourne 
# son token JWT 

def test_that_people_can_join_a_game():
    game_id = createGame(User("neoracle"))
    assert joinGame(User("neobjectif"),game_id) == True

def test_that_two_person_can_join_a_game():
    game_id = createGame(User("neomblic"))
    joueur1_a_join = joinGame(User("neobjectif"),game_id)
    joueur2_a_join = joinGame(User("neorgane"),game_id)
    assert joueur1_a_join == True and joueur2_a_join == True

def test_that_people_cant_join_if_the_username_is_already_used():
    game_id = createGame(User("neoreille"))
    joinGame(User("neosomse"),game_id)
    assert joinGame(User("neosomse"),game_id) == False

def test_that_people_joining_without_sending_any_data_results_in_an_error():
    game_id = createGame(User("neoxyde"))
    response = requests.post(url+"/api/v1/joinGame")
    assert response.status_code == 200
    assert json.loads(response.content.decode("utf-8"))["status"] != "ok"

def test_that_people_joining_without_sending_a_game_id_results_in_an_error():
    data={"username":"neomblic"}
    response = requests.post(url+"/api/v1/joinGame",data=data)
    assert response.status_code == 200
    assert json.loads(response.content.decode("utf-8"))["status"] != "ok"

def test_that_people_joining_without_sending_an_username_still_results_in_an_error():
    game_id = createGame(User("neonyx"))
    data={"game_id":game_id}
    response = requests.post(url+"/api/v1/joinGame",data=data)
    assert response.status_code == 200
    assert json.loads(response.content.decode("utf-8"))["status"] != "ok"

def test_that_people_joining_with_an_empty_username_still_results_in_an_error():
    game_id = createGame(User("neodeur"))
    user = User("")
    assert joinGame(user,game_id) == False

def test_that_people_joining_aving_an_username_that_contains_non_alphanumerics_still_results_in_an_error():
    game_id = createGame(User("neobservateur"))
    user = User("Я брат русского пирата")
    assert joinGame(user,game_id) == False

def test_that_people_joining_aving_a_too_long_username_still_results_in_an_error():
    game_id = createGame(User("neordre"))
    user = User("Les tests unitaires sont généralement effectués pendant la phase de développement des applications mobiles ou logicielles. Ces tests sont normalement effectués par les développeurs, bien qu’à toutes fins pratiques, ils puissent également être effectués par les responsables en assurance QA.")
    assert joinGame(user,game_id) == False


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
    owner = User("neosteopathie")
    game_id = createGame(owner)
    assert startGame(owner) == True

def test_that_a_started_game_cannot_be_started_again():
    owner = User("neosteopathie")
    game_id = createGame(owner)
    startGame(owner)
    assert startGame(owner) == False

def test_that_non_owners_cant_start_a_game():
    owner = User("neosteopathie")
    notOwner = User("neorphelin")
    game_id = createGame(owner)
    joinGame(notOwner,game_id)
    assert startGame(notOwner) == False

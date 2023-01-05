import flask

import truthseeker
from truthseeker.logic import game_logic


routes_api = flask.Blueprint("api", __name__)

@routes_api.route("/createGame", methods=["GET", "POST"])
def create_game():
    username = flask.request.values.get("username")
    if username==None:
        return {"status": "error, username not set"}


    response = {}
    response["status"] = "ok"
    game = game_logic.create_game(owner=username)
    response["game_id"] = game.game_id

    flask.session["game_id"] = game.game_id
    flask.session["is_owner"] = True
    flask.session["username"] = username

    return response
    
@routes_api.route("/joinGame", methods=["GET", "POST"])
def join_game():
    game_id = flask.request.values.get("game_id")
    username = flask.request.values.get("username")
    if game_id==None or username==None:
        return {"status": "error, username or game id not set"}

    game = game_logic.get_game(game_id)
    if game == None:
        return {"status": "error, game does not exist"}
    

    game.add_member(username)

    flask.session["game_id"] = game.game_id
    flask.session["is_owner"] = False
    flask.session["username"] = username

    response = {}
    response["status"] = "ok"
    return response
    
@routes_api.route("/startGame", methods=["GET", "POST"])
def start_game():
    if not flask.session:
        return {"status": "No session"}
    if not flask.session["is_owner"]:
        return {"status": "Error, you are not the owner of this game"}
    if game_logic.get_game(flask.session["game_id"]) == None:
        return {"status": "Error, this game doesn't exist"}
    
    return {"status": "ok"}

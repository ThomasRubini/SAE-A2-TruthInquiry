import flask

from truthseeker.logic import game_logic


routes_api = flask.Blueprint("api", __name__)

@routes_api.route("/createGame")
def create_game():
    username = flask.request.args.get("username")
    if username==None:
        return {"status": "error, username not set"}


    response = {}
    response["status"] = "ok"
    game = game_logic.create_game()
    response["game_id"] = game.game_id
    owner, owner_jwt = game.set_owner(username=username)
    response["jwt"] = owner_jwt
    return response
    
@routes_api.route("/joinGame")
def join_game():
    game_id = flask.request.args.get("game_id")
    username = flask.request.args.get("username")
    if game_id==None or username==None:
        return {"status": "error, username or game id not set"}

    game = game_logic.get_game(game_id)
    if game == None:
        return {"status": "error, game does not exist"}
    
    member, member_jwt = game.add_member(username)

    response = {}
    response["status"] = "ok"
    response["jwt"] = member_jwt
    return response

@routes_api.route("/getGameInfo")
def get_game_info(): # DEPRECATED, SHOULD BE REMOVED
    response = {}
    game_id = flask.request.args.get("game_id")
    if game_id == None:
        response["status"] = "No 'game_id' argument"
        return response 
    game = game_logic.get_game_info(game_id)
    if game == None:
        response["status"] = "Game {} does not exist".format(game_id)
        return response 
    else:
        response["status"] = "ok"
        response["game_id"] = game_id
        response["token"] = game.start_token
        return response
    
@routes_api.route("/needJwt")
def get_game_info(): # DEPRECATED, SHOULD BE REMOVED

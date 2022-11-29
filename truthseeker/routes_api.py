import flask

from truthseeker import game_functions

api_routes = flask.Blueprint("api", __name__)

@api_routes.route("/createGame")
def create_game():
    username = flask.request.args.get("username")
    if username==None:
        response = {}
        return {"status": "error, username not set"}


    response = {}
    response["status"] = "ok"
    game = game_functions.create_game()
    response["game_id"] = game.id
    response["jwt"] = game.gen_jwt(username=username, owner=True)
    return response
    
@api_routes.route("/getGameInfo")
def get_game_info():
    response = {}
    game_id = flask.request.args.get("game_id")
    if game_id == None:
        response["status"] = "No 'game_id' argument"
        return response 
    game = game_functions.get_game_info(game_id)
    if game == None:
        response["status"] = "Game {} does not exist".format(game_id)
        return response 
    else:
        response["status"] = "ok"
        response["game_id"] = game_id
        response["token"] = game.start_token
        return response
    

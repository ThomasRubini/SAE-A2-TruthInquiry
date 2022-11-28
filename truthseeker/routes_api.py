import flask

from truthseeker import game_api

api_routes = flask.Blueprint("api", __name__)

@api_routes.route("/createGame")
def create_game():
    response = {}
    response["status"] = "ok"
    response["gameId"] = game_api.create_game().id
    return response
    
@api_routes.route("/getGameInfo")
def get_game_info():
    response = {}
    gameid = flask.request.args.get("gameid")
    if gameid == None:
        response["status"] = "No 'gameid' argument"
        return response 
    game = game_api.get_game_info(gameid)
    if game == None:
        response["status"] = "Game {} does not exist".format(gameid)
        return response 
    else:
        response["status"] = "ok"
        response["gameid"] = gameid
        response["token"] = game.start_token
        return response
    

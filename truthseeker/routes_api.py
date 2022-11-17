import flask

from truthseeker import game_api

api_routes = flask.Blueprint("api", __name__)

@api_routes.route("/createGame")
def create_game():
    return "Created game {}".format(game_api.create_game().id)
    
@api_routes.route("/getGameInfo")
def get_game_info():
    gameid = flask.request.args.get("gameid")
    if gameid == None:
        return "No 'gameid' argument"
    game = game_api.get_game_info(gameid)
    if game == None:
        return "Game {} does not exist".format(gameid)
    else:
        return "Game {} start token : {}".format(gameid, game.start_token)
    

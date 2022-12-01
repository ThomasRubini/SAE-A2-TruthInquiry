import flask
import jwt

import truthseeker
from truthseeker.logic import game_logic
from functools import wraps


routes_api = flask.Blueprint("api", __name__)

# Auth decorator
def jwt_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        jwt_str = flask.request.args.get("jwt")
        if not jwt_str:
            return {"status": "Error, JWT token missing"}

        try:
            claims = jwt.decode(jwt_str, truthseeker.app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError as e:
            print("Caught exception while decoding JWT token :", e)
            return {"status": "Error, invalid JWT"}

        return f(claims, *args, **kwargs)
    return decorator
        
            



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
    
@routes_api.route("/startGame")
@jwt_required
def start_game(claims):
    if not claims["owner"]:
        return {"status": "Error, you are not the owner of this game"}
    
    if game_logic.get_game(claims["game_id"]) == None:
        return {"status": "Error, this game doesn't exist"}
    
    return {"status": "ok"}

import flask
import json
from truthseeker import APP
from truthseeker.logic import game_logic
from truthseeker.utils import check_username


routes_api = flask.Blueprint("api", __name__)

@routes_api.route("/createGame", methods=["GET", "POST"])
def create_game():
    username = flask.request.values.get("username")
    if username==None:
        return {"error": 1, "msg": "username not set"}
    if not check_username(username):
        return {"error": 1, "msg": "invalid username"}

    response = {}
    response["error"] = 0
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
        return {"error": 1, "msg": "username or game id not set"}
    if not check_username(username):
        return {"error": 1, "msg": "invalid username"}

    game = game_logic.get_game(game_id)
    if game == None:
        return {"error": 1, "msg": "game does not exist"}
    
    if not game.add_member(username):
        return {"error": 1, "msg": f"Username '{username}' already used in game {game.game_id}"}

    flask.session["game_id"] = game.game_id
    flask.session["is_owner"] = False
    flask.session["username"] = username

    APP.socketio_app.emit("playersjoin", [flask.session["username"]], room="game."+game.game_id)

    return {"error": 0}
    
@routes_api.route("/startGame", methods=["GET", "POST"])
def start_game():
    if not flask.session:
        return {"error": 1, "msg": "No session"}
    if not flask.session["is_owner"]:
        return {"error": 1, "msg": "you are not the owner of this game"}
    game = game_logic.get_game(flask.session["game_id"])
    if game == None:
        return {"error": 1, "msg": "this game doesn't exist"}
    if game.has_started:
        return {"error": 1, "msg": "this game is already started"}
    game.generate_data()
    game.has_started = True
    APP.socketio_app.emit("gamestart", {}, room="game."+game.game_id)
    return {"error": 0}

@routes_api.route("/getGameData", methods=["GET", "POST"])
def get_data():
    if not flask.session:
        return {"error": 1, "msg": "No session"}
    game = game_logic.get_game(flask.session["game_id"])
    if game == None:
        return {"error": 1, "msg": "this game doesn't exist"}
    
    response = {}
    response["error"] = 0
    response["gamedata"] = game.gamedata
    return response

@routes_api.route("/getNpcImage", methods=["GET", "POST"])
def getNpcImage():
    npc_id = flask.request.values.get("npcid")
    image = game_logic.get_npc_image(npc_id)
    
    response = flask.make_response(image)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename=f'0.png')
    return response

@routes_api.route("/getNpcReaction", methods=["GET", "POST"])
def getNpcReaction():

    if not flask.session:
        return {"error": 1, "msg": "No session"}
    game = game_logic.get_game(flask.session["game_id"])
    if game == None:
        return {"error": 1, "msg": "this game doesn't exist"}
    npc_id = flask.request.values.get("npcid")
    reactionid = flask.request.values.get("reactionid")
    image = game.get_npc_reaction(npc_id,reactionid)

    errors = ["npc not in game","error reading file"]
    if image in [0,1]:
        return {"error" :1, "msg": errors[image]} , 500
    
    response = flask.make_response(image)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename=f'{reactionid}.png')
    return response

@routes_api.route("/gameProgress", methods=["GET", "POST"])
def gameProgress():
    if not flask.session:
        return {"error": 1, "msg": "No session"}
    game = game_logic.get_game(flask.session["game_id"])
    
    if game == None:
        return {"error": 1, "msg": "this game doesn't exist"}
    
    username = flask.session["username"]
    game.get_member(username).progress += 1
    
    APP.socketio_app.emit("gameprogress", [flask.session["username"]], room="game."+game.game_id)
    if game.has_finished() : APP.socketio_app.emit("gamefinshed",room="game."+game.game_id)
    
    return {"error": 0}

@routes_api.route("/submitAnswers", methods=["GET", "POST"])
def checkAnwser():
    if not flask.session:
        return {"error": 1, "msg": "No session"}
    game = game_logic.get_game(flask.session["game_id"])

    if game == None:
        return {"error": 1, "msg": "this game doesn't exist"}

    member = game.get_member(flask.session["username"])

    if member.has_submitted == True:
        return {"error": 1, "msg": "answers already submitted for this member"}

    playerResponses = flask.request.values.get("responses")

    if playerResponses == None:
        return {"error": 1, "msg": "no responses were sent"}
    results = game.getPlayerResults(json.loads(playerResponses))
    if results == False:
        return {"error": 1, "msg": "invalid npc sent"}
        
    response = {"error": 0}
    member.has_submitted = True
    response["results"] = results
    return response

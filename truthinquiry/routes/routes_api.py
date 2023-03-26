import json
import io

import flask
from sqlalchemy import select

from truthinquiry.ext.database.models import *
from truthinquiry.ext.database.fsa import db
from truthinquiry.ext.discord_bot import discord_bot
from truthinquiry.ext.socketio import socket_io
from truthinquiry.logic import game_logic


routes_api = flask.Blueprint("api", __name__)

# API specification is documented in api_doc.yml

@routes_api.route("/createGame", methods=["GET", "POST"])
def create_game():
    username = flask.request.values.get("username")
    if username is None:
        return {"error": 1, "msg": "username not set"}
    if not game_logic.check_username(username):
        return {"error": 1, "msg": "invalid username"}

    response = {}
    response["error"] = 0
    game = game_logic.create_game(owner=username)
    response["game_id"] = game.game_id

    flask.session["game_id"] = game.game_id
    flask.session["is_owner"] = True
    flask.session["username"] = username

    discord_bot.update_games_presence()

    return response

@routes_api.route("/getGameMembers", methods=["GET", "POST"])
def get_members():
    game_id = flask.request.values.get("game_id")
    game = game_logic.get_game(game_id)
    if game is None:
        return {"error": 1, "msg": "this game doesn't exist"}
    response = {"error" : 0}
    player_list = [member.username for member in game.members]
    response["members"] = player_list
    return response

@routes_api.route("/joinGame", methods=["GET", "POST"])
def join_game():
    game_id = flask.request.values.get("game_id")
    username = flask.request.values.get("username")
    if game_id is None or username is None:
        return {"error": 1, "msg": "username or game id not set"}
    if not game_logic.check_username(username):
        return {"error": 1, "msg": "invalid username"}

    game = game_logic.get_game(game_id)
    if game is None:
        return {"error": 1, "msg": "game does not exist"}

    if not game.add_member(username):
        return {"error": 1, "msg": f"Username '{username}' already used in game {game.game_id}"}

    flask.session["game_id"] = game.game_id
    flask.session["is_owner"] = False
    flask.session["username"] = username

    socket_io.emit("playersjoin", [flask.session["username"]], room="game."+game.game_id)

    return {"error": 0}

@routes_api.route("/isOwner", methods=["GET", "POST"])
def is_owner():
    if not flask.session:
        return {"error": 0, "owner": False}
    game = game_logic.get_game(flask.session["game_id"])
    if game is None:
        return {"error": 0, "owner": False}

    if not flask.session["is_owner"]:
        return {"error": 0, "owner": False}

    return {"error": 0, "owner": True}

@routes_api.route("/hasJoined", methods=["GET", "POST"])
def has_joined():
    if not flask.session:
        return {"error": 0, "joined": False}
    game = game_logic.get_game(flask.session["game_id"])
    if game is None:
        return {"error": 0, "joined": False}
    return {"error": 0, "joined": True}

@routes_api.route("/startGame", methods=["GET", "POST"])
def start_game():
    if not flask.session:
        return {"error": 1, "msg": "No session"}
    if not flask.session["is_owner"]:
        return {"error": 1, "msg": "you are not the owner of this game"}
    game = game_logic.get_game(flask.session["game_id"])
    if game is None:
        return {"error": 1, "msg": "this game doesn't exist"}
    if game.has_started:
        return {"error": 1, "msg": "this game is already started"}
    game.generate_data()
    game.has_started = True
    socket_io.emit("gamestart", {}, room="game."+game.game_id)
    return {"error": 0}

@routes_api.route("/getGameData", methods=["GET", "POST"])
def get_data():
    if not flask.session:
        return {"error": 1, "msg": "No session"}
    game = game_logic.get_game(flask.session["game_id"])
    if game is None:
        return {"error": 1, "msg": "this game doesn't exist"}

    response = {}
    response["error"] = 0
    response["gamedata"] = game.gamedata
    response["username"] = flask.session["username"]

    return response

@routes_api.route("/getNpcImage", methods=["GET", "POST"])
def get_npc_image():
    npc_id = int(flask.request.values.get("npcid"))
    if npc_id is None:
        return {"error": 1, "msg": "no npc was given"}
    image = game_logic.get_npc_image(npc_id)
    if image is None:
        return {"error": 1, "msg": "npc not found"}
    response = flask.make_response(image)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='0.png')
    return response

@routes_api.route("/getNpcReaction", methods=["GET", "POST"])
def get_npc_reaction():

    if not flask.session:
        return {"error": 1, "msg": "No session"}
    game = game_logic.get_game(flask.session["game_id"])
    if game is None:
        return {"error": 1, "msg": "this game doesn't exist"}
    npc_id = flask.request.values.get("npcid")

    image = game.get_npc_reaction(npc_id)
    if image == None:
        return {"error": 1, "msg": "npc not in game"}

    response = flask.make_response(image)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='reaction.png')
    return response

@routes_api.route("/getReaction", methods=["GET", "POST"])
def get_reaction():
    input_uuid = flask.request.values.get("uuid")
    results = db.session.execute(select(Reaction).where(Reaction.REACTION_UUID==uuid.UUID(input_uuid)))
    
    row = results.first()
    if row == None:
        return {"error": 1, "msg": "No such reaction"}
    reaction_obj = row[0]

    return flask.send_file(io.BytesIO(reaction_obj.IMG), mimetype='image/png')
    



@routes_api.route("/gameProgress", methods=["GET", "POST"])
def game_progress():
    if not flask.session:
        return {"error": 1, "msg": "No session"}
    game = game_logic.get_game(flask.session["game_id"])

    if game is None:
        return {"error": 1, "msg": "this game doesn't exist"}

    username = flask.session["username"]
    game.get_member(username).progress += 1

    socket_io.emit("gameprogress", [flask.session["username"]], room="game."+game.game_id)

    return {"error": 0}


@routes_api.route("/submitAnswers", methods=["GET", "POST"])
def check_anwser():
    if not flask.session:
        return {"error": 1, "msg": "No session"}
    game = game_logic.get_game(flask.session["game_id"])

    if game is None:
        return {"error": 1, "msg": "this game doesn't exist"}

    member = game.get_member(flask.session["username"])

    if member.results is not None:
        return {"error": 1, "msg": "answers already submitted for this member"}

    player_responses = flask.request.values.get("responses")

    if player_responses is None:
        return {"error": 1, "msg": "no responses were sent"}

    results = game.get_player_results(json.loads(player_responses))
    if results is False:
        return {"error": 1, "msg": "invalid npc sent"}

    member.has_submitted = True
    member.results = results
    if game.has_finished():
        json_game_results = game.generate_game_results()
        socket_io.emit("gamefinished", json_game_results, room="game."+game.game_id)
        del game
    response = {"error": 0}
    return response

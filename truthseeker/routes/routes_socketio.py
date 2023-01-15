import socketio

from flask_socketio import join_room

from truthseeker import APP
from truthseeker.logic import game_logic


@APP.socketio_app.on('connect')
def connect(auth):
    if not (auth and "game_id" in auth):
        raise socketio.exceptions.ConnectionRefusedError("Invalid connection data passed")

    game = game_logic.get_game(auth["game_id"])
    if not game:
        raise socketio.exceptions.ConnectionRefusedError("No game with this ID")

    room = join_room("game."+auth["game_id"])
    join_room(room)

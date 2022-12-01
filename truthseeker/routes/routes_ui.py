import flask

from truthseeker.logic import game_logic


routes_ui = flask.Blueprint("ui", __name__)

@routes_ui.route("/")
def index():
    return flask.render_template("index.html")

@routes_ui.route("/lobby/<game_id>")
def lobby(game_id):
    # rendered by the javascript client-side
    return flask.render_template("lobby.html")

@routes_ui.route("/solo")
def solo():
    return flask.render_template("game.html")

@routes_ui.route("/multi")
def multi():
    return flask.render_template("game.html")

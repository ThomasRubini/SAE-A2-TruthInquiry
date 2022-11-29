import flask

from truthseeker.logic import game_logic


routes_ui = flask.Blueprint("ui", __name__)

@routes_ui.route("/")
def hello():
    return "Hello World!"

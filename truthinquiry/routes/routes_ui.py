import os

import flask

routes_ui = flask.Blueprint("ui", __name__)


@routes_ui.route("/")
def index():
    return flask.render_template("index.html")


@routes_ui.route("/privacy")
def privacy():
    return flask.render_template("privacy.html")


@routes_ui.route("/licenses")
def licenses():
    return flask.render_template("licenses.html")


@routes_ui.route("/legal")
def legal():
    hosting_info = os.getenv("HOSTING_INFO")
    return flask.render_template("legal.html", hosting_info=hosting_info)

@routes_ui.route("/docs")
def doc():
    return flask.render_template("doc.html")

@routes_ui.route("/lobby")
def lobbyRedirect():
    return flask.redirect("/")


@routes_ui.route("/lobby/<game_id>")
def lobby(game_id):
    # rendered by the javascript client-side
    if game_id is None:
        return flask.redirect("")
    return flask.render_template("lobby.html", gameid=game_id)


@routes_ui.route("/solo")
def solo():
    return flask.render_template("game.html")


@routes_ui.route("/multi")
def multi():
    return flask.render_template("game.html")

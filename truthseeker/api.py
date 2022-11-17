import flask
api_routes = flask.Blueprint("api", __name__)

@api_routes.route("/newGame")
def hello():
    return "Created new game"

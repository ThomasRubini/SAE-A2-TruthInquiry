import flask

routes_admin = flask.Blueprint("admin", __name__)

@routes_admin.route("/")
def index():
    return flask.render_template("admin/index.html")

@routes_admin.route("/npc/<npc_id>")
def npc(npc_id):
    return flask.render_template("admin/npc.html")

@routes_admin.route("/questions")
def questions():
    return flask.render_template("admin/questions.html", langs=["FR", "EN"])

@routes_admin.route("/places")
def places():
    return flask.render_template("admin/places.html")

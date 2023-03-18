import flask

from truthinquiry.ext.database.models import *
from truthinquiry.ext.database.fsa import db

routes_admin = flask.Blueprint("admin", __name__)

@routes_admin.route("/")
def index():
    npcs_objs = db.session.query(Npc).all()
    npcs_dicts = [{"id": npc_obj.NPC_ID, "name": npc_obj.LOCALE.TEXTS[0].TEXT} for npc_obj in npcs_objs]
    return flask.render_template("admin/index.html", npcs=npcs_dicts)

@routes_admin.route("/npc/<npc_id>")
def npc(npc_id):
    if npc_id == "new":
        return flask.render_template("admin/npc.html", npc={})
    else:
        npc_obj = db.session.get(Npc, npc_id)

        npc_answers = []
        for answer_type in npc_obj.ANSWERS:
            answer_list = [answer.TEXT for answer in answer_type.LOCALE.TEXTS]
            npc_answers.append(answer_list)
        
        npc_dict = {
            "name": npc_obj.LOCALE.TEXTS[0].TEXT,
            "img": npc_obj.NPC_ID,
            "answers": npc_answers,
        }

        return flask.render_template("admin/npc.html", npc=npc_dict)

@routes_admin.route("/questions")
def questions():
    return flask.render_template("admin/questions.html", langs=["FR", "EN"])

@routes_admin.route("/places")
def places():
    return flask.render_template("admin/places.html")

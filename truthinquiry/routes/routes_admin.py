import flask
from sqlalchemy import select, or_

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
    lang = "FR"

    results = db.session.execute(
        select(QuestionType, Text)
        .select_from(QuestionType)
        .join(Locale)
        .join(Text, isouter=True)
        .filter(or_(Text.LANG==None, Text.LANG==lang))
        .order_by(QuestionType.QUESTION_TYPE_ID)
    )

    data = []
    old_question_type_id = None

    for question_type, locale in results:
        if question_type.QUESTION_TYPE_ID != old_question_type_id:
            old_question_type_id = question_type.QUESTION_TYPE_ID
            data.append({"questions": []})

        if locale:
            data[-1]["questions"].append({"text": locale.TEXT})
    
    return flask.render_template("admin/questions.html", questions=data, langs=["FR", "EN"])

@routes_admin.route("/places")
def places():
    places_objs = db.session.query(Place).all()
    places_dicts = [{"id": place_obj.PLACE_ID, "name": place_obj.LOCALE.TEXTS[0].TEXT} for place_obj in places_objs]
    return flask.render_template("admin/places.html", places=places_dicts)

@routes_admin.route("/traits")
def traits():
    traits_objs = db.session.query(Trait).all()
    traits_dicts = [{"id": trait_obj.TRAIT_ID, "name": trait_obj.Name.TEXTS[0].TEXT, "desc": trait_obj.Desc.TEXTS[0].TEXT} for trait_obj in traits_objs]
    return flask.render_template("admin/traits.html", traits=traits_dicts)

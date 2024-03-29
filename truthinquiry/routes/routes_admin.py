import flask
from sqlalchemy import select, or_

from truthinquiry.ext.database.models import *
from truthinquiry.ext.database.fsa import db
from truthinquiry.utils import require_admin


routes_admin = flask.Blueprint("admin", __name__)

DEFAULT_LANG = "FR"

@routes_admin.route("/")
@require_admin(ui=True)
def index():
    npcs_objs = db.session.query(Npc).all()
    npcs_dicts = [{"id": npc_obj.NPC_ID, "name": npc_obj.NAME_LOCALE.get_text(DEFAULT_LANG).TEXT} for npc_obj in npcs_objs]
    return flask.render_template("admin/index.html", npcs=npcs_dicts)

@routes_admin.route("/auth")
def auth():
    input_failed = bool(flask.request.values.get("failed"))
    return flask.render_template("admin/auth.html", failed=input_failed)

@routes_admin.route("/npc/<npc_id>")
@require_admin(ui=True)
def npc(npc_id):
    if npc_id == "new":
        return flask.render_template("admin/npc.html", npc={})
    else:
        npc_obj = db.session.get(Npc, npc_id)

        npc_answers = []
        for answer_type in npc_obj.ANSWERS:
            answer_list = [answer.TEXT for answer in answer_type.TEXT_LOCALE.TEXTS]
            npc_answers.append(answer_list)
        
        reactions = [{
            "trait_id": reaction.TRAIT.TRAIT_ID,
            "name": reaction.TRAIT.NAME_LOCALE.get_text(DEFAULT_LANG).TEXT,
            "url": "/api/v1/getReaction?uuid="+reaction.REACTION_UUID
        } for reaction in npc_obj.REACTIONS]

        reactions_to_add = []
        for trait in db.session.query(Trait).all():
            if trait.TRAIT_ID not in [reaction.TRAIT.TRAIT_ID for reaction in npc_obj.REACTIONS]:
                reactions_to_add.append({
                    "trait_id": trait.TRAIT_ID,
                    "name": trait.NAME_LOCALE.get_text(DEFAULT_LANG).TEXT
                })

        npc_dict = {
            "id": npc_obj.NPC_ID,
            "name": npc_obj.NAME_LOCALE.get_text(DEFAULT_LANG).TEXT,
            "img": npc_obj.NPC_ID,
            "answers": npc_answers,
            "reactions": reactions,
            "reactions_to_add": reactions_to_add,
        }

        return flask.render_template("admin/npc.html", npc=npc_dict)

@routes_admin.route("/questions")
@require_admin(ui=True)
def questions():
    lang = DEFAULT_LANG

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
@require_admin(ui=True)
def places():
    lang = DEFAULT_LANG

    places_objs = db.session.query(Place).all()
    places_dicts = [{"id": place_obj.PLACE_ID, "name": place_obj.NAME_LOCALE.get_text(lang).TEXT} for place_obj in places_objs]
    return flask.render_template("admin/places.html", places=places_dicts)

@routes_admin.route("/traits")
@require_admin(ui=True)
def traits():
    lang = DEFAULT_LANG

    traits_objs = db.session.query(Trait).all()
    traits_dicts = [{"id": trait_obj.TRAIT_ID, "name": trait_obj.NAME_LOCALE.get_text(lang).TEXT, "desc": trait_obj.DESC_LOCALE.get_text(lang).TEXT} for trait_obj in traits_objs]
    return flask.render_template("admin/traits.html", traits=traits_dicts)

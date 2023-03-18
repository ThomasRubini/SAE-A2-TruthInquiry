import flask
from sqlalchemy import select, delete, or_

from truthinquiry.ext.database.models import *
from truthinquiry.ext.database.fsa import db


routes_api_admin = flask.Blueprint("api_admin", __name__)

@routes_api_admin.route("/getQuestions", methods=["GET", "POST"])
def get_questions():
    lang = flask.request.values.get("lang")
    if lang is None:
        return {"error": 1, "msg": "lang not set"}


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
            data.append([])

        if locale:
            data[-1].append({"text": locale.TEXT})
    
    return data

@routes_api_admin.route("/setQuestions", methods=["GET", "POST"])
def set_questions():
    if not flask.request.json:
        return {"error": 1, "msg": "no json set"}
    lang = flask.request.json["lang"]
    question_types = flask.request.json["questions"]

    # Delete old questions
    text_ids_requ = (
        select(Locale.LID)
        .join(Text).where(Text.LANG==lang)
        .join(QuestionType)
    )
    db.session.execute(
        delete(Text)
        .where(Text.LID.in_(text_ids_requ.subquery()))
    )
    
    # get question LIDs in database
    question_lids_requ = (
        select(QuestionType.TEXT_LID)
        .join(Locale)
    )
    question_lids = (data[0] for data in db.session.execute(question_lids_requ))

    # set new questions 
    text_obs = []
    for question_lid, questions in zip(question_lids, question_types):
        for question in questions:
            text_obs.append(Text(None, question_lid, lang, question["text"]))

    db.session.add_all(text_obs)
    db.session.commit()

    return {"error": 0}

@routes_api_admin.route("/setTraits", methods=["GET", "POST"])
def set_traits():
    input_lang = flask.request.json["lang"]
    input_traits = flask.request.json["traits"]


    db_traits = db.session.query(Trait).all()
    
    modified_db_traits = []
    for input_trait in input_traits:
        if input_trait["id"]:
            # modify
            db_trait = list(filter(lambda db_trait: db_trait.TRAIT_ID == int(input_trait["id"]), db_traits))[0]
            
            db.session.delete(db_trait.Name.TEXTS[0])
            db.session.delete(db_trait.Desc.TEXTS[0])
            db_trait.Name.TEXTS = [Text(None, None, input_lang, input_trait["name"])]
            db_trait.Desc.TEXTS = [Text(None, None, input_lang, input_trait["desc"])]
            
            db.session.add(db_trait)
            modified_db_traits.append(db_trait)
        else:
            # add
            new_trait = Trait(None, None, None)
            
            new_trait.Name = Locale(None)
            new_trait.Desc = Locale(None)

            new_trait.Name.TEXTS.append(Text(None, None, input_lang, input_trait["name"]))
            new_trait.Desc.TEXTS.append(Text(None, None, input_lang, input_trait["desc"]))
            
            db.session.add(new_trait)

    # delete
    for db_trait in db_traits:
        if db_trait not in modified_db_traits:
            db.session.delete(db_trait)

    db.session.commit()

    return {"error": 0}

@routes_api_admin.route("/setPlaces", methods=["GET", "POST"])
def set_places():
    input_lang = flask.request.json["lang"]
    input_places = flask.request.json["places"]


    db_places = db.session.query(Place).all()
    
    modified_db_places = []
    for input_place in input_places:
        if input_place["id"]:
            # modify
            db_place = list(filter(lambda db_place: db_place.PLACE_ID == int(input_place["id"]), db_places))[0]
            
            db.session.delete(db_place.LOCALE.TEXTS[0])
            
            db_place.LOCALE.TEXTS = [Text(None, None, input_lang, input_place["name"])]
            
            db.session.add(db_place)
            modified_db_places.append(db_place)
        else:
            # add
            new_place = Place(None, None)
            
            new_place.LOCALE = Locale(None)
            new_place.LOCALE.TEXTS = [Text(None, None, input_lang, input_place["name"])]
            
            db.session.add(new_place)

    # delete
    for db_place in db_places:
        if db_place not in modified_db_places:
            db.session.delete(db_place)

    db.session.commit()

    return {"error": 0}
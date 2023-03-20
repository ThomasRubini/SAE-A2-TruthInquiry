import flask
from sqlalchemy import select, delete, or_

from truthinquiry.ext.database.models import *
from truthinquiry.ext.database.fsa import db


routes_api_admin = flask.Blueprint("api_admin", __name__)

@routes_api_admin.route("/setQuestions", methods=["GET", "POST"])
def set_questions():
    if not flask.request.json:
        return {"error": 1, "msg": "no json set"}
    lang = flask.request.json["lang"]
    all_questions = flask.request.json["questions"]

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
    for question_lid, questionType in zip(question_lids, all_questions):
        for question in questionType["questions"]:
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
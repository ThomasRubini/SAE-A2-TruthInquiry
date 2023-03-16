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

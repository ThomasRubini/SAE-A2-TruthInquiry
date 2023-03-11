import flask
from sqlalchemy import select

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
        .join(Text)
        .filter(Text.LANG==lang)
        .order_by(QuestionType.QUESTION_TYPE_ID)
    )

    data = []
    old_question_type_id = None

    for question_type, locale in results:
        if question_type.QUESTION_TYPE_ID != old_question_type_id:
            old_question_type_id = question_type.QUESTION_TYPE_ID
            data.append([])

        data[-1].append({"text": locale.TEXT})
    
    return data

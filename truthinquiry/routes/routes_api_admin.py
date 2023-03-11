import flask
from sqlalchemy import select

from truthinquiry.ext.database.models import *
from truthinquiry.ext.database.fsa import db


routes_api_admin = flask.Blueprint("api_admin", __name__)

@routes_api_admin.route("/getQuestions", methods=["GET", "POST"])
def get_questions():
    pass
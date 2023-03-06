import os
import random

from sqlalchemy import engine as eg
from flask_sqlalchemy import SQLAlchemy

class Database(SQLAlchemy):
    def __init__(self):
        super().__init__()

    def init_app(self, app):

        db_url = eg.URL.create(
            "mariadb+pymysql",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DBNAME")
        )
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
        
        super().init_app(app)

        with app.app_context():
            self.create_all()

db = Database()

class Locale(db.Model):
    """
    Stores the different texts needed by the other tables in multiple languages
    """

    __tablename__ = 'T_LOCALE'
    TEXT_ID = db.Column(db.Integer, primary_key=True, comment="ID of this text (the other tables references to this with *_LID columns)")
    LANG = db.Column(db.VARCHAR(2), primary_key=True, comment="lang ID of the text value in this row, e.g FR, EN, ES")
    TEXT = db.Column(db.Text, comment="Actual text stored for that text ID and lang")

    def __init__(self, TEXT_ID, LANG, TEXT):
        self.TEXT_ID = TEXT_ID
        self.LANG = LANG
        self.TEXT = TEXT

    def __str__(self):
        return f"{self.TEXT_ID}  {self.LANG} {self.TEXT}"


class Place(db.Model):
    """
    Store litteral places, could be a room in the manor or near it
    """

    __tablename__ = 'T_PLACE'
    PLACE_ID = db.Column(db.Integer, primary_key=True, comment="ID of this place")
    NAME_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"), comment="Place name")
    LOCALE = db.relationship("Locale")

    def __init__(self, PLACE_ID, NAME_LID):
        self.PLACE_ID = PLACE_ID
        self.NAME_LID = NAME_LID

    def __str__(self):
        return f"{self.PLACE_ID} {self.NAME_LID}"


class Question(db.Model):
    """
    Stores questions asked by players
    """

    __tablename__ = "T_QUESTION"
    QUESTION_ID = db.Column(db.Integer, primary_key=True, comment="ID of this question")
    QUESTION_TYPE = db.Column(db.Integer, comment="Question type ID, e.g 'when..', 'where..'")
    TEXT_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"), comment="Question text")
    LOCALE = db.relationship("Locale")

    def __init__(self, QUESTION_ID, QUESTION_TYPE, TEXT_LID):
        self.QUESTION_ID = QUESTION_ID
        self.QUESTION_TYPE = QUESTION_TYPE
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"{self.QUESTION_ID} {self.QUESTION_TYPE} {self.TEXT_LID}"


class Answer(db.Model):
    """
    Stores answers given by NPCs
    They are relative to the question type ID, and NPC ID
    """

    __tablename__ = "T_ANSWER"
    ANSWER_ID = db.Column(db.Integer, primary_key=True, comment="ID of this answer")
    QA_TYPE = db.Column(db.Integer, comment="Question type ID")
    NPC_ID = db.Column(db.Integer, db.ForeignKey("T_NPC.NPC_ID"), comment="ID of the NPC that will say this answer")
    TEXT_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"), comment="Text of the answer")
    LOCALE = db.relationship("Locale")
    NPC = db.relationship("Npc")

    def __init__(self, ANSWER_ID, QA_TYPE, NPC_ID, TEXT_LID):
        self.ANSWER_ID = ANSWER_ID
        self.QA_TYPE = QA_TYPE
        self.NPC_ID = NPC_ID
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"{self.ANSWER_ID} {self.QA_TYPE} {self.NPC_ID} {self.TEXT_LID}"


class Npc(db.Model):
    """
    Store Npcs
    """

    __tablename__ = "T_NPC"
    NPC_ID = db.Column(db.Integer, primary_key=True, comment="ID of this Npc")
    NAME_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"), comment="Name of this Npc")
    LOCALE = db.relationship("Locale")

    def __init__(self, NPC_ID, NAME_LID):
        self.NPC_ID = NPC_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"{self.NPC_ID} {self.NAME_LID}"


class Trait(db.Model):
    """
    Store reaction types, e.g 'happy', 'sad', without relation with NPCs
    """
    __tablename__ = "T_TRAIT"
    TRAIT_ID = db.Column(db.Integer, primary_key=True, comment="ID of this trait")
    NAME_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"), comment="Name of this trait")
    DESC_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"), comment="Description of this trait")

    Name = db.relationship("Locale",foreign_keys=[NAME_LID])
    Desc = db.relationship("Locale",foreign_keys=[DESC_LID])


    def __init__(self, TRAIT_ID, NAME_LID):
        self.TRAIT_ID = TRAIT_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"{self.TRAIT_ID} {self.NAME_LID}"


class Reaction(db.Model):
    """
    Relation between a NPC and a Trait
    """
    __tablename__ = "T_REACTION"
    REACTION_ID = db.Column(db.Integer, primary_key=True, comment="ID of this reaction")
    NPC_ID = db.Column(db.Integer, db.ForeignKey("T_NPC.NPC_ID"), primary_key=True, comment="Name of the NPC that will have this reaction")
    TRAIT_ID = db.Column(db.Integer, db.ForeignKey("T_TRAIT.TRAIT_ID"), primary_key=True, comment="ID of the trait of this reaction")
    NPC = db.relationship("Npc")
    TRAIT = db.relationship("Trait")

    def __init__(self, REACTION_ID, NPC_ID, TRAIT_ID):
        self.REACTION_ID = REACTION_ID
        self.NPC_ID = NPC_ID
        self.TRAIT_ID = TRAIT_ID

    def __str__(self) -> str:
        return f"{self.REACTION_ID} {self.NPC_ID} {self.TRAIT_ID}"

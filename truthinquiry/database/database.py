import os
import random

from sqlalchemy import engine as eg
from flask_sqlalchemy import SQLAlchemy

sqlalchemy_db = SQLAlchemy()

class Locale(sqlalchemy_db.Model):
    __tablename__ = 'T_LOCALE'
    TEXT_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    LANG = sqlalchemy_db.Column(sqlalchemy_db.VARCHAR(2), primary_key=True)
    TEXT = sqlalchemy_db.Column(sqlalchemy_db.Text)

    def __init__(self, TEXT_ID, LANG, TEXT):
        self.TEXT_ID = TEXT_ID
        self.LANG = LANG
        self.TEXT = TEXT

    def __str__(self):
        return f"{self.TEXT_ID}  {self.LANG} {self.TEXT}"


class Place(sqlalchemy_db.Model):
    __tablename__ = 'T_PLACE'
    PLACE_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    NAME_LID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = sqlalchemy_db.relationship("Locale")

    def __init__(self, PLACE_ID, NAME_LID):
        self.PLACE_ID = PLACE_ID
        self.NAME_LID = NAME_LID

    def __str__(self):
        return f"{self.PLACE_ID} {self.NAME_LID}"


class Question(sqlalchemy_db.Model):
    __tablename__ = "T_QUESTION"
    QUESTION_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    QUESTION_TYPE = sqlalchemy_db.Column(sqlalchemy_db.Integer)
    TEXT_LID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = sqlalchemy_db.relationship("Locale")

    def __init__(self, QUESTION_ID, QUESTION_TYPE, TEXT_LID):
        self.QUESTION_ID = QUESTION_ID
        self.QUESTION_TYPE = QUESTION_TYPE
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"{self.QUESTION_ID} {self.QUESTION_TYPE} {self.TEXT_LID}"


class Answer(sqlalchemy_db.Model):
    __tablename__ = "T_ANSWER"
    ANSWER_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    QA_TYPE = sqlalchemy_db.Column(sqlalchemy_db.Integer)
    NPC_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_NPC.NPC_ID"))
    TEXT_LID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = sqlalchemy_db.relationship("Locale")
    NPC = sqlalchemy_db.relationship("Npc")

    def __init__(self, ANSWER_ID, QA_TYPE, NPC_ID, TEXT_LID):
        self.ANSWER_ID = ANSWER_ID
        self.QA_TYPE = QA_TYPE
        self.NPC_ID = NPC_ID
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"{self.ANSWER_ID} {self.QA_TYPE} {self.NPC_ID} {self.TEXT_LID}"


class Npc(sqlalchemy_db.Model):
    __tablename__ = "T_NPC"
    NPC_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    NAME_LID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = sqlalchemy_db.relationship("Locale")

    def __init__(self, NPC_ID, NAME_LID):
        self.NPC_ID = NPC_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"{self.NPC_ID} {self.NAME_LID}"


class Trait(sqlalchemy_db.Model):
    __tablename__ = "T_TRAIT"
    TRAIT_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    NAME_LID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_LOCALE.TEXT_ID"))
    DESC_LID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_LOCALE.TEXT_ID"))

    Name = sqlalchemy_db.relationship("Locale",foreign_keys=[NAME_LID])
    Desc = sqlalchemy_db.relationship("Locale",foreign_keys=[DESC_LID])


    def __init__(self, TRAIT_ID, NAME_LID):
        self.TRAIT_ID = TRAIT_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"{self.TRAIT_ID} {self.NAME_LID}"


class Reaction(sqlalchemy_db.Model):
    __tablename__ = "T_REACTION"
    REACTION_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    NPC_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_NPC.NPC_ID"), primary_key=True)
    TRAIT_ID = sqlalchemy_db.Column(sqlalchemy_db.Integer, sqlalchemy_db.ForeignKey("T_TRAIT.TRAIT_ID"), primary_key=True)
    NPC = sqlalchemy_db.relationship("Npc")
    TRAIT = sqlalchemy_db.relationship("Trait")

    def __init__(self, REACTION_ID, NPC_ID, TRAIT_ID):
        self.REACTION_ID = REACTION_ID
        self.NPC_ID = NPC_ID
        self.TRAIT_ID = TRAIT_ID

    def __str__(self) -> str:
        return f"{self.REACTION_ID} {self.NPC_ID} {self.TRAIT_ID}"


class Database:
    def __init__(self, sqlalchemy_db):
        self.sqlalchemy_db = sqlalchemy_db

    def init_app(self, app):
        self.app = app

        db_url = eg.URL.create(
            "mariadb+pymysql",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DBNAME")
        )
        self.app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    def create_tables(self):
        with self.app.app_context():
            self.sqlalchemy_db.create_all()
    
    def get_text_from_lid(self, lang: str, lid: int) -> str:
        """
        Returns the text linked to a language and a locale id

        :param lang: the lang to return the text in
        :param lid: the locale id the get the text from
        :return: the text associated to the lang and lid
        """
        return self.db.session.query(Locale).filter_by(LANG=lang, TEXT_ID=lid).one().TEXT

    def get_random_place(self) -> Place:
        """
        Returns a random place from the database.

        :return: a Place object
        """
        return random.choice(self.db.session.query(Place).all())

    def get_random_npc(self) -> Npc :
        """
        Returns a random npc from the database

        :return: a Npc object
        """
        return random.choice(self.db.session.query(Npc).all())

    def get_npc_random_trait_id(self,npc_id: int) -> int:
        """
        Returns a random reaction for a given npc

        :param npc_id: the npc to get the reaction from
        :return: a reaction identified by it's trait id
        """
        reactions = self.db.session.query(Reaction).filter_by(NPC_ID=npc_id.NPC_ID).all()
        reaction = random.choice(reactions)
        return reaction.TRAIT_ID

    def get_npc_random_answer(self, npc_id:int, qa_type:int) -> Answer :
        """
        Returns a random answser from a given npc and question type

        :param npc_id: the npc to get the answer from
        :param qa_type: the type of the question
        :return: an Answer object
        """
        answers = self.db.session.query(Answer).filter_by(QA_TYPE=qa_type,NPC_ID=npc_id.NPC_ID).all()
        return random.choice(answers)

    def get_random_question(self, qa_type: int) -> Question :
        """
        Returns a random inspector question from a question type

        :param qa_type: the type of the question
        :return: a Question object
        """
        answers = self.db.session.query(Question).filter_by(QUESTION_TYPE=qa_type).all()
        return random.choice(answers)

    def get_trait_from_text(self, text: str) -> int:
        """
        Returns the trait_id from its text value

        :param text: the text representation of the trait in any lang
        :return: the trait_id linked to this text
        """
        trait_lid = self.db.session.query(Locale).filter_by(TEXT=text).one().TEXT_ID
        return self.db.session.query(Trait).filter_by(NAME_LID=trait_lid).one().TRAIT_ID

    def get_trait_from_trait_id(self, trait_id: int) -> Trait:
        """
        Gets a Trait object from a trait_id

        :param trait_id: the id of the trait to search for
        :return: a Trait object
        """
        trait = self.db.session.query(Trait).filter_by(TRAIT_ID=trait_id).one()
        return trait

    def get_reaction_description(self, lang, npc_id, trait_id) -> str:
        """
        Returns the description of the reaction of a given npc in the language specified by the parametter lang

        :param lang: the language to return the description in
        :param npc_id: the id of the npc to get the reaction description from
        :trait_id: the trait associated to the reaction to get the description from
        :return: the description in the given language
        """
        desc_lid = self.db.session.query(Reaction).filter_by(NPC_ID=npc_id,TRAIT_ID=trait_id).one().DESC_LID
        return self.get_text_from_lid(lang, desc_lid)

    def get_traits(self, lang: str) -> list:
        """
        Returns the list of all possible reactions trait in the given language

        :param lang: the lang to return the reactions traits in
        :return: a list of string reprensentation of the reactions traits
        """
        traits = []
        for trait in self.db.session.query(Trait).all():
            traits.append(self.get_text_from_lid(lang,trait.NAME_LID))
        return traits

db = Database(sqlalchemy_db)
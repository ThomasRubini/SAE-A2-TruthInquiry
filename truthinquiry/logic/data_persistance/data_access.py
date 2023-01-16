import os
import random
import truthinquiry.logic.data_persistance.tables as tables

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import engine as eg

url_object = eg.URL.create(
    "mariadb+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_DBNAME"),
)
engine = create_engine(url_object, pool_pre_ping=True, pool_recycle=300)
session = Session(engine)


def get_text_from_lid(lang: str, lid: int) -> str:
    """
    Returns the text linked to a language and a locale id

    :param lang: the lang to return the text in
    :param lid: the locale id the get the text from
    :return: the text associated to the lang and lid
    """
    return session.query(tables.Locale).filter_by(LANG=lang, TEXT_ID=lid).one().TEXT

def get_random_place() -> tables.Place:
    """
    Returns a random place from the database.

    :return: a Place object
    """
    return random.choice(session.query(tables.Place).all())

def get_random_npc() -> tables.Npc :
    """
    Returns a random npc from the database

    :return: a Npc object
    """
    return random.choice(session.query(tables.Npc).all())

def get_npc_random_trait_id(npc_id: int) -> int:
    """
    Returns a random reaction for a given npc

    :param npc_id: the npc to get the reaction from
    :return: a reaction identified by it's trait id
    """
    reactions = session.query(tables.Reaction).filter_by(NPC_ID=npc_id.NPC_ID).all()
    reaction = random.choice(reactions)
    return reaction.TRAIT_ID

def get_npc_random_answer(npc_id:int, qa_type:int) -> tables.Answer :
    """
    Returns a random answser from a given npc and question type

    :param npc_id: the npc to get the answer from
    :param qa_type: the type of the question
    :return: an Answer object
    """
    answers = session.query(tables.Answer).filter_by(QA_TYPE=qa_type,NPC_ID=npc_id.NPC_ID).all()
    return random.choice(answers)

def get_random_question(qa_type: int) -> tables.Question :
    """
    Returns a random inspector question from a question type

    :param qa_type: the type of the question
    :return: a Question object
    """
    answers = session.query(tables.Question).filter_by(QUESTION_TYPE=qa_type).all()
    return random.choice(answers)

def get_trait_from_text(text: str) -> int:
    """
    Returns the trait_id from its text value

    :param text: the text representation of the trait in any lang
    :return: the trait_id linked to this text
    """
    trait_lid = session.query(tables.Locale).filter_by(TEXT=text).one().TEXT_ID
    return session.query(tables.Trait).filter_by(NAME_LID=trait_lid).one().TRAIT_ID

def get_trait_from_trait_id(trait_id: int) -> tables.Trait:
    """
    Gets a Trait object from a trait_id

    :param trait_id: the id of the trait to search for
    :return: a Trait object
    """
    trait = session.query(tables.Trait).filter_by(TRAIT_ID=trait_id).one()
    return trait

def get_reaction_description(lang,npc_id,trait_id) -> str:
    """
    Returns the description of the reaction of a given npc in the language specified by the parametter lang

    :param lang: the language to return the description in
    :param npc_id: the id of the npc to get the reaction description from
    :trait_id: the trait associated to the reaction to get the description from
    :return: the description in the given language
    """
    desc_lid = session.query(tables.Reaction).filter_by(NPC_ID=npc_id,TRAIT_ID=trait_id).one().DESC_LID
    return get_text_from_lid(lang,desc_lid)

def get_traits(lang: str) -> list:
    """
    Returns the list of all possible reactions trait in the given language

    :param lang: the lang to return the reactions traits in
    :return: a list of string reprensentation of the reactions traits
    """
    traits = []
    for trait in session.query(tables.Trait).all():
        traits.append(get_text_from_lid(lang,trait.NAME_LID))
    return traits

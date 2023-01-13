import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import engine as eg
import random
import truthseeker.logic.data_persistance.tables as tables

url_object = eg.URL.create(
    "mariadb+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_DBNAME"),
)
engine = create_engine(url_object)
session = Session(engine)

def get_text_from_lid(lang,lid) -> str:
    return session.query(tables.Locale).filter_by(LANG=lang, TEXT_ID=lid).one().TEXT

def get_random_place() -> tables.Place:
    return random.choice(session.query(tables.Place).all())

def get_random_npc() -> tables.Npc :
    return random.choice(session.query(tables.Npc).all())

def get_npc_random_trait_id(npc) -> int:
    reactions = session.query(tables.Reaction).filter_by(NPC_ID=npc.NPC_ID).all()
    reaction = random.choice(reactions)
    return reaction.TRAIT_ID

def get_npc_random_answer(npc, QA_TYPE) -> tables.Answer :
    answers = session.query(tables.Answer).filter_by(QA_TYPE=QA_TYPE,NPC_ID=npc.NPC_ID).all()
    return random.choice(answers)

def get_random_question(QA_TYPE) -> tables.Answer :
    answers = session.query(tables.Question).filter_by(QUESTION_TYPE=QA_TYPE).all()
    return random.choice(answers)

def get_trait_from_text(text):
    trait_lid = session.query(tables.Locale).filter_by(TEXT=text).one().TEXT_ID
    return session.query(tables.Trait).filter_by(NAME_LID=trait_lid).one().TRAIT_ID

def get_trait_from_trait_id(trait_id):
    trait = session.query(tables.Trait).filter_by(TRAIT_ID=trait_id).one()
    return trait

def get_reaction_description(lang,npc_id,trait_id):
    desc_lid = session.query(tables.Reaction).filter_by(NPC_ID=npc_id,TRAIT_ID=trait_id).one().DESC_LID
    return get_text_from_lid(lang,desc_lid)

def get_traits(lang):
    traits = []
    for trait in session.query(tables.Trait).all():
        traits.append(get_text_from_lid(lang,trait.NAME_LID))
    return traits
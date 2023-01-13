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

def getTextFromLid(lang,lid) -> str:
    return session.query(tables.Locale).filter_by(LANG=lang, TEXT_ID=lid).one().TEXT

def getRandomPlace() -> tables.Place:
    return random.choice(session.query(tables.Place).all())

def getRandomNpc() -> tables.Npc :
    return random.choice(session.query(tables.Npc).all())

def getNpcRandomTraitId(npc) -> int:
    reactions = session.query(tables.Reaction).filter_by(NPC_ID=npc.NPC_ID).all()
    reaction = random.choice(reactions)
    return reaction.TRAIT_ID

def getNpcRandomAnswer(npc, QA_TYPE) -> tables.Answer :
    answers = session.query(tables.Answer).filter_by(QA_TYPE=QA_TYPE,NPC_ID=npc.NPC_ID).all()
    return random.choice(answers)

def getRandomQuestion(QA_TYPE) -> tables.Answer :
    answers = session.query(tables.Question).filter_by(QUESTION_TYPE=QA_TYPE).all()
    return random.choice(answers)

def getTraitFromText(text):
    trait_lid = session.query(tables.Locale).filter_by(TEXT=text).one().TEXT_ID
    return session.query(tables.Trait).filter_by(NAME_LID=trait_lid).one().TRAIT_ID

def getTraitFromTraitId(trait_id):
    trait = session.query(tables.Trait).filter_by(TRAIT_ID=trait_id).one()
    return trait

def getTraits(lang):
    traits = []
    for trait in session.query(tables.Trait).all():
        traits.append(getTextFromLid(lang,trait.NAME_LID))
    return traits
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import engine as eg

from tables import *

from data.answer import ANSWERS
from data.locales import LOCALES
from data.npc import NPCS
from data.places import PLACES
from data.questions import QUESTIONS
from data.reactions import REACTIONS
from data.traits import TRAITS


url_object = eg.URL.create(
    "mariadb+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_DBNAME"),
)
engine = create_engine(url_object)

# Reset data tables
with Session(engine) as session:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    print("adding locales")
    for locale in LOCALES:
        print(locale)
        session.add(locale)
        session.commit()
    
    
    print("adding places")
    for place in PLACES:
        print(place)
        session.add(place)
        session.commit()

    
    print("adding NPCS")
    for npc in NPCS:
        print(npc)
        session.add(npc)
        session.commit()
    
    
    print("adding trait")
    for trait in TRAITS:
        print(trait)
        session.add(trait)
        session.commit()
    
    
    print("adding questions")
    for question in QUESTIONS:
        print(question)
        session.add(question)
        session.commit()
    
    
    print("adding answers")
    for answer in ANSWERS:
        print(answer)
        session.add(answer)
        session.commit()
    
    
    print("adding reactions")
    for reaction in REACTIONS:
        print(reaction)
        session.add(reaction)
        session.commit()
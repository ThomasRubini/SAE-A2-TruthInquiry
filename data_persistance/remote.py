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

from secret import HOST, USER, PASS

url_object = eg.URL.create(
    "mariadb+pymysql",
    username=USER,
    password=PASS,
    host=HOST,
    port=6776,
    database="truthInquiry",
)
engine = create_engine(url_object)


# Reset data tables
with Session(engine) as session:


    session.execute("SELECT CONCAT('DROP TABLE IF EXISTS `', TABLE_SCHEMA, '`.`', TABLE_NAME, '`;') FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'mydb'")
    Base.metadata.create_all(engine)

    print("adding locales")
    for locale in LOCALES:
        print(locale)
    session.add_all(LOCALES)
    
    
    print("adding places")
    for place in PLACES:
        print(place)
    session.add_all(PLACES)

    
    print("adding NPCS")
    for npc in NPCS:
        print(npc)
    session.add_all(NPCS)
    
    
    print("adding trait")
    for trait in TRAITS:
        print(trait)
    session.add_all(TRAITS)
    
    
    print("adding questions")
    for question in QUESTIONS:
        print(question)
    session.add_all(QUESTIONS)
    
    
    print("adding answers")
    for answer in ANSWERS:
        print(answer)
    session.add_all(ANSWERS)
    
    
    print("adding reactions")
    for reactions in REACTIONS:
        print(reactions)
    session.add_all(REACTIONS)
    
    session.commit()

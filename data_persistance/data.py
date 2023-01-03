from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import engine as eg

from tables import *

from answer import ANSWER
from locales import LOCALES
from npc import NPCS
from places import PLACES
from questions import QUESTIONS
from reactions import REACTIONS
from traits import TRAITS

from secret import HOST, USER, PASS

url_object = eg.URL.create(
    "mariadb+pymysql",
    username=USER,
    password=PASS,
    host=HOST,
    port=6776,
    database="truthInquiry",
)

# Create Engine and tables
engine = create_engine(url_object)
Base.metadata.create_all(engine)

with Session(engine) as session:
    print("adding locales")
    session.add_all(LOCALES)
    print("adding places")
    session.add_all(PLACES)
    print("adding NPCS")
    session.add_all(NPCS)
    print("adding trait")
    session.add_all(TRAITS)
    print("adding questions")
    session.add_all(QUESTIONS)
    print("adding answers")
    session.add_all(ANSWER)
    print("adding reaction")
    session.add_all(REACTIONS)
    session.commit()
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from tables import *

from answer import ANSWER
from locales import LOCALES
from npc import NPCS
from places import PLACES
from questions import QUESTIONS
from reactions import REACTIONS
from traits import TRAITS


# Create Engine and tables
engine = create_engine("sqlite://", echo=True, future=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all(ANSWER)
    session.add_all(LOCALES)
    session.add_all(NPCS)
    session.add_all(PLACES)
    session.add_all(QUESTIONS)
    session.add_all(REACTIONS)
    session.add_all(TRAITS)

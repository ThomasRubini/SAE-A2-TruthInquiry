# Load .env file
from dotenv import load_dotenv
load_dotenv()
import json
import yaml
import argparse

from sqlalchemy.orm import sessionmaker

from truthinquiry.ext.database.sa import engine
from truthinquiry.ext.database.models import *

Session = sessionmaker(bind=engine)
session = Session()


def bulk_export():
    data = {}

    rooms = data["rooms"] = {}
    for room in session.query(Place).all():
        current_room = rooms[room.PLACE_ID] = {}
        for text in session.query(Locale).filter_by(TEXT_ID=room.NAME_LID).all():
            current_room[text.LANG] = text.TEXT
    
    questions = data["questions"] = {}
    data["questions"]["withwho"] = {}
    data["questions"]["withwho"]["text"] = []
    data["questions"]["where"] = {}
    data["questions"]["where"]["text"] = []
    for question in session.query(QuestionType).all():
        question_list = data["questions"]["where"]["text"] if question.QUESTION_TYPE_ID == 0 else data["questions"]["withwho"]["text"]
        for text in session.query(Text).filter_by(LID=question.TEXT_LID).all():
            question_list.append({text.LANG : text.TEXT})
    
    traits = data["traits"] = {}
    for trait in session.query(Trait).all():
        current_trait = traits[trait.TRAIT_ID] = {}
        current_trait["name"] = {}
        for text in session.query(TEXT).filter_by(LID=trait.NAME_LID):
            current_trait["name"][text.LANG] = text.TEXT
        
        current_trait["description"] = {}
        for text in session.query(TEXT).filter_by(LID=trait.DESC_LID):
            current_trait["description"][text.LANG] = text.TEXT

    npcs = data["npcs"] = {}
    for npc in session.query(Npc).all():
        current_npc = npcs[npc.NPC_ID] = {}
        current_npc["name"] = {}
        for text in session.query(TEXT).filter_by(LID=npc.NAME_LID):
            current_npc["name"][text.LANG] = text.TEXT
        
        #TODO reactions
        current_npc["answers"] = {}
        current_npc["answers"]["where"] = []
        current_npc["answers"]["withwho"] = []
        for answer in session.query(Answer).filter_by(NPC_ID=npc.NPC_ID):
            answer_list = current_npc["answers"]["where"] if answer.QA_TYPE == 0 else current_npc["answers"]["withwho"]
            for text in session.query(TEXT).filter_by(LID=answer.TEXT_LID):
                answer_list.append({text.LANG: text.TEXT})
    return data


print(json.dumps(bulk_export()))

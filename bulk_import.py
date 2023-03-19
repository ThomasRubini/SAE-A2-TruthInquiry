from dotenv import load_dotenv
load_dotenv()

import sys
import yaml
import os

from sqlalchemy.orm import sessionmaker
from truthinquiry.ext.database.models import *
from truthinquiry.ext.database.sa import engine

Session = sessionmaker(bind=engine)
session = Session()

# full reset .w.
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


class LocaleManager():
    def __init__(self):
        self.used_lids = [0]
        [self.used_lids.append(locale.LID) for locale in session.query(Locale).all()]

    def get_unused_lid(self):
        new_lid = max(self.used_lids) + 1
        self.used_lids.append(new_lid)
        return new_lid
    
    def get_used_lids(self):
        return self.used_lids[1:]


def bulk_import(data, dir):

    # Data list that will be commited to the db
    TEXT_LIST = []
    TRAIT_DICT = {}
    REACTION_LIST = []
    QUESTIONS_LIST = []
    ANSWER_LIST = []
    NPC_LIST = []
    ROOMS_LIST = []
    
    lm = LocaleManager()
    getid = lm.get_unused_lid

    # Questions

    # Where type questions

    question_type_zero = QuestionType(0, getid())
    QUESTIONS_LIST.append(question_type_zero)

    question_type_one = QuestionType(1, getid())
    QUESTIONS_LIST.append(question_type_one)

    questions = data["questions"]
    # handle where type quetions
    for question in questions["where"]["text"]:
        lang = list(question.keys())[0]
        text = list(question.values())[0]
        TEXT_LIST.append(Text(0,question_type_zero.TEXT_LID, lang, text))

    # handle with who type quetions
    for question in questions["withwho"]["text"]:
        lang = list(question.keys())[0]
        text = list(question.values())[0]
        TEXT_LIST.append(Text(0,question_type_one.TEXT_LID, lang, text))

    # Traits
    traits = data["traits"]
    for trait_key, trait in traits.items():
        # create the new trait
        new_trait = Trait(None, getid(), getid())

        for lang in trait["name"]:
            TEXT_LIST.append(Text(0,new_trait.NAME_LID,
                            lang, trait["name"][lang]))

        for lang in trait["description"]:
            TEXT_LIST.append(Text(0,new_trait.DESC_LID, lang,
                            trait["description"][lang]))

        TRAIT_DICT[trait_key] = new_trait

    # Npcs
    npcs = data["npcs"]
    npcid = 1
    for npc in npcs.values():
        new_npc = Npc(npcid, getid())

        # handle the names
        for lang in npc["name"]:
            TEXT_LIST.append(Text(0,new_npc.NAME_LID, lang, npc["name"][lang]))

        for trait_key, reaction in npc.get("reactions", {}).items():
            trait = TRAIT_DICT[trait_key]
            new_reaction = Reaction(None, new_npc.NPC_ID, None)
            new_reaction.TRAIT = trait

            img_path = os.path.join(dir, reaction["img"])

            with open(img_path, "rb") as f:
                new_reaction.IMG = f.read()
            
            REACTION_LIST.append(new_reaction)


        for question_type in npc["answers"]:
            question_type_id = question_type_zero.QUESTION_TYPE_ID if question_type == "where" else question_type_one.QUESTION_TYPE_ID

            new_answer = Answer(question_type_id, new_npc.NPC_ID, getid())
            ANSWER_LIST.append(new_answer)

            for answer in npc["answers"][question_type]:
                lang = list(answer.keys())[0]
                text = list(answer.values())[0]
                TEXT_LIST.append(Text(0,new_answer.TEXT_LID, lang, text))

        NPC_LIST.append(new_npc)
        npcid += 1

    # rooms
    rooms = data["rooms"]
    for room in rooms.values():
        new_room = Place(0,getid())
        for lang in room:
            TEXT_LIST.append(Text(0,new_room.NAME_LID, lang, room[lang]))
        ROOMS_LIST.append(new_room)
    
    for lid in lm.get_used_lids():
        print("lid :"+ str(lid))
        session.add(Locale(lid))
    
    for text in TEXT_LIST:
        print("Text : "+str(text))
        session.add(text)
        session.commit()

    for question in QUESTIONS_LIST:
        print("Question : "+str(question))
        session.add(question)
        session.commit()

    for trait in TRAIT_DICT.values():
        print("Trait : "+ str(trait))
        session.add(trait)
        session.commit()

    for npc in NPC_LIST:
        print("Npc : "+ str(npc))
        session.add(npc)
        session.commit()

    for reaction in REACTION_LIST:
        print("Reaction : " + str(reaction))
        session.add(reaction)
        session.commit()

    for answer in ANSWER_LIST:
        print("Answer : "+ str(answer))
        session.add(answer)
        session.commit()

    for room in ROOMS_LIST:
        print("Room : "+str(room))
        session.add(room)
        session.commit()

if len(sys.argv) <= 1:
    print("Please enter input file")
else:
    path = sys.argv[1]
    bulk_import(yaml.load(open(path, "r"), yaml.Loader), os.path.dirname(path))

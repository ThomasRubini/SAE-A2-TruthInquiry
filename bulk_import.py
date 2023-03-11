
import argparse
import yaml
from dotenv import load_dotenv
load_dotenv()
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
        [self.used_lids.append(locale.TEXT_ID) for locale in session.query(Locale).all()]

    def get_unused_lid(self):
        new_lid = max(self.used_lids) + 1
        self.used_lids.append(new_lid)
        return new_lid



def bulk_import(data):

    # Data list that will be commited to the db
    LID_LIST = []
    TRAIT_LIST = []
    REACTION_LIST = []
    QUESTIONS_LIST = []
    ANSWER_LIST = []
    NPC_LIST = []
    ROOMS_LIST = []
    
    # helper list to simplify
    trait_names = {}
    lm = LocaleManager()
    getid = lm.get_unused_lid

    # Questions

    # Where type questions

    question_type_zero = Question(0, 0, getid())
    QUESTIONS_LIST.append(question_type_zero)

    question_type_one = Question(0, 1, getid())
    QUESTIONS_LIST.append(question_type_zero)

    questions = data["questions"]
    # handle where type quetions
    for question in questions["where"]["text"]:
        lang = list(question.keys())[0]
        text = list(question.values())[0]
        LID_LIST.append(Locale(question_type_zero.TEXT_LID, lang, text))

    # handle with who type quetions
    for question in questions["withwho"]["text"]:
        lang = list(question.keys())[0]
        text = list(question.values())[0]
        LID_LIST.append(Locale(question_type_zero.TEXT_LID, lang, text))

    # Traits
    traits = data["traits"]
    for trait in traits.values():
        # create the new trait
        new_trait = Trait(0,getid(), getid())

        for lang in trait["name"]:
            LID_LIST.append(Locale(new_trait.NAME_LID,
                            lang, trait["name"][lang]))
            trait_names[trait["name"][lang]] = new_trait.TRAIT_ID

        for lang in trait["description"]:
            LID_LIST.append(Locale(new_trait.DESC_LID, lang,
                            trait["description"][lang]))

        TRAIT_LIST.append(new_trait)

    # Npcs
    npcs = data["npc"]
    for npc in npcs.values():
        new_npc = Npc(0, getid())

        # handle the names
        for lang in npc["name"]:
            LID_LIST.append(Locale(new_npc.NAME_LID, lang, npc["name"][lang]))

        for reaction in npc["reactions"]:
            if reaction in list(trait_names.keys()):
                new_reaction = Reaction(0,new_npc.NPC_ID, trait_names[reaction])
                REACTION_LIST.append(new_reaction)
        for question_type in npc["answers"]:
            question_type_id = 0 if question_type == "where" else 1

            new_answer = Answer(0, question_type_id, new_npc.NPC_ID, getid())
            ANSWER_LIST.append(new_answer)

            for answer in npc["answers"][question_type]:
                lang = list(answer.keys())[0]
                text = list(answer.values())[0]
                LID_LIST.append(Locale(new_answer.TEXT_LID, lang, text))

        NPC_LIST.append(new_npc)

    # rooms
    rooms = data["rooms"]
    for room in rooms.values():
        new_room = Place(0,getid())
        for lang in room:
            LID_LIST.append(Locale(new_room.NAME_LID, lang, room[lang]))
        ROOMS_LIST.append(new_room)
    
    for text in LID_LIST:
        print("Locale : "+str(text))
        session.add(text)
        session.commit()
    for question in QUESTIONS_LIST:
        print("Question : "+str(question))
        session.add(question)
        session.commit()
    for trait in TRAIT_LIST:
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


file = open("bulkData.yml", "r")

bulk_import(yaml.load(file, yaml.Loader))

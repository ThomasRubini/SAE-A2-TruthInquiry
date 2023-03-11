from sqlalchemy import Column, Integer, VARCHAR, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Locale(Base):
    """
    Stores the different texts needed by the other tables in multiple languages
    """

    __tablename__ = 'T_LOCALE'
    TEXT_ID = Column(Integer, primary_key=True, comment="ID of this specific text. These IDs may be recycled in the future and may only be used for a short time period.")
    LID = Column(Integer, comment="ID of this locale (the other tables references to this with *_LID columns)")
    LANG = Column(VARCHAR(2), comment="lang ID of the text value in this row, e.g FR, EN, ES")
    TEXT = Column(Text, comment="Actual text stored for that text ID and lang")

    def __init__(self, TEXT_ID, LANG, TEXT):
        self.TEXT_ID = TEXT_ID
        self.LANG = LANG
        self.TEXT = TEXT

    def __str__(self):
        return f"{self.TEXT_ID}  {self.LANG} {self.TEXT}"


class Place(Base):
    """
    Store litteral places, could be a room in the manor or near it
    """

    __tablename__ = 'T_PLACE'
    PLACE_ID = Column(Integer, primary_key=True, comment="ID of this place")
    NAME_LID = Column(Integer, ForeignKey("T_LOCALE.TEXT_ID"), comment="Place name")
    LOCALE = relationship("Locale")

    def __init__(self, PLACE_ID, NAME_LID):
        self.PLACE_ID = PLACE_ID
        self.NAME_LID = NAME_LID

    def __str__(self):
        return f"{self.PLACE_ID} {self.NAME_LID}"


class QuestionType(Base):
    """
    Stores questions types that can be asked by players, e.g "where", "with tho"
    """

    __tablename__ = "T_QUESTION_TYPE"
    QUESTION_TYPE_ID = Column(Integer, primary_key=True, comment="ID of this question type.")
    TEXT_LID = Column(Integer, ForeignKey("T_LOCALE.TEXT_ID"), comment="Question text")
    LOCALE = relationship("Locale")

    def __init__(self, QUESTION_TYPE_ID, TEXT_LID):
        self.QUESTION_ID = QUESTION_TYPE_ID
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"{self.QUESTION_ID} {self.QUESTION_TYPE_ID}"


class Answer(Base):
    """
    Stores answers given by NPCs
    They are relative to the question type ID, and NPC ID
    """

    __tablename__ = "T_ANSWER"
    ANSWER_ID = Column(Integer, primary_key=True, comment="ID of this answer")
    QA_TYPE = Column(Integer, comment="Question type ID")
    NPC_ID = Column(Integer, ForeignKey("T_NPC.NPC_ID"), comment="ID of the NPC that will say this answer")
    TEXT_LID = Column(Integer, ForeignKey("T_LOCALE.TEXT_ID"), comment="Text of the answer")
    LOCALE = relationship("Locale")
    NPC = relationship("Npc")

    def __init__(self, ANSWER_ID, QA_TYPE, NPC_ID, TEXT_LID):
        self.ANSWER_ID = ANSWER_ID
        self.QA_TYPE = QA_TYPE
        self.NPC_ID = NPC_ID
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"{self.ANSWER_ID} {self.QA_TYPE} {self.NPC_ID} {self.TEXT_LID}"


class Npc(Base):
    """
    Store Npcs
    """

    __tablename__ = "T_NPC"
    NPC_ID = Column(Integer, primary_key=True, comment="ID of this Npc")
    NAME_LID = Column(Integer, ForeignKey("T_LOCALE.TEXT_ID"), comment="Name of this Npc")
    LOCALE = relationship("Locale")

    def __init__(self, NPC_ID, NAME_LID):
        self.NPC_ID = NPC_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"{self.NPC_ID} {self.NAME_LID}"


class Trait(Base):
    """
    Store reaction types, e.g 'happy', 'sad', without relation with NPCs
    """
    __tablename__ = "T_TRAIT"
    TRAIT_ID = Column(Integer, primary_key=True, comment="ID of this trait")
    NAME_LID = Column(Integer, ForeignKey("T_LOCALE.TEXT_ID"), comment="Name of this trait")
    DESC_LID = Column(Integer, ForeignKey("T_LOCALE.TEXT_ID"), comment="Description of this trait")

    Name = relationship("Locale",foreign_keys=[NAME_LID])
    Desc = relationship("Locale",foreign_keys=[DESC_LID])


    def __init__(self, TRAIT_ID, NAME_LID):
        self.TRAIT_ID = TRAIT_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"{self.TRAIT_ID} {self.NAME_LID}"


class Reaction(Base):
    """
    Relation between a NPC and a Trait
    """
    __tablename__ = "T_REACTION"
    REACTION_ID = Column(Integer, primary_key=True, comment="ID of this reaction")
    NPC_ID = Column(Integer, ForeignKey("T_NPC.NPC_ID"), primary_key=True, comment="Name of the NPC that will have this reaction")
    TRAIT_ID = Column(Integer, ForeignKey("T_TRAIT.TRAIT_ID"), primary_key=True, comment="ID of the trait of this reaction")
    NPC = relationship("Npc")
    TRAIT = relationship("Trait")

    def __init__(self, REACTION_ID, NPC_ID, TRAIT_ID):
        self.REACTION_ID = REACTION_ID
        self.NPC_ID = NPC_ID
        self.TRAIT_ID = TRAIT_ID

    def __str__(self) -> str:
        return f"{self.REACTION_ID} {self.NPC_ID} {self.TRAIT_ID}"

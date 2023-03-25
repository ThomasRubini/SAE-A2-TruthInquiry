from sqlalchemy import Column, Integer, VARCHAR, Text, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Text(Base):
    """
    Stores the different texts needed by the Locale table in multiple languages
    A LID and a language may be associated with multiple texts (mostly in the case we need to choose a text at random)
    """

    __tablename__ = 'T_TEXT'

    TEXT_ID = Column(Integer, autoincrement=True, primary_key=True, comment="ID of this specific text. These IDs may be recycled in the future and may only be used for a short time period.")
    LID = Column(Integer, ForeignKey("T_LOCALE.LID"), comment="Reference to the locale that this text provides")
    LANG = Column(VARCHAR(2), comment="lang ID of the text value in this row, e.g FR, EN, ES")
    TEXT = Column(Text, comment="Actual text stored")
    LOCALE = relationship("Locale", backref='TEXTS')

    def __init__(self, TEXT_ID, LID, LANG, TEXT):
        self.TEXT_ID = TEXT_ID
        self.LID = LID
        self.LANG = LANG
        self.TEXT = TEXT


    def __str__(self):
        return f"Text(TEXT_ID={self.TEXT_ID}, LID={self.LID}, LANG={self.LANG}, TEXT={self.TEXT})"

    def __repr__(self) -> str:
        return self.__str__()


class Locale(Base):
    """
    Each row represent a text that is needed by other tables.
    the 'Text' table will reference these LIDs with the actual text in multiple languages
    Stores the different texts needed by the other tables
    """

    __tablename__ = 'T_LOCALE'
    LID = Column(Integer, primary_key=True, autoincrement=True, comment="ID of this locale (the other tables references to this with *_LID columns)")
    
    def __init__(self, LID):
        self.LID = LID
        
    def __str__(self):
        return f"Locale(LID={self.LID})"

    def __repr__(self) -> str:
        return self.__str__()

    def get_texts(self, lang):
        texts = []
        for text in self.TEXTS:
            if text.LANG == lang:
                texts.append(text)
        return texts

    def get_text(self, lang, auto_create=False):
        for text in self.TEXTS:
            if text.LANG == lang:
                return text
        
        if auto_create:
            text = Text(None, None, lang, None)
            self.TEXTS.append(text)
            return text
        else:
            return None

        


class Place(Base):
    """
    Store litteral places, could be a room in the manor or near it
    """

    __tablename__ = 'T_PLACE'
    PLACE_ID = Column(Integer, primary_key=True, autoincrement=True, comment="ID of this place")
    NAME_LID = Column(Integer, ForeignKey("T_LOCALE.LID"), comment="Place name")
    NAME_LOCALE = relationship("Locale")

    def __init__(self, PLACE_ID, NAME_LID):
        self.PLACE_ID = PLACE_ID
        self.NAME_LID = NAME_LID

    def __str__(self):
        return f"Place(PLACE_ID={self.PLACE_ID} NAME_LID={self.NAME_LID})"

    def __repr__(self) -> str:
        return self.__str__()


class QuestionType(Base):
    """
    Stores questions types that can be asked by players, e.g "where", "with tho"
    """

    __tablename__ = "T_QUESTION_TYPE"
    QUESTION_TYPE_ID = Column(Integer, default=0, primary_key=True, comment="ID of this question type.")
    TEXT_LID = Column(Integer, ForeignKey("T_LOCALE.LID"), comment="Question text")
    TEXT_LOCALE = relationship("Locale")

    def __init__(self, QUESTION_TYPE_ID, TEXT_LID):
        self.QUESTION_TYPE_ID = QUESTION_TYPE_ID
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"QuestionType(QUESTION_TYPE_ID={self.QUESTION_TYPE_ID}, TEXT_LID={self.TEXT_LID})"

    def __repr__(self) -> str:
        return self.__str__()


class Answer(Base):
    """
    Stores answers given by NPCs
    They are relative to the question type ID, and NPC ID
    """

    __tablename__ = "T_ANSWER"
    QUESTION_TYPE_ID = Column(Integer, ForeignKey("T_QUESTION_TYPE.QUESTION_TYPE_ID"), primary_key=True, comment="Question type ID")
    NPC_ID = Column(Integer, ForeignKey("T_NPC.NPC_ID"), primary_key=True, comment="ID of the NPC that will say this answer")
    TEXT_LID = Column(Integer, ForeignKey("T_LOCALE.LID"), comment="Text of the answer")
    TEXT_LOCALE = relationship("Locale")
    NPC = relationship("Npc", backref="ANSWERS")

    def __init__(self, QUESTION_TYPE_ID, NPC_ID, TEXT_LID):
        self.QUESTION_TYPE_ID = QUESTION_TYPE_ID
        self.NPC_ID = NPC_ID
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"Answer(QUESTION_TYPE_ID={self.QUESTION_TYPE_ID}, NPC_ID={self.NPC_ID}, TEXT_LID={self.TEXT_LID})"

    def __repr__(self) -> str:
        return self.__str__()
        


class Npc(Base):
    """
    Store Npcs
    """

    __tablename__ = "T_NPC"
    NPC_ID = Column(Integer, autoincrement=True, primary_key=True, comment="ID of this Npc")
    NAME_LID = Column(Integer, ForeignKey("T_LOCALE.LID"), comment="Name of this Npc")
    DEFAULT_IMG = Column(LargeBinary(length=2**24), comment="Binary data of the default image of this Npc")
    NAME_LOCALE = relationship("Locale")

    def __init__(self, NPC_ID, NAME_LID):
        self.NPC_ID = NPC_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"Npc(NPC_ID={self.NPC_ID}, NAME_LID={self.NAME_LID})"

    def __repr__(self) -> str:
        return self.__str__()


class Trait(Base):
    """
    Store reaction types, e.g 'happy', 'sad', without relation with NPCs
    """
    __tablename__ = "T_TRAIT"
    TRAIT_ID = Column(Integer, primary_key=True, autoincrement=True, comment="ID of this trait")
    NAME_LID = Column(Integer, ForeignKey("T_LOCALE.LID"), comment="Name of this trait")
    DESC_LID = Column(Integer, ForeignKey("T_LOCALE.LID"), comment="Description of this trait")

    NAME_LOCALE = relationship("Locale",foreign_keys=[NAME_LID])
    DESC_LOCALE = relationship("Locale",foreign_keys=[DESC_LID])


    def __init__(self, TRAIT_ID, NAME_LID, DESC_LID):
        self.TRAIT_ID = TRAIT_ID
        self.NAME_LID = NAME_LID
        self.DESC_LID = DESC_LID

    def __str__(self) -> str:
        return f"Trait(TRAIT_ID={self.TRAIT_ID}, NAME_LID={self.NAME_LID}, DESC_LID={self.DESC_LID})"
        
    def __repr__(self) -> str:
        return self.__str__()


class Reaction(Base):
    """
    Relation between a NPC and a Trait
    """
    __tablename__ = "T_REACTION"
    REACTION_ID = Column(Integer, primary_key=True, autoincrement=True, comment="ID of this reaction")
    NPC_ID = Column(Integer, ForeignKey("T_NPC.NPC_ID"), primary_key=True, comment="Name of the NPC that will have this reaction")
    TRAIT_ID = Column(Integer, ForeignKey("T_TRAIT.TRAIT_ID"), primary_key=True, comment="ID of the trait of this reaction")
    IMG = Column(LargeBinary(length=2**24), comment="Binary data of the image associated to this npc and trait")
    NPC = relationship("Npc")
    TRAIT = relationship("Trait")

    def __init__(self, REACTION_ID, NPC_ID, TRAIT_ID):
        self.REACTION_ID = REACTION_ID
        self.NPC_ID = NPC_ID
        self.TRAIT_ID = TRAIT_ID

    def __str__(self) -> str:
        return f"Reaction(REACTION_ID={self.REACTION_ID}, NPC_ID={self.NPC_ID}, TRAIT_ID={self.TRAIT_ID})"

    def __repr__(self) -> str:
        return self.__str__()
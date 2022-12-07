from sqlalchemy import Column, Integer, Text,ForeignKey
from sqlalchemy.ext.declarative import declarative_base, relationship
Base = declarative_base()

class Locale(Base):
    __tablename__ = 'T_LOCALE'
    TEXT_ID = Column(Integer, primary_key=True)
    LANG = Column(Text)
    TEXT = Column(Text)
    def __init__(self, TEXT_ID, LANG,TEXT ):
        self.PLACE_ID = TEXT_ID
        self.LANG = LANG
        self.TEXT = TEXT
    def __str__(self):
        return self.PLACE_ID + " " + self.LANG + " " + self.TEXT

class Place(Base):
    __tablename__ = 'T_PLACE'
    PLACE_ID = Column(Integer, primary_key=True)
    NAME_LID = Column(Integer, ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = relationship("Locale")
    def __init__(self, PLACE_ID, NAME_LID ):
        self.PLACE_ID = PLACE_ID
        self.NAME_LID = NAME_LID
    def __str__(self):
        return self.PLACE_ID + " " + self.NAME_LID

class Question(Base):
    __tablename__ = "T_QUESTION"
    QUESTION_ID = Column(Integer, primary_key=True)
    QUESTION_TYPE = Column(Integer)
    TEXT_LID =  Column(Integer, ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = relationship("Locale")
    def __init__(self, QUESTION_ID,QUESTION_TYPE,TEXT_LID):
        self.QUESTION_ID = QUESTION_ID
        self.QUESTION_TYPE = QUESTION_TYPE  
        self.TEXT_LID = TEXT_LID
    def __str__(self):
        return self.QUESTION_ID + " " + self.QUESTION_TYPE + " "+ self.TEXT_LID

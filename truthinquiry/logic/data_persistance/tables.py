from truthinquiry import APP
db = APP.db


class Locale(db.Model):
    __tablename__ = 'T_LOCALE'
    TEXT_ID = db.Column(db.Integer, primary_key=True)
    LANG = db.Column(db.VARCHAR(2), primary_key=True)
    TEXT = db.Column(db.Text)

    def __init__(self, TEXT_ID, LANG, TEXT):
        self.TEXT_ID = TEXT_ID
        self.LANG = LANG
        self.TEXT = TEXT

    def __str__(self):
        return f"{self.TEXT_ID}  {self.LANG} {self.TEXT}"


class Place(db.Model):
    __tablename__ = 'T_PLACE'
    PLACE_ID = db.Column(db.Integer, primary_key=True)
    NAME_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = db.relationship("Locale")

    def __init__(self, PLACE_ID, NAME_LID):
        self.PLACE_ID = PLACE_ID
        self.NAME_LID = NAME_LID

    def __str__(self):
        return f"{self.PLACE_ID} {self.NAME_LID}"


class Question(db.Model):
    __tablename__ = "T_QUESTION"
    QUESTION_ID = db.Column(db.Integer, primary_key=True)
    QUESTION_TYPE = db.Column(db.Integer)
    TEXT_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = db.relationship("Locale")

    def __init__(self, QUESTION_ID, QUESTION_TYPE, TEXT_LID):
        self.QUESTION_ID = QUESTION_ID
        self.QUESTION_TYPE = QUESTION_TYPE
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"{self.QUESTION_ID} {self.QUESTION_TYPE} {self.TEXT_LID}"


class Answer(db.Model):
    __tablename__ = "T_ANSWER"
    ANSWER_ID = db.Column(db.Integer, primary_key=True)
    QA_TYPE = db.Column(db.Integer)
    NPC_ID = db.Column(db.Integer, db.ForeignKey("T_NPC.NPC_ID"))
    TEXT_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = db.relationship("Locale")
    NPC = db.relationship("Npc")

    def __init__(self, ANSWER_ID, QA_TYPE, NPC_ID, TEXT_LID):
        self.ANSWER_ID = ANSWER_ID
        self.QA_TYPE = QA_TYPE
        self.NPC_ID = NPC_ID
        self.TEXT_LID = TEXT_LID

    def __str__(self):
        return f"{self.ANSWER_ID} {self.QA_TYPE} {self.NPC_ID} {self.TEXT_LID}"


class Npc(db.Model):
    __tablename__ = "T_NPC"
    NPC_ID = db.Column(db.Integer, primary_key=True)
    NAME_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"))
    LOCALE = db.relationship("Locale")

    def __init__(self, NPC_ID, NAME_LID):
        self.NPC_ID = NPC_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"{self.NPC_ID} {self.NAME_LID}"


class Trait(db.Model):
    __tablename__ = "T_TRAIT"
    TRAIT_ID = db.Column(db.Integer, primary_key=True)
    NAME_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"))
    DESC_LID = db.Column(db.Integer, db.ForeignKey("T_LOCALE.TEXT_ID"))

    Name = db.relationship("Locale",foreign_keys=[NAME_LID])
    Desc = db.relationship("Locale",foreign_keys=[DESC_LID])


    def __init__(self, TRAIT_ID, NAME_LID):
        self.TRAIT_ID = TRAIT_ID
        self.NAME_LID = NAME_LID

    def __str__(self) -> str:
        return f"{self.TRAIT_ID} {self.NAME_LID}"


class Reaction(db.db.Model):
    __tablename__ = "T_REACTION"
    REACTION_ID = db.Column(db.Integer, primary_key=True)
    NPC_ID = db.Column(db.Integer, db.ForeignKey("T_NPC.NPC_ID"), primary_key=True)
    TRAIT_ID = db.Column(db.Integer, db.ForeignKey("T_TRAIT.TRAIT_ID"), primary_key=True)
    NPC = db.relationship("Npc")
    TRAIT = db.relationship("Trait")

    def __init__(self, REACTION_ID, DESC_LID, NPC_ID, TRAIT_ID):
        self.REACTION_ID = REACTION_ID
        self.DESC_LID = DESC_LID
        self.NPC_ID = NPC_ID
        self.TRAIT_ID = TRAIT_ID

    def __str__(self) -> str:
        return f"{self.REACTION_ID} {self.DESC_LID} {self.NPC_ID} {self.TRAIT_ID}"

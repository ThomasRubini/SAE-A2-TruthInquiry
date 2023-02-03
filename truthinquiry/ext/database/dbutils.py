from truthinquiry.ext.database import *

def get_text_from_lid(lang: str, lid: int) -> str:
    """
    Returns the text linked to a language and a locale id

    :param lang: the lang to return the text in
    :param lid: the locale id the get the text from
    :return: the text associated to the lang and lid
    """
    return db.session.query(Locale).filter_by(LANG=lang, TEXT_ID=lid).one().TEXT

def get_random_place() -> Place:
    """
    Returns a random place from the database.

    :return: a Place object
    """
    return random.choice(db.session.query(Place).all())

def get_random_npc() -> Npc :
    """
    Returns a random npc from the database

    :return: a Npc object
    """
    return random.choice(db.session.query(Npc).all())

def get_npc_random_trait_id(npc_id: int) -> int:
    """
    Returns a random reaction for a given npc

    :param npc_id: the npc to get the reaction from
    :return: a reaction identified by it's trait id
    """
    reactions = db.session.query(Reaction).filter_by(NPC_ID=npc_id.NPC_ID).all()
    reaction = random.choice(reactions)
    return reaction.TRAIT_ID

def get_npc_random_answer(npc_id:int, qa_type:int) -> Answer :
    """
    Returns a random answser from a given npc and question type

    :param npc_id: the npc to get the answer from
    :param qa_type: the type of the question
    :return: an Answer object
    """
    answers = db.session.query(Answer).filter_by(QA_TYPE=qa_type,NPC_ID=npc_id.NPC_ID).all()
    return random.choice(answers)

def get_random_question(qa_type: int) -> Question :
    """
    Returns a random inspector question from a question type

    :param qa_type: the type of the question
    :return: a Question object
    """
    answers = db.session.query(Question).filter_by(QUESTION_TYPE=qa_type).all()
    return random.choice(answers)

def get_trait_from_text(text: str) -> int:
    """
    Returns the trait_id from its text value

    :param text: the text representation of the trait in any lang
    :return: the trait_id linked to this text
    """
    trait_lid = db.session.query(Locale).filter_by(TEXT=text).one().TEXT_ID
    return db.session.query(Trait).filter_by(NAME_LID=trait_lid).one().TRAIT_ID

def get_trait_from_trait_id(trait_id: int) -> Trait:
    """
    Gets a Trait object from a trait_id

    :param trait_id: the id of the trait to search for
    :return: a Trait object
    """
    trait = db.session.query(Trait).filter_by(TRAIT_ID=trait_id).one()
    return trait

def get_reaction_description(lang, npc_id, trait_id) -> str:
    """
    Returns the description of the reaction of a given npc in the language specified by the parametter lang

    :param lang: the language to return the description in
    :param npc_id: the id of the npc to get the reaction description from
    :trait_id: the trait associated to the reaction to get the description from
    :return: the description in the given language
    """
    desc_lid = db.session.query(Trait).filter_by(TRAIT_ID=trait_id).one().DESC_LID
    return get_text_from_lid(lang, desc_lid)

def get_traits(lang: str) -> list:
    """
    Returns the list of all possible reactions trait in the given language

    :param lang: the lang to return the reactions traits in
    :return: a list of string reprensentation of the reactions traits
    """
    traits = []
    for trait in db.session.query(Trait).all():
        traits.append(get_text_from_lid(lang,trait.NAME_LID))
    return traits
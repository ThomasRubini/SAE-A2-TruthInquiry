# Load .env file
from dotenv import load_dotenv
load_dotenv()

import argparse

from sqlalchemy.orm import sessionmaker

from truthinquiry.ext.database.sa import engine
from truthinquiry.ext.database.models import *

Session = sessionmaker(bind=engine)
session = Session()

results = session.query(Npc).all()
print(results)

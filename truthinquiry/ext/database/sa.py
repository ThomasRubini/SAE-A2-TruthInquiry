from sqlalchemy import create_engine

from truthinquiry.ext.database.models import Base
from truthinquiry.ext.database.db_url import get_db_url

engine = create_engine(get_db_url())

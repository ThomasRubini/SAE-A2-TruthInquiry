from flask_sqlalchemy import SQLAlchemy

from truthinquiry.ext.database.models import Base
from truthinquiry.ext.database.db_url import get_db_url

db = SQLAlchemy(model_class=Base)

def setup_app_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True} # handle disconnections
    db.init_app(app)
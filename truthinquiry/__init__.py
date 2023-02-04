import os

import flask
from flask_socketio import SocketIO
from sqlalchemy import engine as eg
from flask_sqlalchemy import SQLAlchemy

from truthinquiry.app import TruthInquiryApp
from truthinquiry.database.database import db


# Instantiate
APP = TruthInquiryApp()

# THEN start db
db.init_app(APP)

# THEN start discord bot
APP.start_discord_bot()

# THEN register routes
from truthinquiry.routes import routes_api, routes_ui, routes_socketio

APP.register_blueprint(routes_api.routes_api, url_prefix="/api/v1")
APP.register_blueprint(routes_ui.routes_ui, url_prefix="/")

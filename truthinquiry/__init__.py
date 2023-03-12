import os

import flask
from sqlalchemy import engine as eg
from flask_sqlalchemy import SQLAlchemy

from truthinquiry.app import TruthInquiryApp

from truthinquiry.ext.database import fsa
from truthinquiry.ext.socketio import socket_io
from truthinquiry.ext.discord_bot import discord_bot

from truthinquiry.routes import routes_api, routes_ui, routes_socketio, routes_admin, routes_api_admin, handlers

def register_extensions(app):
    fsa.setup_app_db(app)

    socket_io.init_app(app)

    discord_bot.try_start()

def register_routes(app):
    app.register_blueprint(routes_api.routes_api, url_prefix="/api/v1")
    app.register_blueprint(routes_ui.routes_ui, url_prefix="/")
    app.register_blueprint(routes_admin.routes_admin, url_prefix="/admin")
    app.register_blueprint(routes_api_admin.routes_api_admin, url_prefix="/api/v1/admin")


def create_app():
    app = TruthInquiryApp()

    register_extensions(app)
    
    register_routes(app)

    handlers.register_handlers(app)

    return app

import os

import flask
from sqlalchemy import engine as eg
from flask_sqlalchemy import SQLAlchemy

from truthinquiry.app import TruthInquiryApp

from truthinquiry.ext.database import db
from truthinquiry.ext.socketio import socket_io
from truthinquiry.ext.discord_bot import discord_bot

from truthinquiry.routes import routes_api, routes_ui, routes_socketio

def register_extensions(app):
    db.init_app(app)

    socket_io.init_app(app)

    discord_bot.try_start()

def register_routes(app):
    app.register_blueprint(routes_api.routes_api, url_prefix="/api/v1")
    app.register_blueprint(routes_ui.routes_ui, url_prefix="/")


def create_app():
    app = TruthInquiryApp()

    register_extensions(app)
    
    register_routes(app)

    return app

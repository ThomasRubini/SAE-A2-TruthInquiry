import os

import flask
from flask_socketio import SocketIO

from truthinquiry import discord_bot

from sqlalchemy import engine as eg

from flask_sqlalchemy import SQLAlchemy


class TruthInquiryApp(flask.Flask):
    """
    Main class of the app
    A single instance 'APP' of this class will be created and shared across the files
    The class itself is a child class of flask.Flask and has property representing other services

    :attr SocketIO socketio_app: the SocketIO service
    :attr DiscordBot discord_bot: the Discord Bot service
    """

    def __init__(self):
        super().__init__("truthinquiry")

        self.games_list = {}

        self.config["SECRET_KEY"] = os.getenv("FLASK_SECRET")

        self.setupdb()

        self.socketio_app = SocketIO(
            self,
            cors_allowed_origins=(os.getenv("ORIGIN"), "http://127.0.0.1:5000", "http://localhost:5000")
        )

        self.discord_bot = discord_bot.DiscordBot()
        token = os.getenv("DISCORD_BOT_TOKEN")
        if token:
            self.discord_bot.start(token)
        else:
            print("No token set. Not starting discord bot")
    
    def setupdb(self):
        db_url = eg.URL.create(
            "mariadb+pymysql",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DBNAME")
        )

        self.config["SQLALCHEMY_DATABASE_URI"] = db_url

        self.db = SQLAlchemy(self)



APP = TruthInquiryApp()

from truthinquiry.routes import routes_api, routes_ui, routes_socketio

APP.register_blueprint(routes_api.routes_api, url_prefix="/api/v1")
APP.register_blueprint(routes_ui.routes_ui, url_prefix="/")

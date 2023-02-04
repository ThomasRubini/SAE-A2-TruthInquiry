import os

import flask

from truthinquiry import discord_bot
from truthinquiry.database import database
from flask_socketio import SocketIO

# minimal class definition/initialization

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

        self.socketio_app = SocketIO(
            self,
            cors_allowed_origins=(os.getenv("ORIGIN"), "http://127.0.0.1:5000", "http://localhost:5000")
        )

    def start_discord_bot(self):
        self.discord_bot = discord_bot.DiscordBot()
        token = os.getenv("DISCORD_BOT_TOKEN")
        if token:
            self.discord_bot.start(token)
        else:
            print("No token set. Not starting discord bot")


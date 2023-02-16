import os

import flask

from truthinquiry.ext import discord_bot

class TruthInquiryApp(flask.Flask):
    """
    Main class of the app
    The class itself is a child class of flask.Flask and has property representing other services

    :attr SocketIO socketio_app: the SocketIO service
    :attr DiscordBot discord_bot: the Discord Bot service
    """

    def __init__(self):
        super().__init__("truthinquiry")

        self.games_list = {}

        self.config["SECRET_KEY"] = os.getenv("FLASK_SECRET")

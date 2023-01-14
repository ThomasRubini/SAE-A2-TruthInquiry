import os

import flask
from flask_socketio import SocketIO

from truthseeker import discord_bot


class TruthSeekerApp(flask.Flask):
    """
    Main class of the app
    A single instance 'APP' of this class will be created and shared across the files
    The class itself is a child class of flask.Flask and has property representing other services

    :attr SocketIO socketio_app: the SocketIO service
    :attr DiscordBot discord_bot: the Discord Bot service
    """

    def __init__(self):
        super().__init__("truthseeker")

        self.games_list = {}

        self.config["SECRET_KEY"] = os.getenv("FLASK_SECRET")

        self.socketio_app = SocketIO(self,cors_allowed_origins=["https://truthinquiry.simailadjalim.fr","http://127.0.0.1:5000"])

        self.discord_bot = discord_bot.DiscordBot()
        token = os.getenv("DISCORD_BOT_TOKEN")
        if token:
            self.discord_bot.start(token)
        else:
            print("No token set. Not starting discord bot")

APP = TruthSeekerApp()

from truthseeker.routes import routes_api, routes_ui, routes_socketio

APP.register_blueprint(routes_api.routes_api, url_prefix="/api/v1")
APP.register_blueprint(routes_ui.routes_ui, url_prefix="/")

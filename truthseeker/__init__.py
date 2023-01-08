import flask
from flask_socketio import SocketIO
import os

class TruthSeekerApp(flask.Flask):

    def __init__(self):
        super().__init__("truthseeker")

        self.games_list = {}
        
        self.set_app_secret()
        self.socketio_app = SocketIO(self)

    def run_app(self):
        self.socketio_app.run(self)

    def set_app_secret(self):
        if os.path.isfile("instance/secret.txt"):
            f = open("instance/secret.txt", "r")
            self.config["SECRET_KEY"] = f.read()
            f.close()
            print("Read secret from secret.txt !")
        else:
            import secrets
            self.config["SECRET_KEY"] = secrets.token_hex()
            os.makedirs("instance", exist_ok=True)
            f = open("instance/secret.txt", "w")
            f.write(self.config["SECRET_KEY"])
            f.close()
            print("Generated secret and wrote to secret.txt !")

APP = TruthSeekerApp()

from truthseeker.routes import routes_api, routes_ui, routes_socketio

APP.register_blueprint(routes_api.routes_api, url_prefix="/api/v1")
APP.register_blueprint(routes_ui.routes_ui, url_prefix="/")

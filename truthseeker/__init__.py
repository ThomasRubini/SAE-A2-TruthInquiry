import flask
import os

from truthseeker.routes import routes_api, routes_ui


app = flask.Flask("truthseeker")

def set_secret(app):
    if os.path.isfile("instance/secret.txt"):
        f = open("instance/secret.txt", "r")
        app.config["SECRET_KEY"] = f.read()
        f.close()
        print("Read secret from secret.txt !")
    else:
        import secrets
        app.config["SECRET_KEY"] = secrets.token_hex()
        f = open("instance/secret.txt", "w")
        f.write(app.config["SECRET_KEY"])
        f.close()
        print("Generated secret and wrote to secret.txt !")

set_secret(app)


app.register_blueprint(routes_api.routes_api, url_prefix="/api/v1")
app.register_blueprint(routes_ui.routes_ui, url_prefix="/")

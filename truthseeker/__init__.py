import flask

from truthseeker import api

app = flask.Flask("truthseeker")

app.register_blueprint(api.api_routes, url_prefix="/api/v1")

@app.route("/")
def hello():
    return "Hello World!"
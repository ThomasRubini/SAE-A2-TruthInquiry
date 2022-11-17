import flask

from truthseeker import routes_api

app = flask.Flask("truthseeker")

app.register_blueprint(routes_api.api_routes, url_prefix="/api/v1")

@app.route("/")
def hello():
    return "Hello World!"

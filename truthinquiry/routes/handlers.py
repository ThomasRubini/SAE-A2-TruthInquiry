
import flask
from werkzeug.exceptions import HTTPException

def http_error_handler(e):
    return flask.render_template(
        "errorhandler.html",
        desc=e.description,
        url=f"https://http.cat/{e.code}"), e.code

def register_handlers(app):
    app.errorhandler(HTTPException)(http_error_handler)

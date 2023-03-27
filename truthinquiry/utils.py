from functools import wraps

import flask

def require_admin(*args, **kwargs):
    def decorator(route):
        @wraps(route)
        def decorated_function(*route_args, **route_kwargs):

            if flask.session.get("admin"):
                return route(*route_args, **route_kwargs)
            elif kwargs.get("api"):
                return {"error": 1, "msg": "Invalid authentication"}
            elif kwargs.get("ui"):
                return flask.redirect("/admin/auth")
            else:
                raise ValueError("Can't determine request type")
            
        return decorated_function
    return decorator

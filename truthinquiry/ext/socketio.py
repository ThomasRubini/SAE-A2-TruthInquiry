import os

from flask_socketio import SocketIO

socket_io = SocketIO(
    cors_allowed_origins=(os.getenv("ORIGIN"), "http://127.0.0.1:5000", "http://localhost:5000")
)

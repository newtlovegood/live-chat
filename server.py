import secrets
from dataclasses import dataclass

from flask import Flask, Blueprint
from flask_socketio import SocketIO
from redis import Redis


@dataclass
class Config:
    pass


class Server:
    def __init__(self, flask_app: Flask):
        self.flask_app = flask_app
        self.flask_app.secret_key = secrets.token_hex()
        self.socketio = SocketIO(self.flask_app)
        self.redis = Redis(host='localhost')

    def register_blueprint(self, blueprint: Blueprint):
        self.flask_app.register_blueprint(blueprint)

    def run(self):
        self.socketio.run(self.flask_app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)

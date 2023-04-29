import secrets

from flask import Flask

from chat.routes import router, socketio

app = Flask(__name__)

app.secret_key = secrets.token_hex()

app.register_blueprint(router)
socketio.init_app(app, debug=True, allow_unsafe_werkzeug=True)

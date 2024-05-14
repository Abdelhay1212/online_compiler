from flask import Flask

from .events import socketio
from .routes.main import main


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'secret-key'

    socketio.init_app(app)

    app.register_blueprint(main)

    return app

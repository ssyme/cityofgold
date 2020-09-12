from flask import Flask

from .extensions import db, login
from .views import main, boards, users
from .models import User

def create_app(config_file="settings.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    login.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(boards, url_prefix="/board")
    app.register_blueprint(users, url_prefix="/user")

    return app

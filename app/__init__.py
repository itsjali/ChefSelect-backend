import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate

from app.config import Config
from app.models import db


bcrypt = Bcrypt()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    CORS(app)

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import models

    from app.auth.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.views import main_bp
    app.register_blueprint(main_bp)

    return app

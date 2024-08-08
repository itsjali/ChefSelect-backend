from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from app.config import Config
from app.models import db

migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import models

    from app.views import main_bp
    app.register_blueprint(main_bp)

    return app

import pytest

from app import create_app
from app.models import db
from app.config import TestConfig


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(config_class="app.config.TestConfig")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope="module")
def init_database():
    flask_app = create_app(TestConfig)

    with flask_app.app_context():
        db.create_all()
        yield db
        db.drop_all()
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

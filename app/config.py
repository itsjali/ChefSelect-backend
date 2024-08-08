import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BACKEND_SECRET_KEY = "super-secret-key"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_POSTGRES_DB_URL") 
    TESTING = True
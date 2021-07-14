import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
    ENV='development'
    

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
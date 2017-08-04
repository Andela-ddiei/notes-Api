import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfiguration(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///notes.db'
    SECRET_KEY = os.environ['SECRET_KEY']


class TestingConfiguration(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.environ["NOTES_DATABASE_URI"]


class HerokuConfiguration(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["NOTES_DATABASE_URI"]

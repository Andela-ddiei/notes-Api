import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.environ['SECRET_KEY']


class DevelopmentConfiguration(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///notes.db'


class HerokuConfiguration(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["NOTES_DATABASE_URI"]


class TestingConfiguration(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.environ["NOTES_DATABASE_URI"]

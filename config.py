import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfiguration(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///notes.db'
    SECRET_KEY = os.environ['SECRET_KEY']


class TestingConfiguration(Config):
    TESTING = True
    TESTING_DATABASE_URI = 'sqlite:///test.db'

    SQLALCHEMY_ECHO = False

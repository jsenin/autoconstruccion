import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                                                          'instance', 'app.db')


class Development(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Testing(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


class TestingMemory(Testing):
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'


class Production(BaseConfig):
    DEBUG = False
    TESTING = False


app_config = {
    'DEFAULT': BaseConfig,
    'DEVELOPMENT': Development,
    'PRODUCTION': Production,
    'TESTING': Testing,
    'TESTING_MEMORY': TestingMemory
}

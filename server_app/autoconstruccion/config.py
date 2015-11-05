import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                                                          'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Testing(BaseConfig):
    TESTING = True


class Production(BaseConfig):
    DEBUG = False
    TESTING = False


app_config = {
    'DEFAULT': BaseConfig,
    'DEVELOPMENT': Development,
    'PRODUCTION': Production,
}



class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret'


class Development(BaseConfig):
    DEBUG = True


class Testing(BaseConfig):
    pass


class Production(BaseConfig):
    DEBUG = False


config = {
    'DEFAULT': BaseConfig,
    'DEVELOPMENT': Development,
    'PRODUCTION': Production,
}

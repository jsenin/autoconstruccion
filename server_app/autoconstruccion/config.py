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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class Production(BaseConfig):
    DEBUG = False
    TESTING = False


configs = {
    'DEFAULT': BaseConfig,
    'DEVELOPMENT': Development,
    'PRODUCTION': Production,
    'TESTING': Testing,
    'TESTING_MEMORY': TestingMemory
}


def config_app(app, config_name='DEFAULT'):

    # Load config from default app configs
    if config_name in configs:
        app.config.from_object(configs[config_name])
    else:
        raise ValueError("The config_name is not a defined config")

    # Load config from instance folder.
    app.config.from_pyfile('config.py', silent=True)

    # Load the file specified by the APP_CONFIG_FILE env variable
    app.config.from_envvar('AUTOCONSTRUCCION_APP_CONFIG_FILE', silent=True)

    # If we are on a TESTING app change the batabase uri to append '_test'
    # to avoid crushing actual data.
    if app.config['TESTING']:
        if app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite:///:memory:':
            app.config['SQLALCHEMY_DATABASE_URI'] += '_test'

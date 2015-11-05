from flask import Flask
from autoconstruccion.config import app_config
from autoconstruccion.web import bp as web
from autoconstruccion.models import db


def create_app(config_name='PRODUCTION'):
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    app.config.from_object(app_config[config_name])

    # Load config from instance folder.
    app.config.from_pyfile('config.py')

    # Load the file specified by the APP_CONFIG_FILE env variable
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    # Load database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(web, url_prefix='/', static_folder='static')

    return app


def create_db(config_name='PRODUCTION'):
    app = create_app(config_name)
    db.init_app(app)
    with app.test_request_context():
        from autoconstruccion.models import Project
        db.create_all()

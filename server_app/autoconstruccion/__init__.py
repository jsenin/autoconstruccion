from flask import Flask
from autoconstruccion.config import config_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name='PRODUCTION'):
    app = Flask(__name__, instance_relative_config=True)

    # config app
    config_app(app, config_name)

    # Load database
    db.init_app(app)

    # Register blueprints
    from autoconstruccion.web import bp as web
    app.register_blueprint(web, url_prefix='/', static_folder='static')

    return app


def create_db(config_name='PRODUCTION'):
    app = create_app(config_name)
    db.init_app(app)
    with app.test_request_context():
        db.create_all()

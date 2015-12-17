from flask import Flask
from autoconstruccion.config import config_app, config_notifier
from flask_sqlalchemy import SQLAlchemy
from autoconstruccion.login_manager import login_manager

db = SQLAlchemy()


def create_app(config_name='PRODUCTION'):
    app = Flask(__name__, instance_relative_config=True)

    # config app
    config_app(app, config_name)

    # load notifier
    config_notifier(app)

    # Load database
    db.init_app(app)

    # Init login
    login_manager.init_app(app)

    with app.app_context():
        # Register blueprints
        from autoconstruccion.login import bp as login_bp
        app.register_blueprint(login_bp)
        from autoconstruccion.web import bp as web
        app.register_blueprint(web, url_prefix='/', static_folder='static')
        from autoconstruccion.admin import bp as admin
        app.register_blueprint(admin, url_prefix='/admin', static_folder='static')
    # Register blueprints
    from autoconstruccion.web import bp as web
    app.register_blueprint(web, url_prefix='/', static_folder='static')
    from autoconstruccion.admin import bp as admin
    app.register_blueprint(admin, url_prefix='/admin', static_folder='static')
    from autoconstruccion.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app


def create_db(config_name='PRODUCTION'):
    app = create_app(config_name)
    db.init_app(app)
    with app.test_request_context():
        db.create_all()

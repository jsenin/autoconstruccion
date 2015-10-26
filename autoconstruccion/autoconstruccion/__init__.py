from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    app.config.from_object('config.Development')

    # Load config from instance folder.
    app.config.from_pyfile('config.py')

    # Load the file specified by the APP_CONFIG_FILE env variable
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    @app.route('/')
    def hello_world():
        return "Hello World!!"

    return app

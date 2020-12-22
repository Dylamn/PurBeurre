from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config


api = Api()
db = SQLAlchemy()
migrate = Migrate()


def make_app(configuration: Config = None):
    """Application Factory pattern"""
    from .resources import Category, Categories

    if configuration is None:  # Use the default configuration.
        configuration = Config()

    # Create the Flask application.
    app = Flask(__name__)
    app.config.from_object(configuration)

    # Initialize database layer.
    db.init_app(app)
    migrate.init_app(app, db)

    # Finally, initialize the api.
    api.init_app(app)

    return app

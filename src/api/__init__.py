from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from src.api.exceptions.handlers import register_handlers
from src.config import Config

api = Api()
db = SQLAlchemy()
migrate = Migrate()


def make_app(configuration: Config = None):
    """Application Factory pattern"""
    from .resources import Category, Categories
    from src.api.routes.auth import auth

    if configuration is None:  # Use the default configuration.
        configuration = Config()

    # Create the Flask application.
    app = Flask(__name__)
    app.config.from_object(configuration)
    register_handlers(app)

    # Initialize database layer.
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    app.register_blueprint(auth)

    # Finally, initialize the api.
    api.init_app(app)

    return app

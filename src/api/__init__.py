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

    if configuration is None:
        configuration = Config()

    app = Flask(__name__)
    app.config.from_object(configuration)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    return app

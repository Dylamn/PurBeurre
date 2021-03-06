from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from src.api.exceptions.handlers import register_handlers
from flask_jwt_extended import JWTManager
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

    # Register error handlers
    register_handlers(app)

    # Initialize database layer.
    db.init_app(app)
    migrate.init_app(app, db)

    # Register authentication routes
    app.register_blueprint(auth)

    # Setup the Flask-JWT-Extented extension
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        # TODO: Callback doesn't work, check why
        from .models import BlacklistToken

        jti = decrypted_token['jti']

        return BlacklistToken.check_blacklist(jti)

    # Finally, initialize the api.
    api.init_app(app)

    return app

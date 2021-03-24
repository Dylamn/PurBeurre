from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from src.api.exceptions.handlers import register_handlers
from src.api.exceptions.invalid_token import InvalidToken
from flask_jwt_extended import JWTManager
from src.config import Config

api = Api()
db = SQLAlchemy()
migrate = Migrate()


def make_app(configuration: Config = None):
    """Application Factory pattern"""
    from src.api.routes.auth import auth
    from src.api.routes.imports import imports
    from src.api.resources import Product, Category, UserSubstitute

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

    # Register routes
    app.register_blueprint(auth)
    app.register_blueprint(imports)

    # Setup the Flask-JWT-Extented extension
    jwt = JWTManager(app)

    @app.route('/')
    def root():
        """This endpoint is used by the CLI to determines if the API is available or not."""
        return {}, 200

    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        """Check whether an access token is blacklisted or not."""
        from .models import BlacklistToken
        jti = decrypted_token['jti']

        if BlacklistToken.check_blacklist(jti):
            raise InvalidToken("Token is blacklisted. Please log in again.")

        return False

    # Finally, initialize the api.
    api.init_app(app)

    return app

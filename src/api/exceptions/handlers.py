from flask import jsonify
from .invalid_token import InvalidToken


def register_handlers(app):
    @app.errorhandler(InvalidToken)
    def invalid_token(error):
        response = jsonify(error.to_response())
        response.status_code = error.status_code

        return response

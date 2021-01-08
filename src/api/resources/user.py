from flask_restful import Resource, reqparse
from src.api.models.user import User as UserModel
from src.api import api


class User(Resource):
    def __init__(self):
        self.validator = reqparse.RequestParser()

    def post(self):
        self.validator.add_argument("email") \
            .add_argument("username") \
            .add_argument('password')

        # Validate parameters...
        args = self.validator.parse_args()

        # Create the new record in the DB.
        user = UserModel.create(args)

        response_body = {
            'status': 'ok',
            'message': 'new user registered.',
            'user': user.serialize()
        }

        return response_body, 201

api.add_resource(User, '/users')

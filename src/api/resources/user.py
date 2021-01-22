from flask_restful import Resource, reqparse
from src.api.models.user import User as UserModel
from src.api import api
from src.utils import is_valid_email

class User(Resource):
    def __init__(self):
        self.validator = reqparse.RequestParser()

    def post(self):
        self.validator.add_argument("email", required=True) \
            .add_argument("username", required=True) \
            .add_argument('password', required=True)

        # Validate parameters...
        args = self.validator.parse_args()

        if is_valid_email(args['email']) is not True:
            response_body = {
                'status': 'error',
                'message': 'The given email is not valid.',
            }
            return response_body, 400

        user = UserModel.query.filter_by(email=args['email']).first()

        if user:
            response_body = {
                'status': 'fail',
                'message': 'User already exist. Try another email or log in.',
            }
            return response_body, 400

        # Create the new record in the DB.
        user = UserModel.create(args)

        # Then, generate the auth token
        auth_token = user.encode_auth_token()

        response_body = {
            'status': 'ok',
            'message': 'new user registered.',
            'auth_token': auth_token
        }

        return response_body, 201

api.add_resource(User, '/users')

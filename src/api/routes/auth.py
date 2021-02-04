from flask import Blueprint, request
from flask_restful import reqparse
from bcrypt import checkpw
from src.api.models.user import User as UserModel
from src.api.models.blacklist_token import BlacklistToken
from src.utils import is_valid_email
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/me', methods=['GET'])
def me():
    # Retrieve the Authorization header
    resp, _ = parse_token_from_header()

    if not isinstance(resp, str):
        user = UserModel.query.filter_by(id=resp).first()
        response_body = {
            'status': 'ok',
            'user': user.serialize()
        }

        return response_body, 200

    # Token is not valid or expired
    response_body = {
        'status': 'error',
        'message': resp
    }

    return response_body, 401

@auth.route('/register', methods=['POST'])
def register():
    validator = reqparse.RequestParser()
    validator.add_argument("email", required=True) \
        .add_argument("username", required=True) \
        .add_argument('password', required=True)

    # Validate parameters...
    args = validator.parse_args()

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

@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password').encode('utf-8')

    user = UserModel.query.filter_by(
        email=email
    ).first()

    if not user or not checkpw(password, user.password.encode('utf-8')):
        response_body = {
            'status': 'fail',
            'message': 'Invalid email/password combinaison.'
        }

        return response_body, 400

    auth_token = user.encode_auth_token()

    response_body = {
        'status': 'ok',
        'message': 'Successfully logged in.',
        'auth_token': auth_token
    }

    return response_body, 200


@auth.route('/logout', methods=['POST'])
def logout():
    resp, token = parse_token_from_header()

    if not isinstance(resp, str):
        # Mark the token as blacklisted
        blacklist_token = BlacklistToken(token)

        try:
            blacklist_token.save()
            response_body = {
                'status': 'ok',
                'message': 'Successfully logged out.'
            }

            return response_body, 200
        except Exception:
            response_body = {
                'status': 'error',
                'message': 'An unexpected error occurred. Please try again later.'
            }

            return response_body, 500

    else:
        response_body = {
            'status': 'error',
            'message': resp
        }

        return response_body, 401


@auth.route('/refresh', methods=['POST'])
def refresh():
    pass


def parse_token_from_header():
    """Retrieve the auth token from the header and parse it."""
    from src.api.exceptions.invalid_token import InvalidToken

    authorization_header = request.headers.get('Authorization')
    token = None

    if authorization_header:
        split_header = authorization_header.split(' ')

        if len(split_header) != 2:
            raise  InvalidToken("Token could not be parsed from header.")

        token = split_header[1]

    if token is None:
        raise InvalidToken("Provide a valid auth token.")

    resp = UserModel.decode_auth_token(token)

    return resp, token

from flask import Blueprint, request
from flask_restful import reqparse
from bcrypt import checkpw
from src.api.models.user import User as UserModel
from src.api.models.blacklist_token import BlacklistToken
from src.utils import is_valid_email
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/me', methods=['GET'])
@jwt_required
def me():
    # Retrieve the Authorization header
    user_identity = get_jwt_identity()
    user = UserModel.query.filter_by(id=user_identity).first()

    response_body = {
        'status': 'ok',
        'user': user.serialize()
    }

    return response_body, 200


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
    user = UserModel.create(
        username=args['username'],
        email=args['email'],
        password=args['password']
    )

    # Then, generate the response with tokens
    response_body = {
        'status': 'ok',
        'message': 'new user registered.',
        'access_token': create_access_token(user.id),
        'refresh_token': create_refresh_token(user.id),
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

    response_body = {
        'status': 'ok',
        'message': 'Successfully logged in.',
        'access_token': create_access_token(identity=user.id),
        'refresh_token': create_refresh_token(identity=user.id)
    }

    return response_body, 200


@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    token = get_raw_jwt()

    # Mark the token as blacklisted
    blacklist_token = BlacklistToken(token.get('jti'))

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


@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """Generate a new access token from a refresh token."""
    current_user = get_jwt_identity()

    response_body = {
        'status': 'ok',
        'access_token': create_access_token(identity=current_user)
    }

    return response_body, 200


def parse_token_from_header():
    """Retrieve the auth token from the header and parse it."""
    from src.api.exceptions.invalid_token import InvalidToken

    authorization_header = request.headers.get('Authorization')
    token = None

    if authorization_header:
        split_header = authorization_header.split(' ')

        if len(split_header) != 2:
            raise InvalidToken("Token could not be parsed from header.")

        token = split_header[1]

    if token is None:
        raise InvalidToken("Provide a valid auth token.")

    resp = UserModel.decode_auth_token(token)

    return resp, token

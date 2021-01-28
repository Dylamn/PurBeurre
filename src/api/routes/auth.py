from flask import Blueprint, request
from bcrypt import checkpw
from src.api.models.user import User as UserModel
from src.api.models.blacklist_token import BlacklistToken

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
    authorization_header = request.headers.get('Authorization')
    token = None

    if authorization_header:
        token = authorization_header.split(' ')[1]


    if token is None:
        from src.api.exceptions.invalid_token import InvalidToken

        raise InvalidToken("Provide a valid auth token.")
        # response_body = {
        #     'status': 'error',
        #     'message': 'Provide a valid auth token.'
        # }

        return response_body, 401

    resp = UserModel.decode_auth_token(token)

    return resp, token

import jwt

from .. import db
from src.config import Config
from .base_model import BaseModel
from datetime import datetime, timedelta
from .blacklist_token import BlacklistToken

class User(db.Model, BaseModel):
    """User Model

    Attributes:
        id (int): The identifier of the user.
        username (str): The nickname/username of the user.
        email (str): The email of the user.
        password (str): The bcrypt hashed value of the user password.
        created_at (str): Datetime where this user has been created.
        updated_at (str): Datetime of the last update of this user.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=128), nullable=False)
    email = db.Column(db.String(length=255), nullable=False)
    password = db.Column(db.String(length=255), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def serialize(self):
        """Return a serialized object data format."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def encode_auth_token(self):
        """
        Generates the JWT Auth Token.
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_TTL),
                'iat': datetime.utcnow(),
                'sub': self.id
            }

            return jwt.encode(payload, Config.JWT_SECRET_KEY, Config.JWT_ALGO)
        except TypeError as ex:
            return ex

    @staticmethod
    def decode_auth_token(token):
        """
        Decodes the Auth Token.
        :param token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(
                token, Config.JWT_SECRET_KEY, algorithms=Config.JWT_ALGO
            )

            if BlacklistToken.check_blacklist(payload['jti']):
                return 'Token is blacklisted. Please log in again.'

            return payload['identity']  # The ID of the user

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please try to log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please try to log in again.'

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

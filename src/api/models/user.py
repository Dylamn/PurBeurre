import jwt
from .. import db
from src.config import Config
from datetime import datetime, timedelta
from .blacklist_token import BlacklistToken

class User(db.Model):
    """Category Model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=128), nullable=False)
    email = db.Column(db.String(length=255), nullable=False)
    password = db.Column(db.String(length=255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @classmethod
    def make(cls, data):
        """Instanciate a new model."""
        return cls(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    @classmethod
    def create(cls, data):
        """Save a new model and return the instance."""
        return cls.make(data).save()

    def save(self):
        """Save the model to the database."""
        db.session.add(self)
        db.session.commit()

        return self

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
        Generates the JWT Authen Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_TTL),
                'iat': datetime.utcnow(),
                'sub': self.id
            }

            return jwt.encode(payload, Config.JWT_SECRET, Config.JWT_ALGO)
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
                token, Config.JWT_SECRET, algorithms=Config.JWT_ALGO
            )

            if BlacklistToken.check_blacklist(token):
                return 'Token is blacklisted. Please log in again.'

            return payload['sub']  # The ID of the user

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please try to log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please try to log in again.'

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

import jwt
from .. import db
from datetime import datetime, timedelta
from src.config import Config


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    blacklisted_at = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def check_blacklist(token):
        """
        Check whether the token has been blacklisted.
        """
        res = BlacklistToken.query.filter_by(token=str(token)).first()

        if res:  # The token is blacklisted
            return True

        return False

    def __init__(self, token, **kwargs):
        super(BlacklistToken, self).__init__(**kwargs)

        self.token = token
        self.blacklisted_at = datetime.utcnow()

    def save(self):
        """Save the model to the database."""
        db.session.add(self)
        db.session.commit()

        return self

    def __repr__(self):
        return f'<token: {self.token}>'

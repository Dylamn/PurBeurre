from .. import db
from datetime import datetime


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    jwt_id = db.Column(db.String(36), primary_key=True, autoincrement=False)
    blacklisted_at = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def check_blacklist(token_id):
        """
        Check whether the token has been blacklisted.
        """
        res = BlacklistToken.query.filter_by(jwt_id=str(token_id)).first()

        if res:  # The token is blacklisted
            return True

        return False

    def __init__(self, token_id, **kwargs):
        super(BlacklistToken, self).__init__(**kwargs)

        self.jwt_id = token_id
        self.blacklisted_at = datetime.utcnow()

    def save(self):
        """Save the model to the database."""
        db.session.add(self)
        db.session.commit()

        return self

    def __repr__(self):
        return f'<token: {self.jwt_id}>'

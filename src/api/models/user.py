from .. import db
from datetime import datetime

class User(db.Model):
    """Category Model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=128), nullable=False)
    email = db.Column(db.String(length=255), nullable=False)
    password = db.Column(db.String(length=255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

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
        """Persist the model to the database."""
        return cls.make(data).save()

    def save(self):
        """Send modifications to the database and persist it."""
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

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

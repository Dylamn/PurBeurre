from .. import db
from datetime import datetime


class BaseModel(db.Model):
    """The base class used for all models.

    Attributes:
        is_recently_created (bool): Determine if the model was created during the session.
    """
    is_recently_created = False

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)

    @classmethod
    def make(cls, data):
        """Instanciate a new model."""
        return cls(
            username=data['username'],
            email=data['email'],
            password=data['password'],
        )

    @classmethod
    def create(cls, data):
        """Save a new model and return the instance."""
        model = cls.make(data).save()

        model.is_recently_created = True

        return model

    def touch(self):
        """Touch model timestamps."""
        if self.created_at is None:
            self.created_at = datetime.utcnow()

        self.updated_at = datetime.utcnow()

        return self

    def save(self):
        """Save the model to the database."""
        self.touch()

        db.session.add(self)
        db.session.commit()

        return self

    def serialize(self):
        """Return a serialized object data format."""
        raise NotImplementedError()
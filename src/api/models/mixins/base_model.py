from src.api import db
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(object):
    """The base class used for all models.

    Attributes:
        is_recently_created (bool): Determine if the model was created during the session.
    """
    @declared_attr
    def created_at(self):
        return db.Column(db.DateTime, nullable=True)

    @declared_attr
    def updated_at(self):
        return db.Column(db.DateTime, nullable=True)

    is_recently_created = False

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)

        self.is_recently_created = False

    @classmethod
    def make(cls, **kwargs):
        """Instanciate a new model which is not saved in the database."""
        return cls(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        """Save a new model and return the instance."""
        model = cls.make(**kwargs).save()

        model.is_recently_created = True

        return model

    @classmethod
    def first_or_create(cls, search: dict, **kwargs):
        """Fetch a model for the database if exists otherwise,
        create a new one with the given keywords arguments.

        Args:
            search (dict): Fields which will be filtered for the research.
            kwargs: The Attributes which will be used for the model creation.

        Returns:
            Product
        """

        model = cls.query.filter_by(**search).first()

        if model:
            return model

        return cls().create(**{**search, **kwargs})

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

    def delete(self):
        """Delete the model from the database."""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Return a serialized object data format."""
        raise NotImplementedError()
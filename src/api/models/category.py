from src.api import db


class Category(db.Model):
    """Category Model

    Attributes:
        id (int): The identifier of the category.
        name (str): The category name.
        tag (str): The tag associated to the category.

    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=255), nullable=False)
    tag = db.Column(db.String(length=128), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)

    @classmethod
    def make(cls, **kwargs):
        """Instanciate a new model."""
        return cls(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        """Save a new model and return the instance."""
        return cls.make(**kwargs).save()

    def save(self):
        """Save the model to the database."""
        db.session.add(self)
        db.session.commit()

        return self

    def serialize(self):
        """Return a serialized object data format."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

from src.api import db
from .mixins import BaseModel, Searchable

class Category(db.Model, BaseModel, Searchable):
    """Category Model

    Attributes:
        id (int): The identifier of the category.
        name (str): The category name.
        tag (str): The tag associated to the category.

    """
    __name__ = 'Category'
    __tablename__ = 'categories'
    __metaclass__ = Searchable

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=255), nullable=False)
    tag = db.Column(db.String(length=128), nullable=False, unique=True)


    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)

    def serialize(self):
        """Return a serialized object data format."""
        return {
            'id': self.id,
            'name': self.name,
            'tag': self.tag,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

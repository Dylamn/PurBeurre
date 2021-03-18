from .. import db
from .category import Category
from src.database.products_categories import products_categories
from .mixins import BaseModel, Searchable
from src.utils import pluck


class Product(db.Model, BaseModel, Searchable):
    """Product Model

    Attributes:
        id (int): The product identifier
        name (str): The name of the product
        generic_name (str): A generic name for this product
        brands (str): The brand(s) name(s) of the company which own this product.
        stores (str): The stores where the product can be found.
        nutriscore_grade (str): Indicate the product healthiness with a letter.
        url (str): The OpenFoodFacts URL of this product.
        created_at (str): The datetime where the product has been imported.
        updated_at (str): The datetime where the last product update occurs.

        is_recently_created (bool): Determine if the model was created during the session.
    """
    __name__ = 'Product'
    __tablename__ = 'products'

    # Table columns...
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=255), nullable=False)
    generic_name = db.Column(db.String(length=255), nullable=True)
    brands = db.Column(db.String(length=128), nullable=True)
    stores = db.Column(db.String(length=128), nullable=True)
    nutriscore_grade = db.Column(db.String(1), nullable=True)
    url = db.Column(db.String(length=255), nullable=True)

    # Relationships...
    categories = db.relationship(
        Category.__name__, secondary=products_categories, lazy=True,
        backref=db.backref('products', lazy=True)
    )

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    @classmethod
    def search(cls, search_input: str, operator='REGEXP'):
        """Apply a regexp constraint to the where clause on the name column."""

        # `REGEXP` operator works for MySQL and not for all SGBD.
        # For example, in PostgreSQL, it should be a tilde `~`.
        return cls.query.filter(cls.name.op(operator)(search_input))

    def find_substitute(self, category_tag: str = None) -> list:
        """Find one or more substitute which has a better nutriscore_grade.

        Product categories are ordered in order to have
        the most specifics categories at the end of the list.
        """
        tags = pluck([c.serialize() for c in self.categories], 'tag')

        if len(tags) < 0:
            return []

        if category_tag is None:
            category_tag = tags[-1]
        elif category_tag not in tags:
            return []

        substitutes = Product.query.filter(
            Product.id != self.id,
            Product.categories.any(tag=category_tag),
            Product.nutriscore_grade <= self.nutriscore_grade
        ).order_by(Product.nutriscore_grade).all()

        return substitutes

    def serialize(self):
        """Return a serialized object data format."""
        return {
            'id': self.id,
            'name': self.name,
            'generic_name': self.generic_name,
            'brands': self.brands,
            'stores': self.stores,
            'nutriscore_grade': self.nutriscore_grade,
            'url': self.url,
            'categories': [c.serialize() for c in self.categories if c],
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

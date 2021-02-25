from .. import db
from .category import Category
from src.database.products_categories import products_categories


class Product(db.Model):
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

    __tablename__ = 'products'

    # Table columns...
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=255), nullable=False)
    generic_name = db.Column(db.String(length=255), nullable=True)
    brands = db.Column(db.String(length=128), nullable=True)
    stores = db.Column(db.String(length=128), nullable=True)
    nutriscore_grade = db.Column(db.String(1), nullable=True)
    url = db.Column(db.String(length=255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    is_recently_created: bool = False

    # Relationships...
    categories = db.relationship(
        Category.__name__, secondary=products_categories, lazy=True,
        backref=db.backref('products', lazy=True)
    )

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

        self.is_recently_created = False

    @classmethod
    def make(cls, **kwargs):
        """Instanciate a new model which is not saved in the database."""
        return cls(**kwargs)

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

        return cls().create(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        """Save a new model and return the instance."""
        model = cls.make(**kwargs).save()

        model.is_recently_created = True

        return model

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
            'generic_name': self.generic_name,
            'brands': self.brands,
            'stores': self.stores,
            'nutriscore_grade': self.nutriscore_grade,
            'url': self.url,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

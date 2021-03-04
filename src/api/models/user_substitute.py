from .. import db
from .base_model import BaseModel


class UserSubstitute(db.Model, BaseModel):
    """User Substitute Model

    Attributes:
        user_id (int): The ID of the user to which this substitute belongs to.
        original_product_id (int): The original product which is substitued.
        substitute_product_id (int): The product which substitute the original.
        created_at (str): The datetime where the substitute has been created.
        updated_at (str): The datetime where the substitute last update occurs.

        is_recently_created (bool): Determine if the model was created during the session.
    """
    __name__ = 'UserSubstitute'
    __tablename__ = 'users_substitutes'

    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False
    )
    original_product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), primary_key=True, autoincrement=False
    )
    substitute_product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), primary_key=True, autoincrement=False
    )

    original_product = db.relationship(
        "Product", foreign_keys='UserSubstitute.original_product_id'
    )
    substitute_product = db.relationship(
        "Product", foreign_keys='UserSubstitute.substitute_product_id'
    )

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'original_product': self.original_product.serialize(),
            'substitute_product': self.substitute_product.serialize(),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }

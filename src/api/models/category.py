from src.api import db


class Category(db.Model):
    """Category Model"""
    __tablename__ = 'categories'

    id = db.Column(db.String(255), primary_key=True, autoincrement=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=True)
    products_count = db.Column(db.Integer, nullable=False, default=0)
    known = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

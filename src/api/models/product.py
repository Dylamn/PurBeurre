from .. import db


class Product(db.Model):
    """Category Model"""
    __tablename__ = 'products'

    id = db.Column(db.String(255), primary_key=True, autoincrement=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

from .. import db


class UserProduct(db.Model):
    """Category Model"""
    __tablename__ = 'users_products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    product_id = db.Column(db.String(255), primary_key=True, autoincrement=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<{} '{}.{}'>".format(self.__name__, self.id, self.product_id)

from .. import db


class User(db.Model):
    """Category Model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.String(length=128, nullable=False)
    email = db.String(length=255, nullable=False)
    password = db.String(length=255, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<{} '{}'>".format(self.__name__, self.id)

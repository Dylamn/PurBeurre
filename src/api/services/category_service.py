from datetime import datetime

from ..models.category import db, Category as CategoryModel


class Category:
    @classmethod
    def create(cls, data):
        exists = CategoryModel.query.filter_by(id=data['id']).first()

        if not exists:
            new_category = CategoryModel(
                id=data['id'],
                name=data['name'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            cls.save(new_category)

            return {
                'status': 'ok',
                'message': 'category created.'
            }, 201

        return {
            'status': 'error',
            'message': 'category already exist.'
        }, 400

    @staticmethod
    def save(data):
        db.session.add(data)
        db.session.commit()

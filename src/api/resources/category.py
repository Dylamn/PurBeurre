from flask import request
from flask_restful import Resource
from math import ceil
from src.api import api
from src.api.models import Category as CategoryModel


class Category(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search_query = request.args.get('q')

        # Start querying the model...
        if search_query:
            query = CategoryModel.search(search_query)
        else:
            query = CategoryModel.query

        categories = query.paginate(page, per_page, error_out=False)

        body = {
            "categories": [c.serialize() for c in categories.items],
            "meta": {
                "current_page": categories.page,
                "last_page": ceil(categories.total / 10),
                "total": categories.total,
            }
        }

        return body, 200

api.add_resource(Category, '/categories')

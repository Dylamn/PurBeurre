from flask import request
from flask_restful import Resource
from math import ceil
from src.api.models import Product as ProductModel
from src.api import api


class Product(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = request.args.get('per_page', 10)
        search_query = request.args.get('q')

        # Start querying the model...
        if search_query:
            query = ProductModel.search(search_query)
        else:
            query = ProductModel.query

        products = query.paginate(page, per_page, error_out=False)

        body = {
            "products": [p.serialize() for p in products.items],
            "meta": {
                "current_page": products.page,
                "last_page": ceil(products.total / 10),
                "total": products.total,
            }
        }

        return body, 200


api.add_resource(Product, '/products')

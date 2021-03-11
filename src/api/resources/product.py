from flask import request
from flask_restful import Resource
from math import ceil
from src.api.models import Product as ProductModel
from src.api import api


class Product(Resource):
    def get(self):
        substituate = request.args.get('substituate')

        if substituate:
            response = self._search_substitutes(substituate)
        else:
            response = self._search_products()

        return response

    @staticmethod
    def _search_substitutes(product_id):
        category_level = int(request.args.get('category_level', 0))

        original_product = ProductModel.query.filter_by(
            id=product_id
            # TODO: create a more friendly 404 response (create a first_or_fail method).
        ).first_or_404()

        category, substitutes, max_depth = original_product.find_substitute(
            category_level
        )

        body = {
            'category': category.tag,
            'depth_level': category_level,
            'max_depth': max_depth,
            'substitutes': [product.serialize() for product in substitutes]
        }

        return body, 200

    @staticmethod
    def _search_products():
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

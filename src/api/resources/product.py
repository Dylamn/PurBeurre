from flask import request
from flask_restful import Resource, reqparse
from math import ceil
from src.api.models import Product as ProductModel
from src.api.models import Category as CategoryModel
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
        parser = reqparse.RequestParser()
        # Add fields to validate
        parser.add_argument(
            'category_tag', type=str, nullable=True, help="The tag of a category"
        )
        args = parser.parse_args()
        
        category_tag = args['category_tag']

        original_product = ProductModel.query.filter_by(
            id=product_id
            # TODO: create a more friendly 404 response (create a first_or_fail method).
        ).first_or_404()

        substitutes = original_product.find_substitute(
            category_tag
        )

        body = {
            'category_tag': category_tag,
            'substitutes': [product.serialize() for product in substitutes]
        }

        return body, 200

    @staticmethod
    def _search_products():
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search_query = request.args.get('q')
        category_tag = request.args.get('category_tag')

        # Start querying the model...
        if search_query:
            query = ProductModel.search(search_query)
        else:
            query = ProductModel.query

        if category_tag is not None:
            query = query.join(ProductModel.categories, aliased=True).filter(
                CategoryModel.tag == category_tag
            )

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

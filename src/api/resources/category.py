import requests
from flask import request
from flask_restful import Resource, reqparse
from ..services.category_service import Category as Service
from src.api import api


class Category(Resource):
    OPENFOODFACTS_BASE = 'https://fr.openfoodfacts.org'

    def __init__(self):
        super(Category, self).__init__()
        self.validator = reqparse.RequestParser()

    def get(self):
        return requests.get(f'{self.OPENFOODFACTS_BASE}/categories.json').json()

    def post(self):
        # Define validation rules...
        self.validator \
            .add_argument('id', type=str, required=True) \
            .add_argument('name', type=str, required=True)

        # Validate the given request data,
        # throw an HTTP 400 response if there's a problem with the given data.
        params = self.validator.parse_args()

        return Service.create(params)

    def put(self):
        categories = self.get()

        for category in categories:
            Service.create(category)

        return {'message': 'No content'}, 204


api.add_resource(Category, '/categories')

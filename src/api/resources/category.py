import requests
from flask_restful import Resource, reqparse
from src.api import api
from src.api.config import Config


class Category(Resource):
    def get(self, category_id):
        return requests.get(
            f'{Config.OPENFOODFACTS_BASE}/categorie/{category_id}.json'
        ).json()


api.add_resource(Category, '/categories/<string:category_id>')

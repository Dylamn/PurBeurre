import requests
from flask_restful import Resource
from src.api import api
from src.config import Config


class Categories(Resource):
    def get(self):
        return requests.get(
            f'{Config.OPENFOODFACTS_BASE}/categories.json'
        ).json()


api.add_resource(Categories, '/categories')

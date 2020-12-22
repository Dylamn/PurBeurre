import requests
from flask_restful import Resource, reqparse
from src.api import api
from src.api.config import Config


class Product(Resource):
    def __init__(self):
        self.validator = reqparse.RequestParser()

    def get(self):
        return requests.get(f'{Config.OPENFOODFACTS_BASE}/products')


api.add_resource(Product, '/products')

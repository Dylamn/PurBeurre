import requests
from flask import request
from flask_restful import Resource
from ..services.category_service import Category as Service
from src.api import api


class Category(Resource):

    base_url = 'https://fr.openfoodfacts.org'

    def get(self):

        return requests.get(f'{self.base_url}/categories.json').json()

    def post(self):
        res = Service.create(request.form['data'])


api.add_resource(Category, 'categories')

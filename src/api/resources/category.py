from flask_restful import Resource
import requests


class Category(Resource):

    base_url = 'https://fr.openfoodfacts.org'

    def get(self):

        return requests.get(f'{self.base_url}/categories.json').json()

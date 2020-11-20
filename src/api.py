from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Categories(Resource):
    def get(self):
        return {'categories': 'a list ...'}


api.add_resource(Categories, '/categories')

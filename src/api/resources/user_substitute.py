from flask import request
from flask_restful import Resource
from src.api.models import UserSubstitute as UserSubstituteModel
from src.api import api
from flask_jwt_extended import jwt_required, get_jwt_identity


class UserSubstitute(Resource):
    @jwt_required
    def get(self):
        substitutes = UserSubstituteModel.query.filter_by(
            user_id=get_jwt_identity()
        ).all()

        return {
            'users_substitutes': [s.serialize() for s in substitutes]
        }, 200

    @jwt_required
    def post(self):
        original_product_id = request.args.get('original_product_id')
        substitute_id = request.args.get('substitute_id')

        user_substitute = UserSubstituteModel.first_or_create({
            'user_id': get_jwt_identity(),
            'original_product_id': original_product_id,
            'substitute_product_id': substitute_id
        })

        return {
            'message': 'A new substitute has been created.',
            'user_substitute': user_substitute.serialize()
        }, 201

api.add_resource(UserSubstitute, '/users/substitutes')
